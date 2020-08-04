
# Metrics \label{ch:metrics}

Using the knowledge gained in the previous chapter, various metrics are carefully picked based on how relevant they are to cardiovascular fitness. In an ideal scenario we could measure oxygen levels in the blood, but equipment for this kind of data gathering is expensive and bulky, which makes it hard to perform at the scale required for machine learning applications. 

As a reminder, the subjects were asked to perform the following fitness training session:

 - a 2 minute stage in sedentary rest
 - a 5 minute stage in which the subject provides 50W (0.067 BHP) at 50 Rotations per minute
 - a 5 minute stage in which the subject provides 100W (0.134 BHP) at 50 Rotations per minute
 - a 2 minute stage of recovery in sedentary rest
 - a 5 minute stage in which the subject tries to maintain 115-120 bpm Heart Rate (equals to around 60% of the maximum heart rate of young adults)
 - a 2 minute stage of recovery in sedentary rest
 - a 5 minute stage in which the subject tries to maintain 155-160 bpm Heart Rate (equals to around 80% of the maximum heart rate of young adults)
 - a 1 minute stage in which the subject cycles at maximum exertion
 - a 4 minute stage of recovery

Test subjects were asked to abstain from alcohol for at least 24 hours, and to abstain from caffeine for at least 12 hours. This is an acceptable compromise between the personal life of the test subjects and the half-life time of the substances in the circulatory system.

The RR-intervals are measured and stored using the Elite HRV android app, which can then be exported to text files where each line contains an integer representing the milliseconds between each beat. These intervals are then sent through a filter and passed on for feature extraction/engineering.

The feature extraction/engineering results in every RR interval being accompanied by 10 extra features:
 
 - HR
 - HRV
 - 

## RR-interval filtering and correction

Not all heartbeats are captured perfectly. We need to be able to filter out any ectopic beats that occur, and also be able to account for beats that were erroneously measured or completely skipped by the heart beat sensor or the bluetooth connection.

before passing on to feature engineering, each interval is stored in a seven-beat window. When this window is full, the fourth beat is checked (Current Beat Timing, CBT). If it differs from the previous beat with either more than 50ms, or more than 10ms and 3 times the current HRV, a closer look is taken.

The filterer will assume one of five scenarios happened. For each scenario it creates a hypothetical solution, and calculates how realistic this solutions is. It then picks the best solution and applies a correction to the current seven-beat window.

The filter checks for multiple possibilities:

 - there is a sudden change in HRV, the measured CBT is correct. The future 3 beats are taken and averaged out. The score of this solution is the CBT minus this average.
 - the sensor failed to register a beat. The proposed solution is the replace the CBT with two beats with $CBT / 2$. The score of this solution is the difference between the average of the seven-beat window excluding the CBT, and $CBT / 2$
 - the sensor failed to register two successive beats. The proposed solution is the replace the CBT with three beats with $CBT / 3$. The score of this solution is the difference between the average of the seven-beat window excluding the CBT, and $CBT / 3$
 - the sensor mis-registered a beat. The proposed solution is to average out the CBT and its successor. The score of this solution is the difference between the average of the seven-beat window excluding the CBT and its successor, and the averaged timing value
 - the sensor mis-registered _and_ missed a beat. The proposed solution is to average out the CBT and its successor, and to add an additional beat with this averaged timing. The score of this solution is the difference between the average of the seven-beat window excluding the CBT and its successor, and the averaged timing value

At first, if the score of the sudden change solution is less than 50ms, it means that there is no faulty measurement, just a sudden change in Heart Rate Variability. however, if this is not the case, the filterer checks for the lowest score of the four proposed solutions. If this score is lower than the score of the "sudden change", it is accepted and the seven-beat window is replaced by the solution. If the cause of the change in IBI timing is still unexplained, the filtering gives up and will simply accept the faulty measurement.

## Heart Rate metrics feature engineering for the classification task

### RR interval

The most basic measurement from which all others are derived, the RR interval is the exact time between heartbeats in milliseconds. These values are stored in various sliding windows (of a constant time interval, 10 seconds, 60 seconds, 120 seconds and 300 seconds respectively) for further derivation.

### Current Heart Rate

Beat-to-beat heart rate is the standard way to measure cardiac activity. It is simply the amount of full contractions of the heart per minute. Because we are starting from heart rate variability metrics, it is easily derived by (60000/RR-interval in milliseconds), but to reduce the inherent variability of heart rate variability, the linearly weighted moving average of the last 10 seconds of measurements are taken.

### Current Heart Rate Variability

A very simple way to determine the current overall HRV is to simply take the difference between the last 2 beats, but this proved to be a very unstable measurement, again due to the inhereint variability of HRV. So just like HR, the linearly weighted moving average of the last 10 seconds of measurements are taken.

### Maximum Heart Rate

Maximum heart rate being a constant value for a subject regardless his/her fitness level makes it an important metric to track. During the data gathering training session subjects were asked to perform a maximal exertion test, so the maximum heart rate achieved during the session is taken as their maximum heart rate.

### Resting Heart Rate

During the data gathering training session subjects started out with a 2 minute sedentary rest period. Theoretically the resting heart rate can be determined during this window, but some subjects showed lower heart rates during certain recovery segments in the middle of the session. We attribute this to increased stress level the subject attained from the anticipation of being tested, which is absent during the recovery segments.

Therefore, the resting heart rate is determined to be the global minimum heart rate attained during the session

## Heart Rate Variability metrics

### SDNN, SDSD, RMSSD \& pNN50 (120 second epoch)

Standard Deviation of Inter Beat Intervals is the most basic way to analyse HRV in the time domain, so we include it in our model inputs. Standard deviation of the successive differences between IBIs is also an easy and basic measurement. [@Danieli2014] also shows that RMSSD and SDNN are higher in athletes so we include both metrics.

pNN50 was chosen over NN50 because the amount of beats in the 120 second window varied greatly depending on the current heart rate of the subject. (at maximum exertion, the RR interval can drop to 350ms resulting in a window of 300-350 beats, while at rest the RR interval can be as high as 1000ms, resulting in a window of 120 beats)

### Frequency domain 

For extracting Frequency domain statistics Welch's _spectral density estimation_ is used. The resulting periodogram is returned as a list of equally spaced segments, where each element represents the power of that particular segment. For each frequency band we can sum the corresponding segments to achieve the power that band.

[@Danieli2014] shows that HF power is higher in athletes so we include it. Because it is also a measure of parasympathetic activity, we analyse HF power in a fairly short 60 second epoch otherwise we would not be able to accurately assess HF power during the relativy short recovery and resting segments.
 
Due to the low period of VLF and LF power (oscillation periods of up to 300 seconds and up to 25 seconds respectively) their power is calculated from 300 second epochs. LF/HF ratio is also derived from this 300 second IBI window

### Classification

Due to the setup of the training session it is easy to classify each heart beat. A global time counter keeps track of the absolute time passed since the start of recording, which makes it easy to classify each stage of the session:

 - the resting stage is classified as "resting"
 - the recovery stages are classified as "recovery"
 - the remaining stages are classified as "active"

## Subject Variables for the regression task

For each subject, some extra meta-data is gathered for use in the fitness regression task.

The following meta-data is noted:

 - the Rating of Perceived Exertion of each session
 - the energy spent during the three "constant heart rate" sessions
 - the Baecke questionnaire scores of the subject
 - the Maximum Heart Rate of the subject 
 - the Resting Heart Rate of the subject
 - the maximum heart rate of the subject during the 50W 50RPM stage
 - the maximum heart rate of the subject during the 100W 50RPM stage

out of these variables, a fitness score is calculated from the sum of 3 values:

 - The calories expended during the maximum exertion stage, multiplied by 2. Maximum Exertion is a good metric for VO2_{max}, but as we can't measure oxygen levels in the blood we use the expended energy as a substitute.
 - The sum of the calories expended during the two constant Heart Rate stages, multiplied by the Baecke score divided by 15. These two stages also reflect the capacity for the subject to produce energy under constant load, but this measure is less reliable. By incorporating the Baecke score at this point we can grade the subject on their lifestyle.
 - The average percentage of the Heart Rate Reserve used by the subject during both constant load stages. Heart Rate reserve is the difference between the Max Heart Rate and Resting Heart Rate of the user. The lower the amount used of this reserve, the better the subject has adapted to exerting this load






#### Heart Rate Recovery
 - Heart rate recovery fast-to-slow phase transition: Influence of physical fitness and exercise intensity
 - Post-exercise heart-rate recovery correlates to resting heart-rate variability in healthy men
 - The relationship between resting heart rate variability and heart rate recovery
 - Estimation of heart rate recovery after stair climbing using a wrist-worn device

Ectopic beat


### Zuurstofopname
 - Prediction of maximal or peak oxygen uptake from ratings of perceived exertion
 - Submaximal, Perceptually Regulated Exercise Testing Predicts Maximal Oxygen Uptake: A Meta-Analysis Study 
 - Heart rate and exercise intensity during sports activities. Practical application.
 - Exercise and the autonomic nervous system.

Dit is een andere belangrijke meting, die we helaas niet rechtstreeks kunnen meten. Deze sectie onderzoekt het nut van de zuurstofopname af te leiden uit hartslag (en user input?), maar dit zal waarschijnlijk geen uiteindelijk deel worden van de fitnesscoach. de opgedane kennis is waarschijnlijk wel nutig voor `Physical Load Level` beter te bepalen.

### Physical Load Level
 - Prediction of Physical Load Level by Machine Learning Analysis of Heart Activity after Exercises
 - Heart rate and exercise intensity during sports activities. Practical application.
 - Exercise and the autonomic nervous system.

 Het uiteindelijk doel van alle metrieken en metingen. Een maat voor de inspanning die een gebruiker aan het leveren is. We willen dit nauwkeurig kunnen voorspellen, aangezien de fitnesscoach een specifiek trainingsregime zal aanbevelen op basis van de verwachte load level die dit regime teweeg brengt. Duidelijk de distinctie maken tussen absolute load level en de relatieve load level (hoeveel energie een regime vraagt vs hoeveel de gebruiker zich moet inspannen om deze energie te besteden)
