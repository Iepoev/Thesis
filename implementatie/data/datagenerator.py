import numpy as np
import keras
from glob import glob

import random
import math

class DataGenerator(keras.utils.Sequence):
  'Generates data for Keras'
  def __init__(self,train=True, train_test_split=0.7, batch_size=128, seq_len=128, n_parameters=16, n_classes=7, shuffle=True):
    'Initialization'
    self.train = train
    self.train_test_split = train_test_split
    self.batch_size = batch_size
    self.seq_len = seq_len
    self.n_parameters = n_parameters
    self.n_classes = n_classes
    self.data = self.read_data()
    # self.on_epoch_end()


  def __len__(self):
    'Denotes the number of batches per epoch'
    return int(np.floor(len(self.data) / self.batch_size))

  def __getitem__(self, index):
    'Generate one batch of data'
    X = np.empty((self.batch_size, self.seq_len, self.n_parameters))
    y = np.empty((self.batch_size), dtype=int)

    range_start = 0 if self.train else math.floor(len(self.data)*self.train_test_split)
    range_end = math.ceil(len(self.data)*self.train_test_split) - self.seq_len if self.train else len(self.data) - self.seq_len
    # Generate data
    for i in range(self.batch_size):
      idx = random.randrange(range_start, range_end)
      x_temp = self.data[idx:idx+self.seq_len]
      y_temp = self.data[idx,-1]

      while not np.all(x_temp[:,-1] == y_temp):
        idx = random.randrange(range_start, range_end)
        x_temp = self.data[idx:idx+self.seq_len]
        y_temp = self.data[idx,-1]

      if not self.train:
        print(idx)
      # Store sample
      X[i,] = x_temp[:,:-1]

      # Store class
      y[i] = y_temp

    return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

  def read_data(self):

    dataArray = np.empty((0,self.n_parameters+1), dtype=float)

    for npfile in glob("data/processed/*.npy"):

      # Load file
      data = np.load(npfile)
      dataArray = np.append(dataArray, data, axis=0)

    return dataArray