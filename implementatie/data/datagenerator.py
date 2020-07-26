import numpy as np
import keras
import tensorflow
from glob import glob

import random
import math

class DataGenerator(tensorflow.keras.utils.Sequence):
  'Generates data for Keras'
  def __init__(self, train=True, train_test_split=0.8, squash_class=False, batch_size=8, seq_len=64, n_features=11, n_classes=5):
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
    self.preclassified_X = []
    self.preclassified_y = []

    # 2 sequence lenghts of spare space: one seq_len for the actual sequence and one seql_len for when the offset is equal to seq_len
    self.indexes = [i*self.seq_len for i in range(math.floor(len(self.data) / self.seq_len)-2)]
    self.max_offset = len(self.data) % self.seq_len

    if (self.max_offset == 0):
      self.max_offset = seq_len
      self.indexes = self.indexes[:-1]

    self.current_offset = random.randrange(self.max_offset)

    unique, counts = np.unique(self.data[:,-1], return_counts=True)
    print(f"class counts of beats: {dict(zip(unique, counts))}")

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

    resX = self.preclassified_X[index*self.batch_size:(index+1)*self.batch_size]
    resy = self.preclassified_y[index*self.batch_size:(index+1)*self.batch_size]

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

    # generate a new offset so each sequence is kinda unique
    self.current_offset = random.randrange(self.max_offset)
    # shuffle the base set of indexes
    np.random.shuffle(self.indexes)

    # for each class, create a numpy array and store it in a python list
    X = [np.empty((0, self.seq_len, self.n_features),dtype=float)] * self.n_classes

    # for each base index, pick the sequence that starts at (that index plus the offset)
    for idx in self.indexes:
      seq_start = idx+self.current_offset
      seq_end = idx+self.current_offset+self.seq_len
      clss = int(self.data[seq_end,-1])

      # only use sequences of which the latter half is constant
      if np.all(self.data[seq_end-(math.floor(self.seq_len/2)):seq_end,-1] == clss):
        # append the sequence to its respective class array
        X[clss] = np.append(X[clss], [self.data[seq_start:seq_end,:-1]], axis=0)


    cls_count = ""
    for i, li in enumerate(X):
      cls_count = cls_count + f"{i}: {len(li)}, "

    print(f"class counts of sequences: {cls_count}")


    # balance the data: every class should have the same amount of occurrences per epoch

    # determine the lowest amount of occurences accross all classes
    self.min_class_len = len(X[0])
    for li in X:
      if (self.min_class_len > len(li)): self.min_class_len = len(li)

    # for each class, create
    self.preclassified_X = np.empty((self.n_classes*self.min_class_len, self.seq_len, self.n_features))
    self.preclassified_y = np.empty((self.n_classes*self.min_class_len, self.n_classes))

    # one class at a time, pick the first $min_class_len of that class and put them (and their class) in the 
    # preclassified X and y lists.
    for i, li in enumerate(X):
      self.preclassified_X[i*self.min_class_len:(i+1)*self.min_class_len,] = li[:self.min_class_len]
      self.preclassified_y[i*self.min_class_len:(i+1)*self.min_class_len] = keras.utils.to_categorical(i, num_classes=self.n_classes)

    # shuffle both lists in the same way so every epoch has a non-chronological sequences
    assert len(self.preclassified_X) == len(self.preclassified_y)
    p = np.random.permutation(len(self.preclassified_X))
    self.preclassified_X = self.preclassified_X[p]
    self.preclassified_y = self.preclassified_y[p]
