# introduction

# background
 
## Fysiologische werking van het hart
 - relevante uitleg samenstellen uit het "Anatomy & Physiology" textbook
 - Modelling heart rate kinetics
 - Analvsis of Heart Rate Dynamics During Exkrcise
 - Exercise and the autonomic nervous system.

Er wordt een overzicht gegeven over de functionaliteit van het hart, en een introductie in de termen die verder in de thesis gebruikt worden. Er wordt extra focus gelegd op het effect van fysieke inspanning op hartslag, en andere relevante info om het concept "fitheid" te verduidelijken.

### Parasympathische werking

### Orthosympatische werking



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

##  smartwatches in context plaatsen
https://www.qualcomm.com/products/wearables
 - Accuracy of smartphone application to monitor heart rate.
 - Comparison of Polar M600 Optical Heart Rate and ECG Heart Rate during Exercise
 - Enabling Smartphone-based Estimation of Heart Rate
 - Can Wearable Devices Accurately Measure Heart Rate Variability? A Systematic Review
 - Improving heart rate variability measurements from consumer smartwatches with machine learning


Het probleem moet opgelost worden in de context van wearables. Er wordt een marktonderzoek gedaan naar de huidige markt, waar de processing power en accuraatheid van sensoren onderzocht. In de verdere secties wordt er dieper ingegaan op de gevolgen van deze limitaties.

Het is vrij onrealistisch om een volwaardig ML algoritme puur op de chip van een smartwatch te draaien. Er wordt dus ook onderzoek gedaan naar de mogelijkheid om deze berekeningen te offloaden naar een gepaarde smartphone, een eigen server (SaaS), of exotischere mogelijkheden om dit op te lossen.

### omgaan met minimale computationele kracht

Zelfs als de berekeningen offloaded worden, gaat er nog steeds rekening gehouden moeten worden met minimale computationele kracht. Er wordt onderzocht welke ML subcategorien bestaan die functioneel blijven met weinig berekeningen.

### omgaan met inaccurate metingen
 - Heart rate variability estimation in photoplethysmography signals using Bayesian learning approach
 - Can PPG be used for HRV analysis?
 - Stressing the accuracy: Wrist-worn wearable sensor validation over different conditions

wearables zijn niet altijd even accuraat en kunnen een niveau van onzekerheid in de metingen bevatten. (specifiek, niet accuraat genoeg voor HRV en RR-interval te meten tijdens fysieke inspanning). Om dit te vermijden wordt de abstractie gemaakt naar "ideale" gesimuleerde hartmetingen, en doen we een onderzoek naar de verschillen tussen deze ideale simulatie en de reele metingen. Zo is de uiteindelijke fitnesscoach tevens futureproof aangezien het niet onrealistisch is dat toekomstige wearables wel deze accuraatheid bevatten.

## Fitheid

### Hoe manifesteert fitheid zichzelf
 - Heart rate variability and aerobic fitness
 - Post-exercise heart-rate recovery correlates to resting heart-rate variability in healthy men
 - Heart rate recovery fast-to-slow phase transition: Influence of physical fitness and exercise intensity
 - Recovery and performance in sport: Consensus statement
 - The development of functional overreaching is associated with a faster heart rate recovery in endurance athletes
 - Resting heart rate variability and heart rate recovery after submaximal exercise

We onderzoeken het verschil tussen een fitte persoon en een onfitte persoon op fysiologisch vlak, en trekken conclusies over wat wel en niet relevant is voor ons programma

### Hoe wordt fitheid getrained
 - Recovery and performance in sport: Consensus statement
 - Overtraining syndrome
 - Overtraining in Resistance Exercise: An Exploratory Systematic Review and Methodological Appraisal of the Literature
 - Functional overreaching: The key to peak performance during the taper?
 - Diagnosis and prevention of overtraining syndrome: an opinion on education strategies
 - Effect of overreaching on cognitive performance and related cardiac autonomic control
 - Does overtraining exist? An analysis of overreaching and overtraining research
 - Training adaptation and heart rate variability in elite endurance athletes: Opening the door to effective monitoring
 - The Multimodal Nature of High-Intensity Functional Training: Potential Applications to Improve Sport Performance
 - Heart rate recovery in elite athletes: the impact of age and exercise capacity
 - Assessing overreaching with heart-rate recovery: What is the minimal exercise intensity required?
 - Is heart rate a convenient tool to monitor overreaching? A systematic review of the literature
 - Overtraining syndrome

Functional overreaching
Overtraining
trainingsritme

# Probleemstelling
 - Measurement, prediction, and control of individual heart rate responses to exercise-basics and options for wearable devices

Enerzijds een optimate hartslagsimulator vinden of aanpassen aan de noden van het onderzoek (niet te complex maken, moet enkel complex genoeg zijn zodat de fitnesscoach geanalyseerd kan worden)

anderzijds een fitnesscoach die in staat is om op basis van verschillende metrieken, gedriveerd van enkel en alleen hartslag en user input, een fitnesscore toe kan wijzen. Het hoofddoel is om op basis van de historiek van deze fitness-score een adequaat trainingschema op te stellen, rekening houdend met de voorkeur die de gebruiker ook ingegeven heeft (aanbevelingsysteem) 

## Overzicht van de Hartslag-simulator
https://archive.physionet.org/challenge/2002/generators/
https://archive.physionet.org/physiobank/database/nsrdb/
https://physionet.org/content/ecgsyn/1.0.0/

init waarbij we parameters geven aan een commanda, die dan een persoonprofiel kan creeren. Dit profiel geeft een lijst van bpm-metingen terug. we kunnen met commandos dit profiel ook verschillende niveaus aan fysieke intensiteit laten beleven, en het profiel fitter of minder fit maken.

## Overzicht van de fitnesscoach

### base level fitness bepalen in dagdagelijks leven
 - Long Short-Term Network Based Unobtrusive Perceived Workload Monitoring with Consumer Grade Smartwatches in the Wild

Streamed, labeled data voor te initialiseren. Streamed, unlabeled data voor de rest

met behulp van permanente monitoring en andere variabelen zoals besproken in onderdeel `metrieken`. Dit onderdeel moet in staat zijn om het _verbeteren_ van de Base Level Fitness te detecteren.

### detectie van huidige status
 - Implicit Context-aware Learning and Discovery for Streaming Data Analytics
 - Detection of functional overreaching in endurance athletes using proteomics
 - On the physiological and psychological differences between functional overreaching and acute fatigue

in rust, actief, hoge fysieke inspanning, (slapen?)

Streamed, unlabeled data. Machine Learning classificatie-probleem met context

In geval van hoge fysieke inspanning zou de gebruiker de optie moeten krijgen om te laten tellen als trainingsessie

### trainingsplanning opstellen (aanbevelingsysteem)


Het systeem weet de volgende dingen:
 - de huidige fitheid van de gebruiker
 - de hoeveelheid rust dat de gebruiker heeft gehad recentelijk
 - welke trainingsessies en de intensiteit van de voorbije trainingsessis van de gebruiker 
 - welke impact ieder type trainingsessie heeft
 - een optimaal trainingschema dat in optimale omstandigheden zo dicht mogelijk gevolgd wordt

Aanbevelingsysteem gebruiken om een top n mogelijke trainingsessie samen te stellen (bvb intensief interval-sprinten, langdurig lopen, hoge-intensiteit cardio-sessie, rustdag, gewichtheffen,...). De gebruiker kan hieruit een kiezen.

### realtime feedback tijdens trainingsessie
 - MiLift: Efficient Smartwatch-Based Workout Tracking Using Automatic Segmentation
 - The Multimodal Nature of High-Intensity Functional Training: Potential Applications to Improve Sport Performance
 - Modelling the HRV response to training loads in elite rugby sevens players
 - Effects of varying training load on heart rate variability and running performance among an Olympic rugby sevens team

Classification probleem: gestreamde hearbeat met een rolling window zegt of de inspanning te hoog of te laag is om het doel van de sessie te bereiken. Machine Learning classificatie-probleem

### Analyseren van een trainingsessie
 - Heart rate recovery after exercise: Relations to heart rate variability and coplexity
 - Ultra-short-term heart rate variability indexes at rest and post-exercise in athletes: Evaluating the agreement with accepted recommendations

Na afronden van een trainingsessie wordt de intensiteit van de sessie berekend en wordt bijgehouden in de historiek zodat er rekening gehouden mee kan worden in het aanbevelingsysteem

### gebruikte technieken

# resultaten

# conclusies