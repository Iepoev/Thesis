
import argparse
import datetime
import keras
import numpy as np
import tensorflow as tf
import math

from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input, Embedding, Dropout, MaxPooling1D, MaxPooling2D, Bidirectional, Conv1D, Conv2D
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.callbacks import TensorBoard, ReduceLROnPlateau

from sklearn.metrics import classification_report
from tcn import TCN, tcn_full_summary


from src.user import User
from src.baecke import baecke
from data.hr_classifier_datagenerator import HR_Classifier_DataGenerator

def seq_to_seq_classification():

  logdir = "logs/fit/seq_to_seq_classification" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = TensorBoard(log_dir=logdir)


  # Generators
  training_generator = HR_Classifier_DataGenerator()
  val_generator = HR_Classifier_DataGenerator(train=False)

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
  training_generator = HR_Classifier_DataGenerator(squash_class=True, n_features=n_features, n_classes=n_classes)
  val_generator = HR_Classifier_DataGenerator(train=False, squash_class=True, n_features=n_features, n_classes=n_classes)

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
  training_generator = HR_Classifier_DataGenerator(squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)
  val_generator = HR_Classifier_DataGenerator(train=False, squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)

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
  training_generator = HR_Classifier_DataGenerator(squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)
  val_generator = HR_Classifier_DataGenerator(train=False, squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)

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
  deepheart()
  # TempConvN()

if __name__ == "__main__":
  main()

