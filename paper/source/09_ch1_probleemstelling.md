\pagenumbering{arabic}

# Introduction \label{ch:goal}

## Goal

The goal of this master thesis is to research the possibility of using machine learning to develop a digital personal coach for sports activities. It should be able to measure and track the performance of the user and suggest appropriate training sessions that result in an increase in cardiovascular fitness. In ideal conditions, a fully mature fitness coach should, therefore:

 - Be able to determine a "base fitness level" of the user during the initialisation of the coaching program. This would be a machine learning regression task on labeled, batched sequence data to determine a certain "fitness level score"

 - Be able to determine the increase or decrease of the cardiovascular fitness of the user through unlabeled monitoring. This would be a machine learning regression task on unlabeled, batched sequence data to update the previously acquired "fitness level score"

 - Permanently track the user and classify their current "activity state", optionally be able to automatically count periods of increased activity as a workout session. This would be a machine learning multi-label classification task on unlabeled, real-time sequence data to determine the current exertion level on a short-term timescale (30-60 seconds).

 - Be able to track a user during their training session and provide feedback to keep the user in the optimal exertion range. This is a machine learning multi-label classification task on unlabeled, real-time sequence data to determine the current exertion level on a very short-term timescale (5-10 seconds).

 - Compile the result of a workout session to gauge the intensity and the effect on the body of the user. At this point, it should be able to determine the fatigue state of the user so that the coach can take this into account. This would be a machine learning classification task on labeled, batched sequence data to determine a fatigue state.

 - Suggest the user what kind of workout to perform next and how long to recover from recent workouts. This would be a recommender system task that can accurately predict so-called overreaching in the user.

## Scope of the thesis

To limit the scope of this master thesis, only the first three of these goals will be researched in-depth, the first two have been combined into 1 multipurpose model.

 - A model to gauge the cardiovascular fitness level of the user. Re-applying this model during different stages of the coaching period would be able to gauge the increase and decrease of the fitness level.

 - A model capable of classifying the state of the user. Are they resting, active, recovering, under intense exertion, ...

The primary measurement used is Heart Rate Variability (HRV). This is the minuscule variability in the time between heartbeats and is the result of a multitude of complex interactions between various hormonal and nervous systems of the body. HRV has been a subject of research in the medical community and can be used to predict various cardiovascular diseases or conditions. Current generation heart rate monitors can monitor HRV to a respectable degree compared to medical-grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning. This however excludes the increasingly popular "smartwatches" that monitor heartrate using the less accurate light-based PPG method, as this method is incapable of measuring HRV.


## Why only heart rate

While modern smartphones are almost always equipped with various sensors that can facilitate data-gathering (such as accelerometers, pedometers, GPS-trackers, ...), this thesis will focus on heart rate and its variability only. HRV has been shown to be a marker of conditions such as epilepsy, Parkinson, multiple sclerosis [@Cygankiewicz2013], stress resilience [@Dong2018], and even sudden death from cardiac causes [@Bassan2005].

Closer related to the subject of a fitness coach, it has been shown that habitual aerobic exercise plays a role in maintaining augmented HRV [@DeMeersman], that HRV is likely to be sensitive to training adaptation [@Buchheit2014] and that HRV might be a better measure of cardiovascular fitness than post-exercise Heart Rate Recovery [@Buchheit2006].

Limiting the subject to Heart Rate Variability reduces complexity and introduces less unknown variables, which should result in a clear conclusion of whether HRV is a suitable subject for further research and continued development.

## Methodology

### Data Gathering
 
Participants were asked to strap on a Polar H7 HRV-capable chest heart rate monitor and perform a specific fitness training session on a Kettler Ergometer X3. Beat-to-beat intervals were measured and stored using the Elite HRV Android app, which can export these values into text files where each line represents the milliseconds between 2 beats.

The Kettler Ergometer X3 is equipped with an electromagnetic braking system that adapts to the cycling strength of the user. Brake horsepower (BHP) is determined by output torque and rotational speed, so the Ergometer measures the rotational speed of the user and provides adequate braking power so that the user is forced to provide the preset BHP to keep the rotational speed constant. This BHP is provided in Wattage (Joule per second).

The Ergometer is also able to count the energy spent during the various stages of the session. As the power is equal to energy over time, determining energy is simply a matter of multiplying the power determined earlier with the time spent at this power output.

The session consisted of the following stages:

 - A 2-minute stage in sedentary rest.
 - A 5-minute stage in which the subject provides 50 Watt (0.067 BHP) at 50 rotations per minute.
 - A 5-minute stage in which the subject provides 100 Watt (0.134 BHP) at 50 rpm.
 - A 2-minute stage of recovery in sedentary rest.
 - A 5-minute stage in which the subject tries to maintain 115-120 bpm heart rate (equals to around 60% of the theoretical maximum heart rate of young adults).
 - A 2-minute stage of recovery in sedentary rest.
 - A 5-minute stage in which the subject tries to maintain 155-160 bpm heart rate (equals to around 80% of the theoretical maximum heart rate of young adults).
 - A 1-minute stage in which the subject cycles at maximum exertion.
 - A 13-minute stage of recovery, of which 4 minutes are kept for analysis.

Additionally, the following meta-data is noted:

 - The Rating of Perceived Exertion (RPE) of each session.
 - The energy spent during the three "constant heart rate" sessions.
 - The distance traveled during the three "constant heart rate" sessions.
 - The Baecke questionnaire scores of the subject.

The reasoning behind the methodology of this data gathering session is explained in-depth in chapter \ref{ch:metrics}. In total 27 test subjects were gathered, of which 23 were able to fully complete the session, resulting in \~95.000 timesteps of heartbeat data.

### Machine learning

Various sequence learning and established Natural Language Processing (NLP) techniques are tested and compared for the activity state classification task:

 - A standard Long Short Term Memory (LSTM) network.
 - A deeply layered LSTM network.
 - An experimental "DeepHeart" network that was successfully used to diagnose various medical conditions [@Ballinger2018].
 - A bespoke evolution of DeepHeart.
 - A Temporal Convolutional Network (TCN).

Various convolutional and residual networks are tested for the base-level fitness regression task.

These networks are written in Python 3.8.3, created using Keras, which uses the Tensorflow 2 library to train these networks on a GTX 1070Ti CUDA-enabled graphics card.