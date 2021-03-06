
# Appendix A: Network Summaries {.unnumbered}

## LSTM network summary {.unnumbered}

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
======================================================	z===========
input_1 (InputLayer)         [(None, 128, 11)]         0         
_________________________________________________________________
lstm (LSTM)                  (None, 11)                1012      
_________________________________________________________________
dense (Dense)                (None, 3)                 36        
=================================================================
Total params: 1,048
Trainable params: 1,048
Non-trainable params: 0
_________________________________________________________________

```

## Deep LSTM network summary {.unnumbered}

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         [(None, 128, 11)]         0         
_________________________________________________________________
lstm (LSTM)                  (None, 128, 11)           1012      
_________________________________________________________________
lstm_1 (LSTM)                (None, 128, 11)           1012      
_________________________________________________________________
lstm_2 (LSTM)                (None, 11)                1012      
_________________________________________________________________
dense (Dense)                (None, 3)                 36        
=================================================================
Total params: 3,072
Trainable params: 3,072
Non-trainable params: 0
_________________________________________________________________
```

## DeepHeart network summary {.unnumbered}

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         [(None, 128, 11)]         0         
_________________________________________________________________
conv1d (Conv1D)              (None, 117, 128)          17024     
_________________________________________________________________
dropout (Dropout)            (None, 117, 128)          0         
_________________________________________________________________
max_pooling1d (MaxPooling1D) (None, 58, 128)           0         
_________________________________________________________________
conv1d_1 (Conv1D)            (None, 54, 128)           82048     
_________________________________________________________________
dropout_1 (Dropout)          (None, 54, 128)           0         
_________________________________________________________________
max_pooling1d_1 (MaxPooling1 (None, 27, 128)           0         
_________________________________________________________________
conv1d_2 (Conv1D)            (None, 23, 128)           82048     
_________________________________________________________________
dropout_2 (Dropout)          (None, 23, 128)           0         
_________________________________________________________________
max_pooling1d_2 (MaxPooling1 (None, 11, 128)           0         
_________________________________________________________________
bidirectional (Bidirectional (None, 11, 128)           98816     
_________________________________________________________________
bidirectional_1 (Bidirection (None, 11, 128)           98816     
_________________________________________________________________
bidirectional_2 (Bidirection (None, 11, 128)           98816     
_________________________________________________________________
bidirectional_3 (Bidirection (None, 128)               98816     
_________________________________________________________________
dropout_3 (Dropout)          (None, 128)               0         
_________________________________________________________________
dense (Dense)                (None, 3)                 387       
=================================================================
Total params: 576,771
Trainable params: 576,771
Non-trainable params: 0
_________________________________________________________________

```

## DeepHeartV2 network summary {.unnumbered}

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         [(None, 128, 11)]         0         
_________________________________________________________________
bidirectional (Bidirectional (None, 128, 22)           2024      
_________________________________________________________________
bidirectional_1 (Bidirection (None, 128, 22)           2992      
_________________________________________________________________
bidirectional_2 (Bidirection (None, 128, 22)           2992      
_________________________________________________________________
bidirectional_3 (Bidirection (None, 128, 22)           2992      
_________________________________________________________________
dropout (Dropout)            (None, 128, 22)           0         
_________________________________________________________________
conv1d (Conv1D)              (None, 128, 128)          33920     
_________________________________________________________________
dropout_1 (Dropout)          (None, 128, 128)          0         
_________________________________________________________________
max_pooling1d (MaxPooling1D) (None, 64, 128)           0         
_________________________________________________________________
conv1d_1 (Conv1D)            (None, 64, 128)           82048     
_________________________________________________________________
dropout_2 (Dropout)          (None, 64, 128)           0         
_________________________________________________________________
max_pooling1d_1 (MaxPooling1 (None, 32, 128)           0         
_________________________________________________________________
conv1d_2 (Conv1D)            (None, 32, 128)           82048     
_________________________________________________________________
dropout_3 (Dropout)          (None, 32, 128)           0         
_________________________________________________________________
max_pooling1d_2 (MaxPooling1 (None, 16, 128)           0         
_________________________________________________________________
bidirectional_4 (Bidirection (None, 22)                12320     
_________________________________________________________________
dense (Dense)                (None, 3)                 69        
=================================================================
Total params: 221,405
Trainable params: 221,405
Non-trainable params: 0
_________________________________________________________________

```

## TCN network summary {.unnumbered}

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         [(None, 128, 11)]         0         
_________________________________________________________________
tcn (TCN)                    (None, 128)               1307904   
_________________________________________________________________
dense (Dense)                (None, 3)                 387       
=================================================================
Total params: 1,308,291
Trainable params: 1,298,051
Non-trainable params: 10,240
_________________________________________________________________

```