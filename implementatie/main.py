
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


def lstm():
  logdir = "logs/fit/lstm" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tboard = TensorBoard(log_dir=logdir)

  # Generators
  t_gen = Datagenerator(squash_class=True)
  v_gen = Datagenerator(train=False, squash_class=True)

  i = Input(shape=(t_gen.seq_len, t_gen.n_features))
  x = LSTM(t_gen.n_features)(i)
  x = Dense(t_gen.n_classes, activation='softmax')(x)

  train_model(i, x, t_gen, v_gen, tboard, learn_rate=0.001)


def deep_lstm():
  logdir = "logs/fit/deep_lstm" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tboard = TensorBoard(log_dir=logdir)

  # Generators
  t_gen = Datagenerator(squash_class=True)
  v_gen = Datagenerator(train=False, squash_class=True)

  i = Input(shape=(t_gen.seq_len, t_gen.n_features))
  x = LSTM(t_gen.n_features,return_sequences=True)(i)
  x = LSTM(t_gen.n_features,return_sequences=True)(x)
  x = LSTM(t_gen.n_features)(x)
  x = Dense(t_gen.n_classes, activation='softmax')(x)

  train_model(i, x, t_gen, v_gen, tboard, learn_rate=0.001)


# Ballinger2018
def deepheart():
  logdir = "logs/fit/deepheart" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tboard = TensorBoard(log_dir=logdir)

  # Generators
  t_gen = Datagenerator(squash_class=True)
  v_gen = Datagenerator(train=False, squash_class=True)

  i = Input(shape=(t_gen.seq_len, t_gen.n_features))
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
  # x = Conv1D(3, 11, activation='tanh')(x)
  x = Dense(t_gen.n_classes, activation='softmax')(x)

  train_model(i, x, t_gen, v_gen, tboard, learn_rate=0.001, factor=0.7)


# Ballinger2018
def deepheartv2():
  logdir = "logs/fit/deepheartv2" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tboard = TensorBoard(log_dir=logdir)

  # Generators
  t_gen = Datagenerator(squash_class=True)
  v_gen = Datagenerator(train=False, squash_class=True)

  i = Input(shape=(t_gen.seq_len, t_gen.n_features))
  x = Bidirectional(LSTM(t_gen.n_features, return_sequences=True))(i)
  x = Bidirectional(LSTM(t_gen.n_features, return_sequences=True))(x)
  x = Bidirectional(LSTM(t_gen.n_features, return_sequences=True))(x)
  x = Bidirectional(LSTM(t_gen.n_features, return_sequences=True))(x)
  x = Dropout(0.2)(x)
  x = Conv1D(128, 12, activation='relu', padding="causal")(x)
  x = Dropout(0.2)(x)
  x = MaxPooling1D(pool_size=2)(x)
  x = Conv1D(128, 5, activation='relu', padding="causal")(x)
  x = Dropout(0.2)(x)
  x = MaxPooling1D(pool_size=2)(x)
  x = Conv1D(128, 5, activation='relu', padding="causal")(x)
  x = Dropout(0.2)(x)
  x = MaxPooling1D(pool_size=2)(x)
  x = Bidirectional(LSTM(t_gen.n_features, return_sequences=False))(x)
  # x = Conv1D(training_generator.n_classes, 11, activation='tanh')(x)
  x = Dense(t_gen.n_classes, activation='softmax')(x)

  train_model(i, x, t_gen, v_gen, tboard, learn_rate=0.001, factor=0.7)


def TempConvN():

  logdir = "logs/fit/tcn" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tboard = TensorBoard(log_dir=logdir)

  # Generators
  t_gen = Datagenerator(squash_class=True)
  v_gen = Datagenerator(train=False, squash_class=True)

  i = Input(shape=(t_gen.seq_len, t_gen.n_features))

  # x = TCN(
  #   nb_filters=t_gen.seq_len,
  #   kernel_size=12, 
  #   return_sequences=False, 
  #   use_batch_norm=True
  #   )(i)  # The TCN layers are here.

  # x = TCN(
  #   nb_filters=t_gen.seq_len, 
  #   kernel_size=16, 
  #   # dilations=[1, 2, 4, 8, 16, 32],
  #   # use_skip_connections=True,
  #   return_sequences=False, 
  #   # dropout_rate= 0.2,
  #   # activation="softmax",
  #   use_batch_norm=True
  #   )(i)  # The TCN layers are here.
  # x = Dense(t_gen.n_classes, activation='softmax')(x)


  x = TCN(
    nb_filters=t_gen.seq_len, 
    kernel_size=2,
    nb_stacks=4,
    dilations=[1, 2, 4, 8, 16],
    use_skip_connections=True,
    return_sequences=False, 
    # dropout_rate= 0.2,
    # activation="softmax",
    use_batch_norm=True
    )(i)  # The TCN layers are here.
  x = Dense(t_gen.n_classes, activation='softmax')(x)


  # x = TCN(
  #   nb_filters=t_gen.n_classes, 
  #   kernel_size=2,
  #   nb_stacks=4,
  #   dilations=[1, 2, 4, 8, 16, 32],
  #   use_skip_connections=True,
  #   return_sequences=False, 
  #   # dropout_rate= 0.2,
  #   # activation="softmax",
  #   use_batch_norm=True
  #   )(i)  # The TCN layers are here.
  # x = Dense(t_gen.n_classes, activation='softmax')(x)

  train_model(i, x, t_gen, v_gen, tboard, learn_rate=0.0001)

def train_model(inputs, outputs, training_generator, val_generator, tensorboard_callback,
  learn_rate=0.01, epochs=500, factor=0.1):

  opt = tf.keras.optimizers.Adam(learning_rate=learn_rate)
  reduce_lr = ReduceLROnPlateau(monitor='categorical_accuracy', factor=factor,
                              patience=50, min_lr=0.0000001, min_delta=0.0001)


  model = Model(inputs=[inputs], outputs=[outputs])
  model.summary()
  model.compile(
    loss='categorical_crossentropy', 
    optimizer=opt, 
    metrics=['categorical_accuracy'])
  model.fit(
    training_generator, 
    epochs=epochs, 
    callbacks=[tensorboard_callback, reduce_lr], 
    validation_data=val_generator)

  scores = model.evaluate(val_generator, verbose=1)


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

def main():

  #print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

  # lstm()
  # deep_lstm()
  # deepheart()
  # deepheartv2()
  # TempConvN()
  TempConvN()
  TempConvN()
  deepheartv2()
  deepheartv2()
  deepheartv2()
  # fitness_classifier()

if __name__ == "__main__":
  main()


