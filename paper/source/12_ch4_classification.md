
# Data Gathering \label{ch:data}

For the activity state classification task, the proposals stem from either Natural Language Processing or from earlier experimentations involving Machine learning and Heart Rate data. The raw input data of all users are concatenated, resulting in 95.000 datapoints. Indexes spaced evenly apart based on the desirec sequence lenght are generated, and a random offset is generated based on the lenght of the remaining beats that don't fit inside a sequence. 

For each epoch an attempt is made to assign a class to all these sequences. If all beats in the tail of the sequence are the same class, the entire sequence gets assigned this class. The lenght of this tail is a parameter that is explored later in the chapter, but the default case is a tail lenght of half the sequence length.

```python
if np.all(data[seq_end-(seq_len/2):seq_end,-1] == clss):
 	X[clss] = np.append(X[clss], [data[seq_start:seq_end,:-1]])

```


After these classes are determined, an equal amount of sequences for each class is bundled as the data for that epoch. After each epoch the indexes are reshuffled and the offset is regenerated, so that each epoch will see slightly different sequences in a different order.


```python
# 2 sequence lenghts of spare space: one seq_len for the actual sequence and one seql_len for when the offset is equal to seq_len
indexes = [i*seq_len for i in range(math.floor(len(data) / seq_len)-1)]
max_offset = len(data) % seq_len

if (max_offset == 0):
  max_offset = seq_len
  indexes = indexes[:-1]

current_offset = random.randrange(max_offset)
```

Sequence-to-sequence classification (where each element in a sequence receives a classification, instead of just the full sequence receiving a single classification) was considered, but proved to be too inaccurate to consider as a solution.


## Long Short Term Memory 

Long short-term memory (LSTM) is a type of Recurrent Neural Network (RNN) that is used to analyse sequence data. A common use-case is connected handwriting recognition and speech recognition. An LSTM consists of multiple cells, each containing a memory cell and gates that make the cell capable of remembering values over arbitrary time intervals. The LSTM itself was proposed as an evolution of the standard RNN to solve the vanishing gradient problem, in which gradients that are back-propagated can explode or implode in size.

The LSTM used has a cell for each beat in the input sequence, and a densely connect output layer containing three neurons, each signifying one of the three output classes. After training with categorical crossentropy an accuracy rating of XXXXXX \% is reached.


## Deep LSTM

## DeepHeart

## Temporal Convolutional Network



## Labeling methods

At first the sequences get assigned the