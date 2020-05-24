
# Metrics \label{ch:metrics}

## metrieken

### Accelerometer

Dit is een moeilijke metriek om te betrekken, aangezien dit heel afhankelijk is van het type van de trainingsessie. In deze sectie onderzoeken we in welke mate de accelerometer gebruikt kan worden in andere gevallen, en of dit een substantieel voordeel is om te betrekken in de fitnesscoach.

### Verschillende soorten heartrate

Hartslag kunnen we zelf meten. Momenteel zijn smartwatches zelden accuraat genoeg om HRV te bepalen, maar in het onderzoek gaan we er van uit dat het wel mogelijk is. Zie sectie `Gevolgen van inaccurate metingen`. High-end borstkas hartmetingen zijn wel in staat om HRV te meden.

Dit zijn allemaal vaak gebruikte metrieken in medische literatuur, en komen vaak terug in het bepalen van inspanning en fysieke fitheid. Deze sectie overloopt ze allemaal, hun significantie in de context van dit onderzoek, en waar ze gebruikt worden.

#### Heart Rate 
 - RR Interval

#### Resting Heart Rate
 - Determining target heart rate for exercising in a cardiac rehabilitation program: a retrospective study.
 - Relationship between resting heart rate, blood pressure and pulse pressure in adolescents

Heart rate reserve
Target heart rate opstellen met Karvonen method

#### Heart Rate Variability (HRV)
 - Heart rate variability and aerobic fitness
 - Deep neural heart rate variability analysis
 - The relationship between resting heart rate variability and heart rate recovery

RMSSD: Root mean square of the successive differences RMSSD is strongly backed by research and is considered the most relevant and accurate measure of Autonomic Nervous System activity over the short-term. Here are a few studies referencing its use: 
ln(RMSSD): log van RMSSD
NN50: The number of pairs of successive NN (R-R) intervals that differ by more than 50 ms
PNN50: The proportion of NN50 divided by the total number of NN (R-R) intervals
SDNN: Standard deviation of the NN (R-R) intervals


TODO: de paper [@Shaffer2017] is heel uitgebreid, later terugkeren om de relevante informatie uit te filteren



#### Time domain TODO

A way to measure HRV is in the time domain, meaning that we look at the time in between heart beats and derive metrics from the difference.

 - SDNN
 - SDRR
 - SDANN
 - SDNNI
 - RMSSD
 - HTI


Therefore, 60 seconds appears to be an acceptable recording time for lnRMSSD data collection in col- legiate athletes. [@Esco2014]

#### Frequency domain TODO

Various oscillations have been measured with a frequency ranging from seconds to >24 hours and can be roughly grouped into different bands (see table \ref{hrv_freq}). The LF and HF bands are significant because their oscillations can be affected by breathing rythm. More specifically, the LF band is affected by slow breaths (3 to 9 per minute) and the HF band is affected by fast breathing (9 to 24 per minut)e

Name                            Period                  Actors
----                            ------                  ------
Ultra Low (ULF)                 5 min - 24 hrs          
Very Low (VLF)                  25 sec - 300 sec
Low (LF)                        7 sec - 25 sec
High (HF) or Respiratory band   <7 sec

Table: frequency bands of Heart Rate variability. \label{hrv_freq}

 - LF/HF ratio



#### Contextual Factors TODO

#### Subject Variables TODO



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
