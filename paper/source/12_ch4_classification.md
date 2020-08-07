
# Activity State Classification \label{ch:data}

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

Using these method, each epoch would result in 


Sequence-to-sequence classification (where each element in a sequence receives a classification, instead of just the full sequence receiving a single classification) was considered, but proved to be too inaccurate to be viable as a solution.


## Long Short Term Memory 

Long short-term memory (LSTM) is a type of Recurrent Neural Network (RNN) that is used to analyse sequence data. A common use-case is connected handwriting recognition and speech recognition. An LSTM consists of multiple cells, each containing a memory cell and gates that make the cell capable of remembering values over arbitrary time intervals. These cells can pass a value to their successor cell (the hidden state), which makes them capable of handling sequences of data. The LSTM itself was proposed as an evolution of the standard RNN to solve the vanishing gradient problem, in which gradients that are back-propagated can explode or implode in size.

The LSTM used has a cell for each beat in the input sequence with 3 hidden states  and will output the hidden states of the very last cell. A densely connect layer containing three neurons, each signifying one of the three output classes is used as the output layer. After training with categorical crossentropy an accuracy rating of XXXXXX \% is reached.

The final layer uses softmax activation and the model is trained using categorical crossentropy using the "adam" optimizer. This combination ius chosen because it is optimized for multi-class labeling.
 

RESULTATEN VAN LSTM HIER

BESPREKING VAN LSTM HIER


## Deep LSTM

As an evolution of a standard LSTM network, a network with three stacked LSTM layers is evaluated. Instead of the LSMT layer returning the hidden states of the last cells, it outputs all the hidden states of all cells. this is then passed to a second LSTM layer which then passes its entire sequence to the third and final LSTM layer. This third layer passes the hidden outputs of its last cell to a dense layer in the same way as the shallow LSTM.


>> A densely connect layer containing three neurons, each signifying one of the three output classes is used as the output layer. After training with categorical crossentropy an accuracy rating of XXXXXX \% is reached.

RESULTATEN VAN DLSTM HIER

BESPREKING VAN DLSTM HIER


## DeepHeart

DeepHeart is a network architecture proposed by [@Ballinger2018] to classify HRV data into 5 categories (normal, diabetes, high blood pressure and sleep apnea). It is designed to give a classification for every timestep (Heartbeat in this case), which makes it a sequence-to-sequence algorithm. The model consists of the following layers:

 - A Convolutional layer with a filter size of 12 followed by a 0.2 dropout and a maxpooling layer with a pool size of 2
 - Two Convolutional layers with a filter size of 5, each followed by a 0.2 dropout and a maxpooling layer with a pool size of 2
 - 4 Bidirectional LSTM layers, which means that each layer consists of 2 LSTM chains, one standard and one that goes backwards in time. This has as benefit that these layers can analyze sequences in the past as well as in the future. Of these four layers the first three output all their hidden states to the following layer and the fourth outputs the hidden state of the last cell
 - Here a slight adaptation is made to the original design. Instead of a "a convolution of filter length 1" with tanh activation, a densely connected layer is used as output for the classification.


RESULTATEN VAN DH HIER

BESPREKING VAN DH HIER


## DeepHeart v 2

DeepHeartV2 is a proposed evolution of deepheart for this thesis with the following changes:

 - The Maxpooling layers are removed because they reduced the sequence lenght to 11 timesteps with 128 features when they were used as input for the LSTM layers.
 - The Convolutional Layers use causal padding, a technique also used in WaveNet [@Oord2016]
 - The Bidirectional LSTMs each have 11 hidden outputs to match the number of features in the input data.


RESULTATEN VAN DH2 HIER

BESPREKING VAN DH2 HIER


## Temporal Convolutional Network

A Temportal Convolution Network (also known as a Causal Convolutional Network) is an adaptation of the wellknown Convolutional Neural Network, where there is no recurrent connection between "cells", but instead the input layer (receiving the sequence timesteps) gets step-wise convoluted down to an output layer. It is important that these convolutions respect the ordering in which the data is modeled.

This network architecture requires either a large amount of layers or a wide filtering at every layer to achieve the large "receptive field" of the input layer. A way to increase this field without significantly increasing computational size is by using "Dilated Causal Convolution". This involves ignoring certain connections between layers based on their location and depth within the network. Visually it can be explained by imagining a tree structure within the layers (fig \ref{DCC}). 

![Dilated Causal Convolution [@Oord2016] \label{DCC}](source/figures/DilutedCuasalCN.png){ width=100% }

In this implementation the keras-tcn package is used, which can stack multiple of these networks together as residual blocks (fig \ref{TCN_blocks}) which means these blocks have the potential to be skipped over. The TCN used in this thesis has a filter size of 2, contains 4 stacks of residual blocks, each containing 5 layers with resp. 1, 2, 4, 8 and 16 dilations. The implementation provides a flag that can be set to only return the outputs of the last timestep, so asking the TCN to model 3 features and using softmax activation results in the classification that we want.

![Residual blocks in the TCN (From the keras-tcn github page) \label{TCN_blocks}](source/figures/TCN_blocks.jpg){ width=100% }

RESULTATEN VAN TCN HIER

BESPREKING VAN TCN HIER


## Labeling methods

As mentioned before in the introduction of this chapter, the method used to assign a class is a parameter in itself. If all beats in the tail of the sequence are the same class, the entire sequence gets assigned this class. If this is not the case, the proposed sequence is instead discarded. This means that some trainable cases in the dataset are not used alltogether. It is however clear that a sufficiently low "checking parameter" will result in a sequenc that is hard to predicte. If the checking parameter is 1/_seq\_len_, the first _seq\_len_-1 can have a different class than the eventual sequence class.

 RESULTATEN VAN TAIL LENGTH HIER

 BESPREKING VAN TAIL LENGTH HIER
