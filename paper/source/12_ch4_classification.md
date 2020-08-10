
# Implementation

## Activity State Classification \label{ch:classification}

For the activity state classification task, the proposals stem from either natural language processing or earlier experimentations involving machine learning and heart rate data. The raw input data of all users are concatenated, resulting in 95.000 data points. Before any shuffling happens, the first 80% is picked as training data and the remaining 20% as validation data.

Indexes spaced evenly apart based on the desired sequence length are generated, and a random offset is generated based on the length of the remaining beats that do not fit inside a sequence.

Each heartbeat has been labeled as a class, but these classes need to be translated to a single class for the entire sequence. If all beats in the tail of the sequence are the same class, the entire sequence gets assigned to this class. The length of this tail is a parameter that is explored later in the chapter, but the default case is a tail length of half the sequence length.

After these classes are determined, all sequences are sorted into their respective class bin and an equal amount of sequences for each class is bundled as the data for that epoch. After each epoch, the indexes are reshuffled and the offset is regenerated so that each epoch will see slightly different sequences in a different order.

Using this method with 3 classes, each epoch would result in approximately 30 batches, each containing 9 sequences of 128 timesteps. This means that approximately 35.000 beats out of the 76.000 timesteps of training data are used, this due to the fact that not every class is represented evenly in the raw data. Batch size is chosen as a multiple of the number of classes so that the total amount of sequences is divisible by the batch size. All the following networks use some form of softmax activation in their final layer and are trained with the "adam" optimizer using categorical cross-entropy as the loss function. This combination is chosen because it is optimized for multi-class labeling problems.


![Data batching \label{fig:data_batching}](source/figures/data_batching.png){ width=100% }


Another optimisation made is to dampen the learning rate once the network is reaching an equilibrium. Due to the relatively small dataset, the accuracy can vary wildly from epoch to epoch. By lowering the learning rate towards the end of the training run, a more consistent final result is achieved.

Each network is trained three times using the same settings and the result is averaged out, but in almost all cases the result of training fell within a margin of error.

### Long Short Term Memory

Long short-term memory (LSTM) is a type of recurrent neural network (RNN) that is used to analyse sequence data. A common use-case is connected handwriting recognition and speech recognition. An LSTM consists of multiple cells, each containing a memory cell and gates that make the cell capable of remembering values over arbitrary time intervals. These cells can pass a value to their successor cell (the hidden state), which makes them capable of handling sequences of data. The LSTM itself was proposed as an evolution of the standard RNN to solve the vanishing gradient problem, in which gradients that are back-propagated can explode or implode in size.


![RNN \& LSTM Cell [@Lanbouri2020] \label{fig:lstm}](source/figures/lstm.png){ width=100% }


The LSTM used has a cell for each beat in the input sequence, each with 11 hidden states (one for each feature). This layer outputs the hidden states of the very last cell. A densely connected layer containing three neurons, each signifying one of the three output classes, is used as the output layer.

This network manages to achieve some correct labeling with an accuracy of \~58\% on the validation set. A completely random labeler would correctly label 33\% of sequences, so LSTM is better but still far from ideal.

<!-- \~60\% on the training set and -->

### Deep LSTM

As an evolution of a standard LSTM network, a network with three stacked LSTM layers is evaluated. Instead of the LSTM layer returning the hidden states of the last cells, it outputs all the hidden states of all cells. This is then passed to a second LSTM layer which then passes all of its hidden states to the third and final LSTM layer. This third layer passes the hidden outputs of its very last cell to a dense layer in the same way as the shallow LSTM. This results in a network containing 3072 trainable parameters. The network achieves \~65\% accuracy on the validation set, which is marginally better than a simple LSTM.

<!-- \~63\% accuracy on the training set and  -->

### DeepHeart

DeepHeart is a network architecture proposed by Ballinger et al. [@Ballinger2018] to classify HRV data into 5 categories (normal, diabetes, high blood pressure, and sleep apnea). It is designed to give a classification for every timestep (Heartbeat in this case), which makes it a sequence-to-sequence algorithm. It is the combination of a convolutional network and a recurrent network. Convolutional layers are layers that can reduce dimensionality of the previous layer, meaning that that they take multiple inputs and reduce it down to 1 output in an overlapping manner. This means that with a filter size of 4, each timestep in the output will be the result of a combination of 4 timesteps in the input. This of course reduces the length of the sequence by the filter length. Convolutional layers are often paired with pooling layers, which further reduce dimensionality. In this case, Maxpooling layers with a pool size of 2 were used. This means that for each 2 timesteps, only the maximum was passed on to the next layer. Maxpooling reduces the length of the sequence by its pool size.


![Convolutional and Pooling layers \label{fig:conv_pool}](source/figures/conv_pool.png){ width=100% }


The model consists of the following layers:

 - A convolutional layer with a filter size of 12, followed by a 0.2 dropout and a max pooling layer with a pool size of 2
 - Two convolutional layers with a filter size of 5, each followed by a 0.2 dropout and a max pooling layer with a pool size of 2
 - 4 Bidirectional LSTM layers, which means that each layer consists of 2 LSTM chains, one standard, and one that goes backward in time. This has the benefit that these layers can analyze sequences in the past as well as in the future. Of these four layers the first three output all their hidden states to the following layer and the fourth outputs the hidden state of the last cell
 - Here a slight adaptation is made to the original design. Instead of a "convolution of filter length 1" with tanh activation, a densely connected layer is used as output for the classification, to make the network more suitable to multilabel classification for disjunct classes.


![Deepheart [@Ballinger2018] \label{fig:deepheart}](source/figures/deepheart.png){ width=100% }


This results in a network containing 576.771 trainable parameters. The network achieves only \~62\% accuracy on the validation set, which makes it perform on the same level as the fairly simple and computationally less intensive simple LSTM network.

<!-- \~60\% accuracy on the training set and -->

### DeepHeart v2

DeepHeartV2 is a proposed evolution of DeepHeart for this thesis with the following changes:

 - In the original DeepHeart, the sequences are convoluted before being passed to multiple layers of RNNs. This has a significant impact on the productivity of the LSTM layers as much of the temporal information is filtered out before it reaches the memory cells of the LSTM. In the original model, there were only 11 timesteps left in these layers. In this version of DeepHeart, the 4 stacked LSTM layers are swapped with the 9 layers of the convolutional network.
 - The convolutional layers now use causal padding, a technique also used in WaveNet [@Oord2016].
 - A final LSTM is added before the densely connected output layer.
 - The bidirectional LSTMs each have 11 hidden outputs to match the number of features in the input data.

This results in a network containing 221.405 trainable parameters. The network achieves an accuracy of \~75\% on the validation set, which makes it perform significantly better than the original DeepHeart.

<!-- \~80\% accuracy on the training set and -->

### Temporal Convolutional Network

A Temporal Convolution Network (also known as a Causal Convolutional Network) is an adaptation of the well known Convolutional Neural Network, where there is no recurrent connection between "cells", but instead the input layer (receiving the sequence timesteps) gets step-wise convoluted down to an output layer. These convolutions must respect the ordering in which the data is modeled.

This network architecture requires either a large number of layers or wide filtering at every layer to achieve the large "receptive field" of the input layer. A way to increase this field without significantly increasing computational size is by using "Dilated Causal Convolution". This involves ignoring certain connections between layers based on their location and depth within the network. Visually it can be explained by imagining a tree structure within the layers (fig \ref{DCC}).

![Dilated Causal Convolution [@Oord2016] \label{DCC}](source/figures/DilutedCuasalCN.png){ width=100% }

In this implementation the keras-tcn package is used, which can stack multiple of these networks together as residual blocks (fig \ref{TCN_blocks}) which means these blocks have the potential to be skipped over. The TCN used in this thesis has a filter size of 2, contains 4 stacks of residual blocks, each containing 5 layers with resp. 1, 2, 4, 8, and 16 dilations, resulting in a receptive field of 128 timesteps. This layer outputs the states of its 128 timesteps to the densely connected layer containing 3 neurons, using softmax activation results in the classification that we want.

![Residual blocks in the TCN (From the keras-tcn github page) \label{TCN_blocks}](source/figures/TCN_blocks.jpg){ width=100% }

This results in a network containing 1.308.291 trainable parameters which makes it the most complex model by a wide margin. The network achieves \~85\% accuracy on the validation set, which makes it perform the best out of all models tested thus far.

<!-- \~80\% accuracy on the training set -->

### Labeling methods

As mentioned before in the introduction of this chapter, the method used to assign a class is a parameter in itself. If all beats in the tail of the sequence are the same class, the entire sequence gets assigned to this class. If this is not the case, the proposed sequence is instead discarded, this means that entire sections in the dataset are not used altogether. Decreasing this tail length would increase the dataset because fewer sequences are discarded.

It is however clear that a sufficiently low "checking parameter" will result in a sequence that is hard to predict. If the checking parameter is 1/_seq\_len_, the first _seq\_len_-1 can have a different class than the eventual sequence class.

The impact of this parameter is explored by training the 2 best performing models (DeepHeartV2 and TCN) on various tail lengths (TL).


Model          TL 50%      TL 25%         TL 10%       TL 5%
-----          ------      ------         ------       -----
DeepHeart V2   75%         70%            69%          66%
TCN            85%         82%            81%          80%


Table: The resulting accuracy of decreasing classification tail length. \label{Taillength}

Only a mild accuracy drop is observed in the TCN, while DeepHeartV2 shows a larger drop. What is apparent is that the accuracy drop is manageable, especially after a further investigation showed that it became harder for the model to achieve an optimal result with lower tail lengths. Some training runs showed nearly identical performance with TL 5% as with TL 50%, but the lower the TL parameter the lower the number of training sessions that achieved this accuracy, dragging the average result down. The training data size increased from approx. 30 batches per epoch for 50% TL to approx 35 batches per epoch for 5% TL, which is only a slight increase.


### Seq2Seq Classification

Sequence-to-sequence classification (where each element in a sequence receives a classification, instead of just the full sequence receiving a single classification) was considered but proved to be too inaccurate to be viable as a solution.


## Base-level fitness regression \label{ch:regression}

The base-level fitness regression is a fairly simple task. For each test subject, the data from their fitness training session was extracted and the base-level fitness was scored based on meta-data gained from the Baecke questionnaire and the stationary bicycle.

The goal would now be to create a model that can perform regression on just the data extracted from the heart rate sensor. If this method can be shown to be a valid way to achieve a fitness score, it means that it is possible to measure cardiovascular fitness based on heart rate data alone.

A simple densely connected neural network consisting of a handful of densely connected layers should be able to handle this task, after which possible improvements like Convolutional Neural Networks and others can be compared. However, it quickly became clear that the dataset of 23 subjects is too small to provide any result. Data resampling such as Bootstrapping (Creating new input samples by randomly sampling elements from other existing input samples) or Jackknifing (determining the distribution of each sample element and randomly generating new input samples from these distributions) would make it difficult to calculate a corresponding base-level fitness score, so would not have been beneficial for proving the validity of the regression task.

Validation loss rose to astronomical values and predictions on validation data were orders of magnitude larger or smaller than the expected 60-200 value range. An attempt was made to use K-Fold Cross Validation which mildly increased the training quality, but still, no adequate result was reached.
