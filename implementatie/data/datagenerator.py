import numpy as np
import keras
import tensorflow
from glob import glob

import random
import math

class DataGenerator(tensorflow.keras.utils.Sequence):
  'Generates data for Keras'
  def __init__(self, train=True, train_test_split=0.8, squash_class=False, batch_size=16, seq_len=64, n_features=11, n_classes=5):
    'Initialization'
    self.train = train
    self.train_test_split = train_test_split
    self.squash_class = squash_class
    self.batch_size = batch_size
    self.seq_len = seq_len
    self.n_features = n_features
    self.n_classes = n_classes
    self.data = self.read_data()

    self.min_class_len = 0
    self.preclassified_data = []

    # 2 sequence lenghts of spare space: one seq_len for the actual sequence and one seql_len for when the offset is equal to seq_len
    self.indexes = [i*self.seq_len for i in range(math.floor(len(self.data) / self.seq_len)-2)]
    self.max_offset = len(self.data) % self.seq_len

    if (self.max_offset == 0):
      self.max_offset = seq_len
      self.indexes = self.indexes[:-1]

    self.current_offset = random.randrange(self.max_offset)

    unique, counts = np.unique(self.data[:,-1], return_counts=True)
    print(dict(zip(unique, counts)))

    self.on_epoch_end()


    print(f"generator length: {self.__len__()} batches of {self.batch_size} sequences with length {self.seq_len} (sample total: {len(self.data)})")

    # if self.squash_class:
    #   (x_temp, y_temp) = self._find_squashed_sample(0, len(self.data))
    #   print(f"input shape: {x_temp.shape}, output shape: {y_temp.shape}")
    # else:
    #   (x_temp, y_temp) = self._find_sample(0, len(self.data))
    #   print(f"input shape: {x_temp.shape}, output shape: {y_temp.shape}")

  def __len__(self):
    'Denotes the number of batches per epoch'

    return math.floor((self.min_class_len*self.n_classes) / self.batch_size)

  def __getitem__(self, index):
    'Generate one batch of data'

    resX = self.preclassified_data[index*self.batch_size:(index+1)*self.batch_size,:, :-1]
    resy = keras.utils.to_categorical(
      self.preclassified_data[index*self.batch_size:(index+1)*self.batch_size,:,-1], 
      num_classes=self.n_classes)

    return resX, resy

  def read_data(self):

    dataArray = np.empty((0,self.n_features+1), dtype=float)

    for npfile in glob("data/processed/*.npy"):

      # Load file
      data = np.load(npfile)
      dataArray = np.append(dataArray, data, axis=0)

    if self.train:
      dataArray = dataArray[:math.floor(len(dataArray)*self.train_test_split)]
    else:
      dataArray = dataArray[math.floor(len(dataArray)*self.train_test_split):]

    return dataArray

  def on_epoch_end(self):
    self.current_offset = random.randrange(self.max_offset)
    np.random.shuffle(self.indexes)

    X = [np.empty((0, self.seq_len, self.n_features+1),dtype=float)] * self.n_classes

    for idx in self.indexes:
      seq_start = idx+self.current_offset
      seq_end = idx+self.current_offset+self.seq_len
      clss = int(self.data[seq_end,-1])

      if np.all(self.data[seq_end-10:seq_end,-1] == clss):
        X[clss] = np.append(X[clss], [self.data[seq_start:seq_end]], axis=0)

    self.min_class_len = len(X[0])

    for li in X:
      if (self.min_class_len > len(li)): self.min_class_len = len(li)

    self.preclassified_data = np.empty((self.n_classes*self.min_class_len, self.seq_len, self.n_features+1))
    for i, li in enumerate(X):
      self.preclassified_data[i*self.min_class_len:(i+1)*self.min_class_len,] = li[:self.min_class_len,:,:]

    np.random.shuffle(self.preclassified_data)
