
import argparse
import datetime
import keras
import numpy as np
import tensorflow as tf
import math
from glob import glob
import os.path

from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input, Embedding, Dropout, MaxPooling1D, MaxPooling2D, Bidirectional, Conv1D, Conv2D
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.callbacks import TensorBoard, ReduceLROnPlateau

from sklearn.metrics import classification_report
from tcn import TCN, tcn_full_summary


from src.user import User
from src.baecke import baecke

from data.datagenerator import Datagenerator

def seq_to_seq_classification():

  logdir = "logs/fit/seq_to_seq_classification" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = TensorBoard(log_dir=logdir)


  # Generators
  training_generator = Datagenerator()
  val_generator = Datagenerator(train=False)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp[31][0])
  print(outp.shape)

  # LSTM for sequence classification 
  model = Sequential()
  model.add(LSTM(32,return_sequences=True, input_shape=(training_generator.seq_len,16)))
  model.add(LSTM(5,return_sequences=True, input_shape=(training_generator.seq_len,16)))
  # model.add(Dense(training_generator.n_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
  print(model.summary())
  model.fit(training_generator, epochs=300,callbacks=[tensorboard_callback])

  scores = model.evaluate(val_generator, verbose=1)
  print(scores)
  print("Accuracy: %.2f%%" % (scores[1]*100))

def seq_classification():
  logdir = "logs/fit/seq_classification" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = TensorBoard(log_dir=logdir)

  n_features = 11
  n_classes = 3

  # Generators
  training_generator = Datagenerator(squash_class=True, n_features=n_features, n_classes=n_classes)
  val_generator = Datagenerator(train=False, squash_class=True, n_features=n_features, n_classes=n_classes)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp.shape)
  print(outp.shape)

  # LSTM for sequence classification 
  model = Sequential()
  model.add(Dense(training_generator.seq_len, activation='sigmoid', input_shape=(training_generator.seq_len,n_features)))
  model.add(LSTM(training_generator.seq_len,return_sequences=True))
  model.add(LSTM(16,return_sequences=True))
  model.add(LSTM(16))
  model.add(Dense(training_generator.n_classes, activation='softmax'))

  model.summary()
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

  model.fit(
    training_generator, 
    epochs=200, 
    callbacks=[tensorboard_callback], 
    validation_data=val_generator)
  scores = model.evaluate(val_generator, verbose=1)


# Ballinger2018
def deepheart():
  logdir = "logs/fit/deepheart" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = TensorBoard(log_dir=logdir)

  n_features = 11
  n_classes = 3
  seq_len = 128

  # Generators
  training_generator = Datagenerator(squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)
  val_generator = Datagenerator(train=False, squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp.shape)
  print(outp.shape)

  opt = tf.keras.optimizers.Adam(learning_rate=0.00001)
  reduce_lr = ReduceLROnPlateau(monitor='val_categorical_accuracy', factor=0.9,
                              patience=50, min_lr=0.0000001)


  i = Input(shape=(training_generator.seq_len, n_features))
  x = Conv1D(128, 12, activation='relu')(i)
  x = Dropout(0.2)(x)
  x = MaxPooling1D(pool_size=2)(x)
  x = Conv1D(128, 5, activation='relu')(x)
  x = Dropout(0.2)(x)
  x = MaxPooling1D(pool_size=2)(x)
  x = Conv1D(128, 5, activation='relu')(x)
  x = Dropout(0.2)(x)
  x = MaxPooling1D(pool_size=2)(x)
  x = Bidirectional(LSTM(64, return_sequences=True))(x)
  x = Bidirectional(LSTM(64, return_sequences=True))(x)
  x = Bidirectional(LSTM(64, return_sequences=True))(x)
  x = Bidirectional(LSTM(64, return_sequences=False))(x)
  x = Dropout(0.2)(x)
  # x = Conv1D(training_generator.n_classes, 11, activation='tanh')(x)
  x = Dense(training_generator.n_classes, activation='softmax')(x)

  model = Model(inputs=[i], outputs=[x])
  model.summary()
  model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['categorical_accuracy'])


  model.fit(
    training_generator, 
    epochs=1000, 
    callbacks=[tensorboard_callback,reduce_lr], 
    validation_data=val_generator)

  scores = model.evaluate(val_generator, verbose=1)
  print(scores)


def TempConvN():

  logdir = "logs/fit/tcn" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = TensorBoard(log_dir=logdir)

  n_features = 11
  n_classes = 3
  seq_len = 128

  # Generators
  training_generator = Datagenerator(squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)
  val_generator = Datagenerator(train=False, squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp.shape)
  print(outp.shape)

  i = Input(shape=(training_generator.seq_len, n_features))
  # x = TCN(
  #   nb_filters=seq_len,
  #   kernel_size=12, 
  #   return_sequences=False, 
  #   use_batch_norm=True
  #   )(i)  # The TCN layers are here.

  # x = TCN(
  #   nb_filters=seq_len, 
  #   kernel_size=16, 
  #   # dilations=[1, 2, 4, 8, 16, 32],
  #   # use_skip_connections=True,
  #   return_sequences=False, 
  #   # dropout_rate= 0.2,
  #   # activation="softmax",
  #   use_batch_norm=True
  #   )(i)  # The TCN layers are here.
  # x = Dense(training_generator.n_classes, activation='softmax')(x)

  x = TCN(
    nb_filters=seq_len, 
    kernel_size=2,
    nb_stacks=4,
    dilations=[1, 2, 4, 8,16],
    use_skip_connections=True,
    return_sequences=False, 
    # dropout_rate= 0.2,
    # activation="softmax",
    use_batch_norm=True
    )(i)  # The TCN layers are here.
  x = Dense(training_generator.n_classes, activation='softmax')(x)

  model = Model(inputs=[i], outputs=[x])

  model.summary()

  # try using different optimizers and different optimizer configs
  model.compile('adam', 'categorical_crossentropy', metrics=['categorical_accuracy'])

  model.fit(training_generator, epochs=500, callbacks=[tensorboard_callback], validation_data=val_generator)

  # print(model.predict(val_generator.__getitem__(0)))

  scores = model.evaluate(val_generator, verbose=1, callbacks=[tensorboard_callback])
  print(scores)

def fitness_classifier():

  logdir = "logs/fit/tcn" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = TensorBoard(log_dir=logdir)

  dataArray = np.empty((0,60), dtype=float)
  profileArray = np.empty((0,16), dtype=float)
  scores = np.empty(0, dtype=float)

  for data_fname in glob("data/processed/*_data.npy"):
    # Load file
    name = os.path.basename(data_fname[:-9]) # strip "_data.npy" from fname

    data = np.load(data_fname)
    dataArray = np.append(dataArray, [data], axis=0)

    profile_fname = os.path.dirname(data_fname) + "/" + name + "_profile.npy"
    profile = np.load(profile_fname)
    score = fitness_score(profile, name)
    profileArray = np.append(profileArray, [profile], axis=0)
    scores = np.append(scores, [score], axis=0)
  print(dataArray.shape)
  print(profileArray.shape)

  # i = Input(shape=dataArray.shape[1])
  # x = Dense(dataArray.shape[1], activation='relu')(i)
  # x = Dense(1, kernel_initializer='normal')(x)

  # model = Model(inputs=[i], outputs=[x])

  # model.summary()

  # # try using different optimizers and different optimizer configs
  # model.compile(optimizer='adam', loss='mean_squared_error')

  # model.fit(dataArray[:-3], scores[:-3], epochs=10, callbacks=[tensorboard_callback])

  # print(list(zip(scores,model.predict(dataArray))))

  # scores = model.evaluate(val_generator, verbose=1, callbacks=[tensorboard_callback])
  # print(scores)

def fitness_score(profileArray, name):
  (resting_hr, max_hr, ex1_max_hr, rpe_2, ex2_max_hr, rpe_3, kcal_3, dist_3, rpe_4, kcal_4, dist_4, kcal_5, dist_5, baeke_W, baeke_S, baeke_L) = profileArray

  np.set_printoptions(precision=3)
  np.set_printoptions(suppress=True)

  HR_reserve = max_hr - resting_hr
  baeke_total = (baeke_W+ baeke_S+ baeke_L)/15


  # VO2max is the most important metric but can't be measured
  # instead use Kcal as a substitute 
  # max exertion kcal is the most important metric because it is generated at peak oxygen consumption (5-25)

  # the other kcal metrics aren't proven to correlate (5-60), but use them nonetheless with a modifier to make them less important
  # also use the Heart Rate Reserve usage of the first and second session (0-100) 

  # use the Baecke score as a modifier

  kcal5 = kcal_5 * 2
  kcal_rest = (kcal_3+kcal_4) * baeke_total
  hr1_score = (100-(((ex1_max_hr-resting_hr)/ (max_hr - resting_hr))*100))/2
  hr2_score = (100-(((ex2_max_hr-resting_hr)/ (max_hr - resting_hr))*100))/2
  res = (kcal5 + kcal_rest + hr1_score + hr2_score)

  # print(f"kcal5 {kcal5:.2f}, kcal rest {kcal_rest:.2f}, hr1 score {hr1_score:.2f}, hr2 score {hr2_score:.2f}, baeke_total {baeke_total:.2f}")
  # print(f"hr1 score {hr1_score:.2f}%, hr2 score {hr2_score:.2f}%")
  # print(f"hr_rest {resting_hr:.2f}, hr max {max_hr:.2f}, hr1_max {ex1_max_hr:.2f}, hr2_max {ex2_max_hr:.2f}")
  print(f"{name}: {res:.2f}")
  # print(profileArray)
  # print("==============")

  return res


def main():

  parser = argparse.ArgumentParser(description='Fitness coach.')

  parser.add_argument('-f','--file', const='data/user/userdata.hdf5', nargs='?', help='import user data and model from a file')
  parser.add_argument('-i','--init', default='fromscratch', nargs='?', choices=['fromscratch', 'inactive', 'active', 'elite'], help='initialize user data, either from scratch or a basic fit/unfit user)')

  args = parser.parse_args()
  print(args)

  if args.file:
    u = User.fromfile(fname=args.file)
    print(u)
  else:
    if args.init == 'fromscratch':
      (work_index,sport_index,leisure_index) = baecke()
      u = User(work_index,sport_index,leisure_index)
      print(u)
      u.export_hdf5()
    elif args.init == 'inactive':
      u = User(2.0, 2.0, 1.0)
      print(u)
      u.export_hdf5()
    elif args.init == 'active':
      u = User(2.0, 4.0, 3.0)
      print(u)
      u.export_hdf5()
    elif args.init == 'elite':
      u = User(4.5, 5.0, 4.0)
      print(u)
      u.export_hdf5()

  #print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

  # seq_classification()
  # deepheart()
  TempConvN()
  # fitness_classifier()

if __name__ == "__main__":
  main()

