import numpy as np
import keras
from glob import glob

import random
import math

class DataGenerator(keras.utils.Sequence):
  'Generates data for Keras'
  def __init__(self, train=True, train_test_split=0.7, squash_category=False, batch_size=128, seq_len=128, n_features=16, n_classes=5, shuffle=True):
    'Initialization'
    self.train = train
    self.train_test_split = train_test_split
    self.squash_category = squash_category
    self.batch_size = batch_size
    self.seq_len = seq_len
    self.n_features = n_features
    self.n_classes = n_classes
    self.data = self.read_data()
    # self.on_epoch_end()

    print(f"generator length: {self.__len__()} batches of {self.batch_size} sequences with length {self.seq_len} (sample total: {len(self.data)})")

    if self.squash_category:
      (x_temp, y_temp) = self._find_squashed_sample(0, len(self.data))
      print(f"input shape: {x_temp.shape}, output shape: {y_temp.shape}")
    else:
      (x_temp, y_temp) = self._find_sample(0, len(self.data))
      print(f"input shape: {x_temp.shape}, output shape: {y_temp.shape}")

  def __len__(self):
    'Denotes the number of batches per epoch'
    return int(np.floor(len(self.data) / self.batch_size))

  def __getitem__(self, index):
    'Generate one batch of data'
    X = np.empty((self.batch_size, self.seq_len, self.n_features))

    y = np.empty((self.batch_size), dtype=int) if self.squash_category else np.empty((self.batch_size, self.seq_len, self.n_classes), dtype=int)

    range_start = 0 if self.train else math.floor(len(self.data)*self.train_test_split)
    range_end = math.ceil(len(self.data)*self.train_test_split) - self.seq_len if self.train else len(self.data) - self.seq_len

    if self.squash_category:
      return self._find_squashed_sample(range_start, range_end)
    else:
      for i in range(self.batch_size):
        (x_temp, y_temp) = self._find_sample(range_start, range_end)

        X[i,] = x_temp
        y[i,] = y_temp

    return X, y

  def _find_sample(self, range_start, range_end):
    idx = random.randrange(range_start, range_end)
    x_temp = self.data[idx:idx+self.seq_len]
    y_temp = self.data[idx:idx+self.seq_len,-1]

    return (x_temp[:,:-1], keras.utils.to_categorical(y_temp, num_classes=self.n_classes))

  def _find_squashed_sample(self, range_start, range_end):
    idx = random.randrange(range_start, range_end)
    x_temp = self.data[idx:idx+self.seq_len]
    y_temp = self.data[idx,-1]

    while not np.all(x_temp[:,-1] == y_temp):
      idx = random.randrange(range_start, range_end)
      x_temp = self.data[idx:idx+self.seq_len]
      y_temp = self.data[idx,-1]

    return (x_temp[:,:-1], keras.utils.to_categorical(y_temp, num_classes=self.n_classes))

  def read_data(self):

    dataArray = np.empty((0,self.n_features+1), dtype=float)

    for npfile in glob("data/processed/*.npy"):

      # Load file
      data = np.load(npfile)
      dataArray = np.append(dataArray, data, axis=0)

    return dataArray
