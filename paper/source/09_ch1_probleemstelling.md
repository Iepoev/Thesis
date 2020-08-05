
# Introduction \label{ch:goal}

## Goal

The goal of this master thesis is to research the possibility of using Machine Learning to develop a digital personal coach for sport activities. It should be able to measure and track the performance of the user and suggest appropriate training sessions that result in an increase in cardiovascular fitness. In ideal conditions, a fully mature fitness coach should therefor be able to:

 - Be able to determine a "base fitness level" of the user during initialisation of the coaching program. This would be a machine learning regression task on labeled, batched sequence data to determine a certain "fitness level score"

 - Be able to determine the increase or decrease of the cardiovascular fitness of the user throught unlabeled monitoring. This would be a machine learning regression task on unlabeled, batched sequence data to update the previously acquired "fitness level score"

 - permanently track the user and classify his/her current state, optionally be able to automatically count periods of increased activity as a workout session. This would be a machine learning multi-label classification task on unlabeled, real-time sequenced data to determine the current exertion leven on a short-term timescale (30-60 seconds).

 - be able to track a user during his/her training session and provide feedback to keep the user in the optimal exertion range. This is a machine learning multi-label classification task on unlabeled, real-time sequence data to determine the current exertion leven on a very short-term timescale (5-10 seconds).

 - compile the result of a workout session to guage the intensity and the effect on the body of the user. At this point it should be able to determine the fatigue state of the user so that the coach can take this into account. This would be a machine learning classification task on labeled, batched sequence data to determine a fatigue state.

 - Suggest the user what kind of workout to perform next and how long to recover from recent workouts. This would be a recommender system task that can accurately predict overreaching in the user.

## scope of the thesis

to limit the scope of this master thesis, only 2 of these goals will be researched in depth

 - A model that can classify the state of the user. Is he/she resting, active, recovering, under intense exertion,...

 - A model to gauge the cardiovascular fitness level of the user.

The primary measurement used is Heart Rate Variability. This is the miniscule variability in time between heartbeats and is the result of a multitude of complex interactions between various hormonal and nervous systems of the body. HRV has been a subject of research in the medical community and can be used to predect various cardiovascular diseases or conditions. Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning.


## Why only heart rate

While modern smartphones are almost always equiped with various sensors that can facilitate data-gathering (such as accelerometer, pedometers, gps-trackers,...), this thesis will focus on heart rate and its variablity only. HRV has been a subject of research in the medical community and has been shown to be a marker of conditions such as epilepsy, Parkinson, multiple sclerosis [@Cygankiewicz2013], stress resilience [@Dong2018] and ev sudden death from cardiac causes [@Bassan2005].

Closer related to the subject of a fitness coach, it has been shown that habitual aerobic exercise plays a role in maintaining augmented HRV [@DeMeersman], that HRV is likely to be sensitive to training adaptation [@Buchheit2014] and that HRV might be a better measure of cardiovascular fitness than post-exercise Heart Rate Recovery [@Buchheit2006].

Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning. This however excludes the increasingly popular "smartwatches" that monitor heartrate using the less accurate light-based PPG method, as this method is incapable of measuring HRV.

Limiting the subject to Heart Rate Variability reduces complexity and introduces less unknown variables, which should result in a clear conclusion wether HRV is a suitable subject for further research and continued development.

## Methodology

### Data Gathering
 
Participants were asked to strap on a Polar H7 HRV-capable chest heart rate monitor and perform a specific fitness training session on a Kettler Ergometer X3. Beat-to-beat intervals were measered and stored using the Elite HRV android app, which is able to export these values into text files where each line represents the milliseconds between 2 beats.

The Kettler Ergometer X3 is equiped with an electromagnetic braking system which adapts to the cycling strenght of the user. Brake horsepower is determined by output torque and rotational speed, so the Ergometer measures the rotational speed of the user and provides adequate braking power so that the user is forced to provide the preset brake horsepower to keep the rotational speed constant. This brake horsepower is provided in Wattage (Joule per second).

The Ergometer is also able to calculate the energy spent during the various stages of the session. As the power is equal to energy over time, determining energy is simply a matter of multiplying the power determined earlier with the time spent at this power output.

The session consisted of the following stages:

 - a 2 minute stage in sedentary rest
 - a 5 minute stage in which the subject provides 50W (0.067 BHP) at 50 Rotations per minute
 - a 5 minute stage in which the subject provides 100W (0.134 BHP) at 50 Rotations per minute
 - a 2 minute stage of recovery in sedentary rest
 - a 5 minute stage in which the subject tries to maintain 115-120 bpm Heart Rate (equals to around 60% of the maximum heart rate of young adults)
 - a 2 minute stage of recovery in sedentary rest
 - a 5 minute stage in which the subject tries to maintain 155-160 bpm Heart Rate (equals to around 80% of the maximum heart rate of young adults)
 - a 1 minute stage in which the subject cycles at maximum exertion
 - a 13 minute stage of recovery

The following meta-data is noted:

 - the Rating of Perceived Exertion of each session
 - the energy spent during the three "constant heart rate" sessions
 - the distance traveled during the three "constant heart rate" sessions
 - the Baecke questionnaire scores of the subject

The reasoning behind the methodology of this data gathering session is explained in depth in in chapter \ref{ch:metrics}. In total 27 test subjects were gathered, of which 23 were able to fully complete the session, resulting in \~95.000 heartbeats of data.

### Machine learning

Various sequence learning and established Natural Language Processing techniques are tested and compared for the activity state classification task:

 - a standard Long Short Term Memory (LSTM) network
 - a deeply layered Long Short Term Memory (LSTM) network
 - an experimental "Deepheart" network that was successfully used to diagnose various medical conditions [@Ballinger2018]
 - a Temporal Convolutional Network (TCN)

Various Convolutional and residual networks are tested for the base level fitness regression task.