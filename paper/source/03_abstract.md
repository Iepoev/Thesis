
# Abstract {.unnumbered}

## background

People who practice sports occasionally, often have no or very limited support and guidance. People can download a fitness scheme or app from the internet, but these schemes are often not personalized to the physical capabilities of that person. Moreover, these schemes are often static and do not take into account the real progress that a user has made or personal goals. Nowadays, the technological advances allow a more accurate monitoring of the user. Smart watches are become more and more popular. Heart rate sensors are becoming cheap and commonplace. Computational power of wearables and smartphones is increasing, which makes running complex tasks such as light-weight machine learning more of a reality.

## Method

The goal of this master thesis is to research the possibility of using Machine Learning to develop a digital personal coach for sport activities. To achieve this goal, 2 subgoals have been isolated. 

 - A model that can classify the state of the user. Is he/she resting, active, recovering, under intense exertion,...

 - A model to gauge the cardiovascular fitness level of the user.

The primary measurement used is Heart Rate Variability. This is the miniscule variability in time between heartbeats and is the result of a multitude of complex interactions between various hormonal and nervous systems of the body. HRV has been a subject of research in the medical community and can be used to predict various cardiovascular diseases or conditions. Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning.

In this master thesis the Polar H7 (a HRV-capable chest strap) is used to measure heart rate data from test subjects. Healthy young adults were asked to perform a specific fitness training session on a Kettler ergometer x3, their heart rate response was measured and various meta-datapoints were noted. A polar plug-in adapter was used synchronise the measurements between the chest strap and the hometrainer. The heart rate measurements were used as labeled data for the heart rate classifier. A formula is established to give a "fitness score" based on their results and with some post-processing the heart rate measurements are reduced to a fixed amount of datapoints as input for the fitness score regression. Multiple deep neural networks are tested and evaluated for the classifier and regression tasks.

## Results

## Conclusion

\pagenumbering{roman}
\setcounter{page}{1}

