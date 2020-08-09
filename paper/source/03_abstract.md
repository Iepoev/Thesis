
\newpage

## Abstract {.unnumbered}

### Method {.unnumbered}

The goal of this master thesis is to use Machine Learning to develop a digital personal coach for sport activities. 2 subgoals have been isolated: A model capable of classifying the activity state of the user and a model to gauge the cardiovascular fitness level of the user. The primary measurement used is Heart Rate Variability. HRV has been a subject of research in the medical community and can be used to predict various cardiovascular diseases or conditions. This thesis attempts to reapproriate the existing HRV research for cardiovascular fitness and machine learning.

Healthy young adults were asked to perform a specific fitness training session on a stationary bicycle, their heart rate response was measured and various meta-datapoints were noted. In total 23 test subjects were added to the data set, resulting in \~95.000 timesteps of hearbeat data.

### Results {.unnumbered}

The following models were tested for acitivy state classification: LSTM (\~58% accuracy), Deep LSTM (\~65% accuracy), DeepHeart (\~62% accuracy), DeepHeartV2 (\~75% accuracy), TCN (\~85% accuracy). Developing the fitness base level regression resulted in a failure due to the small number of participants.

### Conclusion {.unnumbered}

The proposed networks managed to achieve up to \~85\% accuracy on activity state classification. This is a fairly positive result, but not yet applicable for real-world scenarios. 

However, while it is impossible to fully prove the validity of the applied methods until more data is gathered, both subgoals were explored and validated using heavily cited, peer-reviewed studies.

## Summary {.unnumbered}

### background {.unnumbered}

People who practice sports occasionally, often have no or very limited support and guidance. People can download a fitness scheme or app from the internet, but these schemes are often not personalized to the physical capabilities of that person. Moreover, these schemes are often static and do not take into account the real progress that a user has made or personal goals. Nowadays, the technological advances allow a more accurate monitoring of the user. Smart watches are become more and more popular. Heart rate sensors are becoming cheap and commonplace. Computational power of wearables and smartphones is increasing, which makes running complex tasks such as light-weight machine learning more of a reality.

### Method {.unnumbered}

The goal of this master thesis is to research the possibility of using Machine Learning to develop a digital personal coach for sport activities. To achieve this goal, 2 subgoals have been isolated. 

 - A model capable of classifying the state of the user. Is he/she resting, active, recovering, under intense exertion, ...
 - A model to gauge the cardiovascular fitness level of the user.

The primary measurement used is Heart Rate Variability. This is the miniscule variability in time between heartbeats and is the result of a multitude of complex interactions between various hormonal and nervous systems of the body. HRV has been a subject of research in the medical community and can be used to predict various cardiovascular diseases or conditions. Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning.

In this master thesis the Polar H7 (a HRV-capable chest strap) is used to measure heart rate data from test subjects. Healthy young adults were asked to perform a specific fitness training session on a Kettler ergometer x3, their heart rate response was measured and various meta-datapoints were noted. A polar plug-in adapter was used synchronise the measurements between the chest strap and the stationary bicycle.  In total 27 test subjects were gathered, of which 23 were able to fully complete the session, resulting in \~95.000 timesteps of hearbeat data.

The heart rate measurements were used as labeled data for the heart rate classifier. A formula is established to give a "fitness score" based on their results and with some post-processing the heart rate measurements are reduced to a fixed amount of datapoints as input for the fitness score regression. Multiple deep neural networks are tested and evaluated for the classifier and regression tasks. 

### Results {.unnumbered}

The following accuracies were achieved for acitivy state classification:

Model          Accuracy
-----          --------
LSTM           \~58%
Deep LSTM      \~65%
DeepHeart      \~62%
DeepHeartV2    \~75%
TCN            \~85%

Developing the fitness base level regression resulted in a failure due to the small number of participants.

### Conclusion {.unnumbered}

The proposed networks managed to achieve up to \~85\% accuracy on activity state classification. This is a fairly positive result, but not yet applicable for real-world scenarios. 

However, while it is impossible to fully prove the validity of the applied methods until more data is gathered, both subgoals were explored and validated using heavily cited, peer-reviewed studies.

\pagenumbering{roman}
\setcounter{page}{1}

