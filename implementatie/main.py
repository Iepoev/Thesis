
import argparse
import datetime
import keras
import numpy as np
import tensorflow as tf

from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input, Embedding, Dropout, MaxPooling1D, Bidirectional, Conv1D
from tensorflow.keras.preprocessing import sequence

from sklearn.metrics import classification_report
from tcn import TCN, tcn_full_summary


from src.user import User
from src.baecke import baecke
from data.datagenerator import DataGenerator

def seq_to_seq_classification():

  logdir = "logs/fit/seq_to_seq_classification" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)


  # Generators
  training_generator = DataGenerator()
  test_generator = DataGenerator(train=False)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp[31][0])
  print(outp.shape)

  # LSTM for sequence classification 
  model = Sequential()
  model.add(LSTM(32,return_sequences=True, input_shape=(training_generator.seq_len,16)))
  model.add(LSTM(5,return_sequences=True, input_shape=(training_generator.seq_len,16)))
  # model.add(Dense(training_generator.n_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  print(model.summary())
  model.fit(training_generator, epochs=300,callbacks=[tensorboard_callback])

  scores = model.evaluate(test_generator, verbose=1)
  print(scores)
  print("Accuracy: %.2f%%" % (scores[1]*100))

def seq_classification():
  logdir = "logs/fit/seq_classification" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

  n_features = 11
  n_classes = 3

  # Generators
  training_generator = DataGenerator(squash_class=True, n_features=n_features, n_classes=n_classes)
  test_generator = DataGenerator(train=False, squash_class=True, n_features=n_features, n_classes=n_classes)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp.shape)
  print(outp.shape)
  # print(outp)
  # print(training_generator.n_classes)

  # LSTM for sequence classification 
  model = Sequential()
  model.add(Dense(training_generator.seq_len, activation='sigmoid', input_shape=(training_generator.seq_len,n_features)))
  model.add(LSTM(training_generator.seq_len,return_sequences=True))
  model.add(LSTM(16,return_sequences=True))
  model.add(LSTM(16))
  model.add(Dense(training_generator.n_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  print(model.summary())
  model.fit(training_generator, epochs=20,callbacks=[tensorboard_callback])

  scores = model.evaluate(test_generator, verbose=1)


# Ballinger2018
def deepheart():
  logdir = "logs/fit/deepheart" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

  n_features = 11
  n_classes = 3
  seq_len = 64

  # Generators
  training_generator = DataGenerator(squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)
  test_generator = DataGenerator(train=False, squash_class=True, n_features=n_features, seq_len=seq_len, n_classes=n_classes)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp.shape)
  print(outp.shape)

  i = Input(shape=(training_generator.seq_len, n_features))
  x = TCN(return_sequences=True, kernel_size=12, nb_filters=seq_len,use_batch_norm=True)(i)  # The TCN layers are here.
  x = Dropout(0.2)(x)
  # x = MaxPooling1D(pool_size=2)(x)
  # x = TCN(return_sequences=True, kernel_size=5, nb_filters=seq_len,use_batch_norm=True)(x)  # The TCN layers are here.
  # x = Dropout(0.2)(x)
  # x = MaxPooling1D(pool_size=2)(x)
  # x = TCN(return_sequences=True, kernel_size=5, nb_filters=seq_len,use_batch_norm=True)(x)  # The TCN layers are here.
  # x = Dropout(0.2)(x)
  # x = MaxPooling1D(pool_size=2)(x)
  # x = Bidirectional(LSTM(seq_len, return_sequences=True))(x)
  # x = Bidirectional(LSTM(seq_len, return_sequences=True))(x)
  # x = Bidirectional(LSTM(seq_len, return_sequences=True))(x)
  # x = Bidirectional(LSTM(seq_len, return_sequences=False))(x)
  x = Dropout(0.2)(x)
  # x = Conv1D(filters=training_generator.n_classes, kernel_size=seq_len, activation='tanh')(x)
  # x = Dense(training_generator.n_classes, activation='softmax')(i)
  x = Dense(training_generator.n_classes, activation='softmax')(x)

  model = Model(inputs=[i], outputs=[x])

  model.summary()

  # try using different optimizers and different optimizer configs
  model.compile('adam', 'categorical_crossentropy', metrics=['accuracy'])

  model.fit(training_generator, epochs=20, callbacks=[tensorboard_callback])

  # print(model.predict(test_generator.__getitem__(0)))

  scores = model.evaluate(test_generator, verbose=1)
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

  #seq_classification()
  deepheart()

if __name__ == "__main__":
  main()

