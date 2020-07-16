import numpy as np
import keras
from glob import glob

import random
import math

class DataGenerator(keras.utils.Sequence):
  'Generates data for Keras'
  def __init__(self, train=True, train_test_split=0.7, squash_category=False, batch_size=32, seq_len=64, n_features=16, n_classes=5, shuffle=True):
    'Initialization'
    self.train = train
    self.train_test_split = train_test_split
    self.squash_category = squash_category
    self.batch_size = batch_size
    self.seq_len = seq_len
    self.n_features = n_features
    self.n_classes = n_classes
    self.data = self.read_data()

    self.indexes = [i*self.seq_len for i in range(math.floor(len(self.data) / self.seq_len))]
    self.max_offset = len(self.data) % self.seq_len
    self.current_offset = 0

    self.on_epoch_end()

    print(f"generator length: {self.__len__()} batches of {self.batch_size} sequences with length {self.seq_len} (sample total: {len(self.data)})")

    # if self.squash_category:
    #   (x_temp, y_temp) = self._find_squashed_sample(0, len(self.data))
    #   print(f"input shape: {x_temp.shape}, output shape: {y_temp.shape}")
    # else:
    #   (x_temp, y_temp) = self._find_sample(0, len(self.data))
    #   print(f"input shape: {x_temp.shape}, output shape: {y_temp.shape}")

  def __len__(self):
    'Denotes the number of batches per epoch'
    return int(np.floor(len(self.indexes) / self.batch_size))

  def __getitem__(self, index):
    'Generate one batch of data'
    X = np.empty((self.batch_size, self.seq_len, self.n_features))

    batch_indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]


    # range_start = 0 if self.train else math.floor(len(self.data)*self.train_test_split)
    # range_end = math.ceil(len(self.data)*self.train_test_split) - self.seq_len if self.train else len(self.data) - self.seq_len

    if self.squash_category:
      y = np.empty((self.batch_size), dtype=int)

      seq_start = data_idx+self.current_offset
      seq_end = data_idx+self.current_offset+self.seq_len

      X = self.data[seq_start:seq_end,:-1]
      y = self.data[seq_start,-1]

      return X, keras.utils.to_categorical(y, num_classes=self.n_classes)
    else:
      y = np.empty((self.batch_size, self.seq_len, self.n_classes), dtype=int)

      for i, data_idx in enumerate(batch_indexes):

        seq_start = data_idx+self.current_offset
        seq_end = data_idx+self.current_offset+self.seq_len

        X[i,] = self.data[seq_start:seq_end,:-1]
        y[i,] = keras.utils.to_categorical(self.data[seq_start:seq_end,-1], num_classes=self.n_classes)

    return X, y

  # def _find_sample(self, batch_indexes):
  #   idx = random.randrange(range_start, range_end)
  #   x_temp = self.data[idx:idx+self.seq_len]
  #   y_temp = self.data[idx:idx+self.seq_len,-1]

  #   for i in batch_indexes:


  #   return (x_temp[:,:-1], keras.utils.to_categorical(y_temp, num_classes=self.n_classes))

  # def _find_squashed_sample(self, range_start, range_end):
  #   idx = random.randrange(range_start, range_end)
  #   x_temp = self.data[idx:idx+self.seq_len]
  #   y_temp = self.data[idx,-1]

  #   while not np.all(x_temp[:,-1] == y_temp):
  #     idx = random.randrange(range_start, range_end)
  #     x_temp = self.data[idx:idx+self.seq_len]
  #     y_temp = self.data[idx,-1]

  #   return (x_temp[:,:-1], keras.utils.to_categorical(y_temp, num_classes=self.n_classes))

  def read_data(self):

    dataArray = np.empty((0,self.n_features+1), dtype=float)

    for npfile in glob("data/processed/*.npy"):

      # Load file
      data = np.load(npfile)
      dataArray = np.append(dataArray, data, axis=0)

    return dataArray

  def on_epoch_end(self):
    self.current_offset = random.randrange(self.max_offset)
    np.random.shuffle(self.indexes)
