
# Base Level Fitness regression \label{ch:data}

The base-level fitness regression is a fairly simple task. For each test subject, the data from their fitness training session was extracted and the base level fitness was scored based on meta-data gained from the Baecke questionnaire and the stationary bicycle.

The goal would now be to create a model that can perform regression on just the data extracted from the Heart Rate sensor. If this method can be shown to be a valid way to achieve a fitness score, it means that it is possible to measure cardiovascular fitness based on heart rate data alone.

A simple densely connected neural network consisting of a handful of densely connected layers should be able to handle this task, after which possible improvements like Convolutional Neural Networks and others can be compared. However, it quickly became clear that the dataset of 23 subjects is too small to provide any result. Data resampling such as Bootstrapping (Creating new input samples by randomly sampling elements from other existing input samples) or Jackknifing (determining the distribution of each sample element and randomly generating new input samples from these distributions) would make it difficult to calculate a corresponding base level fitness score, so would not have been beneficial for proving the validity of the regression task.

Validation loss rose to astronomical values and predictions on validation data were orders of magnitude larger or smaller than the expected 60-200 value range. An attempt was made to use K-Fold Cross Validation which mildly increased the training quality, but still, no adequate result was reached.
