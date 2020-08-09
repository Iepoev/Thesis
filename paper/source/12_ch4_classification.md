
# Activity State Classification \label{ch:data}

For the activity state classification task, the proposals stem from either natural language processing or from earlier experimentations involving machine learning and heart rate data. The raw input data of all users are concatenated, resulting in 95.000 datapoints. Indexes spaced evenly apart based on the desirec sequence length are generated, and a random offset is generated based on the length of the remaining beats that don't fit inside a sequence. 

For each epoch an attempt is made to assign a class to all these sequences. If all beats in the tail of the sequence are the same class, the entire sequence gets assigned this class. The length of this tail is a parameter that is explored later in the chapter, but the default case is a tail length of half the sequence length.

```python
if np.all(data[seq_end-(seq_len/2):seq_end,-1] == clss):
 	X[clss] = np.append(X[clss], [data[seq_start:seq_end,:-1]])

```

After these classes are determined, an equal amount of sequences for each class is bundled as the data for that epoch. After each epoch the indexes are reshuffled and the offset is regenerated, so that each epoch will see slightly different sequences in a different order.


```python
# 2 sequence lengths of spare space: 
# one seq_len for the actual sequence and 
# one seql_len for when the offset is equal to seq_len
indexes = [i*seq_len for i in range(math.floor(len(data) / seq_len)-1)]
max_offset = len(data) % seq_len

if max_offset == 0:
  max_offset = seq_len
  indexes = indexes[:-1]

current_offset = random.randrange(max_offset)
```

Using this method, each epoch would result in approximately 30 batches, each containing 9 sequences of 128 timesteps. Batch size is chosen as a multiple of the amount of classes so that the total amount of sequences is divisible by batch size. All the following networks use some form of softmax activation in their final layer and are trained with the "adam" optimizer using categorical cross entropy as the loss function. This combination is chosen because it is optimized for multi-class labeling problems.

Another optimisation made is to dampen the learning rate once the network is reaching an equilibrium. Due to the relatively small dataset the accuracy can vary wildly from epoch to epoch. By lowering the learning rate towards the end of the training run, a more consistent final result is achieved.

Each network is trained three times using the same settings and the result is averaged out, but in almost all cases the result of training fell within a margin of error.

## Long Short Term Memory 

Long short-term memory (LSTM) is a type of recurrent neural network (RNN) that is used to analyse sequence data. A common use-case is connected handwriting recognition and speech recognition. An LSTM consists of multiple cells, each containing a memory cell and gates that make the cell capable of remembering values over arbitrary time intervals. These cells can pass a value to their successor cell (the hidden state), which makes them capable of handling sequences of data. The LSTM itself was proposed as an evolution of the standard RNN to solve the vanishing gradient problem, in which gradients that are back-propagated can explode or implode in size.

The LSTM used has a cell for each beat in the input sequence, each with 11 hidden states (one for each feature). This layer outputs the hidden states of the very last cell. A densely connect layer containing three neurons, each signifying one of the three output classes is used as the output layer.

This network manages to achieve some correct labeling with an accuracy of \~58\% on the validation set. A completely random labeler would correctly label 33\% of sequences, so LSTM is better but still far from ideal.

<!-- \~60\% on the training set and -->

## Deep LSTM

As an evolution of a standard LSTM network, a network with three stacked LSTM layers is evaluated. Instead of the LSTM layer returning the hidden states of the last cells, it outputs all the hidden states of all cells. This is then passed to a second LSTM layer which then passes all of its hidden states to the third and final LSTM layer. This third layer passes the hidden outputs of its very last cell to a dense layer in the same way as the shallow LSTM. This results in a network containing 3072 trainable parameters. The networks achieves a \~65\% on the validation set, which is marginally better than a simple LSTM.

<!-- \~63\% accuracy on the training set and  -->

## DeepHeart

DeepHeart is a network architecture proposed by [@Ballinger2018] to classify HRV data into 5 categories (normal, diabetes, high blood pressure and sleep apnea). It is designed to give a classification for every timestep (Heartbeat in this case), which makes it a sequence-to-sequence algorithm. The model consists of the following layers:

 - A Convolutional layer with a filter size of 12, followed by a 0.2 dropout and a maxpooling layer with a pool size of 2
 - Two Convolutional layers with a filter size of 5, each followed by a 0.2 dropout and a maxpooling layer with a pool size of 2
 - 4 Bidirectional LSTM layers, which means that each layer consists of 2 LSTM chains, one standard and one that goes backwards in time. This has as benefit that these layers can analyze sequences in the past as well as in the future. Of these four layers the first three output all their hidden states to the following layer and the fourth outputs the hidden state of the last cell
 - Here a slight adaptation is made to the original design. Instead of a "convolution of filter length 1" with tanh activation, a densely connected layer is used as output for the classification, to make the network more suitable to multilabel classification for disjunct classes.

This results in a network containing 576.771 trainable parameters. The network achieves only a \~62\% on the validation set, which makes it perform on the same level as the fairly simple and computationally less intensive simple LSTM network.

<!-- \~60\% accuracy on the training set and -->

## DeepHeart v2

DeepHeartV2 is a proposed evolution of DeepHeart for this thesis with the following changes:

 - In the original DeepHeart, the sequences are convoluted before being passed to multiple layers of RNNs. This has a significant impact on the productivity of the LSTM layers as much of the temporal information is filtered out before it reaches the memory cells of the LSTM. In the original model there were only 11 timesteps left in these layers. In this version of DeepHeart, the 4 stacked LSTM layers are swapped with the 9 layers of the convolutional network.
 - The Convolutional Layers use causal padding, a technique also used in WaveNet [@Oord2016]
 - A final LSTM is added before the densely connected output layer.
 - The Bidirectional LSTMs each have 11 hidden outputs to match the number of features in the input data.

This results in a network containing 221.405 trainable parameters. The network achieves a \~75\% on the validation set, which makes it perform significantly better than the original DeepHeart.

<!-- \~80\% accuracy on the training set and -->

## Temporal Convolutional Network

A Temportal Convolution Network (also known as a Causal Convolutional Network) is an adaptation of the wellknown Convolutional Neural Network, where there is no recurrent connection between "cells", but instead the input layer (receiving the sequence timesteps) gets step-wise convoluted down to an output layer. It is important that these convolutions respect the ordering in which the data is modeled.

This network architecture requires either a large amount of layers or a wide filtering at every layer to achieve the large "receptive field" of the input layer. A way to increase this field without significantly increasing computational size is by using "Dilated Causal Convolution". This involves ignoring certain connections between layers based on their location and depth within the network. Visually it can be explained by imagining a tree structure within the layers (fig \ref{DCC}). 

![Dilated Causal Convolution [@Oord2016] \label{DCC}](source/figures/DilutedCuasalCN.png){ width=100% }

In this implementation the keras-tcn package is used, which can stack multiple of these networks together as residual blocks (fig \ref{TCN_blocks}) which means these blocks have the potential to be skipped over. The TCN used in this thesis has a filter size of 2, contains 4 stacks of residual blocks, each containing 5 layers with resp. 1, 2, 4, 8 and 16 dilations. This layer outputs the states of its 128 timesteps to the densely connected layer containing 3 neurons, using softmax activation results in the classification that we want.

![Residual blocks in the TCN (From the keras-tcn github page) \label{TCN_blocks}](source/figures/TCN_blocks.jpg){ width=100% }

This results in a network containing 1.308.291 trainable parameters which makes it the most complex model by a wide margin. The network achieves a \~85\% on the validation set, which makes it perform the best out of all models tested thus far.

<!-- \~80\% accuracy on the training set -->

## Labeling methods

As mentioned before in the introduction of this chapter, the method used to assign a class is a parameter in itself. If all beats in the tail of the sequence are the same class, the entire sequence gets assigned this class. If this is not the case, the proposed sequence is instead discarded, this means that entire sections in the dataset are not used altogether. Decreasing this tail length would increase the dataset because fewer sequences are discarded.

It is however clear that a sufficiently low "checking parameter" will result in a sequence that is hard to predict. If the checking parameter is 1/_seq\_len_, the first _seq\_len_-1 can have a different class than the eventual sequence class.

The impact of this parameter is explored by training the 2 best performing models (DeepHeartV2 and TCN) on various tail lengths (TL).


Model          TL 50%      TL 25%         TL 10%       TL 5%
-----          ------      ------         ------       -----
DeepHeart V2   75%         70%            69%          66%
TCN            85%         82%            81%          80%


Table: The resulting accuracy of decreasing classification tail length. \label{Taillength}

Only a mild accuracy drop is observed in the TCN, while DeepHeartV2 shows a larger drop. What is apparent is that the accuracy drop is manageable, especially after further investigation showed that it became harder for the model to achieve an optimal result. Some training runs showed nearly identical performance with TL 5% as with TL 50%, but the lower the TL paramater the lower the amount of training sessions that achieved this accuracy, dragging the average result down. Training data size increased from approx. 30 batches per epoch for 50% TL to approx 35 batches per epoch for 5% TL, which is only a slight increase.


## Seq2Seq Classification

Sequence-to-sequence classification (where each element in a sequence receives a classification, instead of just the full sequence receiving a single classification) was considered, but proved to be too inaccurate to be viable as a solution.