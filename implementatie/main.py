
import argparse
import keras
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import numpy as np
from sklearn.metrics import classification_report
import tensorflow as tf

import datetime

from src.user import User
from src.baecke import baecke
from data.datagenerator import DataGenerator

def tensorflow():

  logdir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)


  train_test_split = 0.7

  # Generators
  training_generator = DataGenerator(train_test_split=train_test_split)
  validation_generator = DataGenerator(train=False, train_test_split=train_test_split, batch_size=128)

  (inp, outp) = training_generator.__getitem__(0)
  print(inp.shape)
  print(outp.shape)


  # LSTM for sequence classification 
  model = Sequential()
  model.add(LSTM(32,return_sequences=True, input_shape=(training_generator.seq_len,16)))
  model.add(LSTM(5,return_sequences=True, input_shape=(training_generator.seq_len,16)))
  # model.add(Dense(training_generator.n_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  print(model.summary())
  model.fit(training_generator, epochs=100,callbacks=[tensorboard_callback])

  # (X_eval, y_true) = validation_generator.__getitem__(0)

  # y_true = np.argmax(y_true, axis=1) # Convert one-hot to index
  # y_pred = np.argmax(model.predict(X_eval), axis=1)

  # print(y_pred)

  # print(classification_report(y_true, y_pred))

  scores = model.evaluate(validation_generator, verbose=1)
  print(scores)
  print("Accuracy: %.2f%%" % (scores[1]*100))


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


  tensorflow()

if __name__ == "__main__":
  main()

