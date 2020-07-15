
import argparse
import numpy

import tensorflow as tf

from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence

from src.user import User
from src.baecke import baecke
from data.datagenerator import DataGenerator

def tensorflow():

  train_test_split = 0.7

  # Generators
  training_generator = DataGenerator(train_test_split=train_test_split)
  validation_generator = DataGenerator(train=False, train_test_split=train_test_split)


  # LSTM for sequence classification in the IMDB dataset

  # # fix random seed for reproducibility
  # numpy.random.seed(7)
  # # load the dataset but only keep the top n words, zero the rest
  # top_words = 5000
  # (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=top_words)
  # # truncate and pad input sequences
  # max_review_length = 500
  # X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
  # X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)
  # # create the model
  # print(X_train[:50])
  # print(y_train[:50])
  # embedding_vecor_length = 32

  model = Sequential()
  model.add(LSTM(64,return_sequences=True))
  model.add(LSTM(64))
  model.add(Dense(1, activation='sigmoid'))
  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  model.fit(training_generator, epochs=2, batch_size=128)
  print(model.summary())
  # Final evaluation of the model
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

