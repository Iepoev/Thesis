
# Data Gathering \label{ch:metrics}


Using the knowledge gained in the previous chapter, various metrics are carefully picked based on how relevant they are to cardiovascular fitness. In an ideal scenario, we could measure oxygen levels in the blood, but equipment for this kind of data gathering is expensive and bulky, which makes it hard to perform at the scale required for machine learning applications.

As a reminder, the subjects were asked to perform the following fitness training session:

 - a 2-minute stage in sedentary rest
 - a 5-minute stage in which the subject provides 50W (0.067 BHP) at 50 rpm
 - a 5-minute stage in which the subject provides 100W (0.134 BHP) at 50 rpm
 - a 2-minute stage of recovery in sedentary rest
 - a 5-minute stage in which the subject tries to maintain 115-120 bpm Heart Rate (equals to around 60% of the maximum heart rate of young adults)
 - a 2-minute stage of recovery in sedentary rest
 - a 5-minute stage in which the subject tries to maintain 155-160 bpm Heart Rate (equals to around 80% of the maximum heart rate of young adults)
 - a 1-minute stage in which the subject cycles at maximum exertion
 - a 4-minute stage of recovery

Test subjects were sourced from the student population and were of mixed gender, various fitness levels, aged between 19 and 28 years old. Test subjects were asked to abstain from alcohol for at least 24 hours and to abstain from caffeine for at least 12 hours. This is an acceptable compromise between the personal life of the test subjects and the half-life time of the substances in the circulatory system. In total 27 test subjects were gathered, of which 23 were able to fully complete the session, resulting in \~95.000 timesteps of heartbeat data.


The RR intervals are measured and stored using the Elite HRV Android app, which can then be exported to text files where each line contains an integer representing the milliseconds between each beat. These intervals are then sent through a filter and passed on for feature engineering.

## RR interval filtering and correction

Not all heartbeats are captured perfectly. Any ectopic beats that occur need to be filtered out and beats that were erroneously measured or completely skipped by the heartbeat sensor or the Bluetooth connection need to be accounted for.

Before passing on to feature engineering, each interval is stored in a seven-beat window. When this window is full, the fourth beat is checked (Current Beat Timing, CBT). If it differs from the previous beat with either more than 50ms or more than 10ms and 3 times the current HRV, a closer look is taken.

The filterer will assume one of five scenarios happened. For each scenario, it creates a hypothetical solution and calculates how realistic this solution is. It then picks the best solution and applies a correction to the current seven-beat window.

The filter checks for multiple possibilities:

 - there is a sudden change in HRV, the measured CBT is correct. The future 3 beats are taken and averaged out. The score of this solution is the CBT minus this average.
 - the sensor failed to register a beat. The proposed solution is to replace the CBT with two beats with $CBT / 2$. The score of this solution is the difference between the average of the seven-beat window excluding the CBT, and $CBT / 2$
 - the sensor failed to register two successive beats. The proposed solution is to replace the CBT with three beats with $CBT / 3$. The score of this solution is the difference between the average of the seven-beat window excluding the CBT, and $CBT / 3$
 - the sensor misregistered a beat. The proposed solution is to average out the CBT and its successor. The score of this solution is the difference between the average of the seven-beat window excluding the CBT and its successor, and the averaged timing value
 - the sensor misregistered _and_ missed a beat. The proposed solution is to average out the CBT and its successor and to add an additional beat with this averaged timing. The score of this solution is the difference between the average of the seven-beat window excluding the CBT and its successor, and the averaged timing value.

At first, if the score of the sudden change solution is less than 50ms, it means that there is no faulty measurement, just a sudden change in Heart Rate Variability. however, if this is not the case, the filterer checks for the lowest score of the four proposed solutions. If this score is lower than the score of the "sudden change", it is accepted and the seven-beat window is replaced by the solution. If the cause of the change in IBI timing is still unexplained, the filtering gives up and will simply accept the faulty measurement.

## Heart Rate metrics feature engineering for the classification task

The feature engineering results in every RR interval being accompanied by 10 extra features:

 - HR
 - HRV
 - SDNN
 - SDSD
 - pNN50
 - RMSSD
 - HF power (60s epoch)
 - LF power (300s epoch)
 - VLF power (300s epoch)
 - LF/HF ratio (300s epoch)


Figure \ref{user_data} plots these datapoints out for a sample user over time. It is immediately clear that some correlations exist, which means that we should be able to obtain a working Machine Learning classifier.

![Feature extraction from heartbeat data \label{user_data}](source/figures/user_data.png){ width=100% }


### RR interval

The most basic measurement from which all others are derived, the RR interval is the exact time between heartbeats in milliseconds. These values are stored in various sliding windows (of a constant time interval, 10 seconds, 60 seconds, 120 seconds, and 300 seconds respectively) for further derivation.

### Current Heart Rate

The beat-to-beat heart rate is the standard way to measure cardiac activity. It is simply the number of full contractions of the heart per minute. Because we are starting from heart rate variability metrics, it is easily derived by (60000/RR interval in milliseconds), but to reduce the inherent variability of heart rate variability, the linearly weighted moving average of the last 10 seconds of measurements is taken.

### Current Heart Rate Variability

A very simple way to determine the current overall HRV is to simply make the difference between the last 2 beats, but this proved to be a very unstable measurement, again due to the inherent variability of HRV. So just like HR, the linearly weighted moving average of the last 10 seconds of measurements is taken.

### Maximum Heart Rate

Maximum heart rate being a constant value for a subject regardless of their fitness level makes it an important metric to track. During the data gathering training session, subjects were asked to perform a maximal exertion test, so the maximum heart rate achieved during the session is assumed to be their maximum heart rate.

### Resting Heart Rate

During the data gathering training session, subjects started with a 2-minute sedentary rest period. Theoretically, the resting heart rate can be determined during this window, but some subjects showed lower heart rates during certain recovery segments in the middle of the session. This can be attributed to the increased stress level the subject attained from the anticipation of being tested, which is absent during the recovery segments.

Therefore, the resting heart rate is determined to be the global minimum heart rate attained during the session.

### HRV Time domain

Standard Deviation of Inter Beat Intervals is the most basic way to analyse HRV in the time domain, so it should be included in our model inputs. The standard deviation of the successive differences between IBIs is also an easy and basic measurement. [@Danieli2014] also shows that RMSSD and SDNN are higher in athletes so both metrics are included.

pNN50 was chosen over NN50 because the number of beats in the 120-second window varies greatly depending on the current heart rate of the subject. (at maximum exertion, the RR interval can drop to 350ms resulting in a window of 300-350 beats, while at rest the RR interval can be as high as 1000ms, resulting in a window of 120 beats)

### HRV Frequency domain

For extracting frequency domain statistics Welch's _spectral density estimation_ is used. The resulting periodogram is returned as a list of equally spaced segments, where each element represents the power of that particular segment. For each frequency band, we can sum the corresponding segments to achieve the power of that band.

[@Danieli2014] shows that HF power is higher in athletes, so it is included. Because it is also a measure of parasympathetic activity, we analyse HF power in a fairly short 60-second epoch otherwise we would not be able to accurately assess HF power during the relatively short recovery and resting segments.

Due to the low period of VLF and LF power (oscillation periods of up to 300 seconds and up to 25 seconds respectively), their power is calculated from 300-second epochs. LF/HF ratio is also derived from this 300-second IBI window.

### Classification

Due to the setup of the training session, it is easy to classify each heartbeat. A global time counter keeps track of the absolute time passed since the start of recording, which makes it easy to classify each stage of the session:

 - the resting stage is classified as "resting" (class 0)
 - the active stages are classified as "active" (class 1)
 - the recovery stages are classified as "recovery" (class 2)

## Subject Variables for the regression task

For each subject, some extra meta-data is gathered for use in the fitness regression task.

### Fitness score

The following meta-data is noted (fig \ref{fitness_subvariables}):

 - the resting heart rate of the subject
 - the maximum heart rate of the subject during the 50W 50 rpm stage
 - the maximum heart rate of the subject during the 100W 50 rpm stage
 - the maximum heart rate of the subject
 - the energy spent during the three "constant heart rate" stages
 - the Baecke questionnaire scores of the subject

out of these variables, a fitness score is calculated from the sum of 3 values:

 - The calories expended during the maximum exertion stage, multiplied by 2. Maximum exertion is a good metric for VO2$_{max}$, but as we can't measure oxygen levels in the blood we use the expended energy as a substitute.
 - The sum of the calories expended during the two constant Heart Rate stages, multiplied by the Baecke score divided by 15. The energy expenditure of these two stages also reflects the capacity for the subject to produce energy under constant load, but this measure is less reliable and not backed by research. By incorporating the Baecke score at this point we can make this measure less important while also grading the subject on their lifestyle which has been shown to correlate with cardiovascular fitness.
 - The average percentage of the heart rate reserve used by the subject during both constant load stages. heart rate reserve is the difference between the maximum heart rate and resting heart rate of the user. The lower the amount used of this reserve, the better the subject has adapted to exerting this load

The resulting score (\ref{fitness_score}) is a unitless value between 60 and 170. This score is very dependent on gender and should not be used to compare different subjects, as it is intended to monitor the increase or decrease in cardiovascular fitness of the subject.

![Fitness scores of the test subjects \label{fitness_score}](source/figures/fitness_score_boxplot.png){ width=100% }

![Fitness scores sub-variables of the test subjects \label{fitness_subvariables}](source/figures/user_profile_hr.png){ width=100% }

### Input data

Because of the limitations of neural networks, the size of the input must be identical for all subjects. This means that the variable-length heartbeat data can't simply be passed to the machine learning algorithm. The data of the training session must be engineered to fit a constant-length input.

The maximum heart rate, resting heart rate, VLF, LF \& HF power, and LF/HF ratio are extracted from the complete session.
For every active stage of the session the VLF power, LF power, HF power, LF/HF ratio, maximum Heart rate, and rMSSD of that 5-minute segment is extracted. For every recovery stage, these same parameters are extracted with the additional Heart Rate Recovery after 1 minute and the Heart Rate Recovery after 2 minutes.
