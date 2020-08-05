# Hardware \label{ch:hardware}


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



# Fitnesscoach \label{ch:fitnesscoach}

## Overzicht van de fitnesscoach

### base level fitness bepalen in dagdagelijks leven
 - Long Short-Term Network Based Unobtrusive Perceived Workload Monitoring with Consumer Grade Smartwatches in the Wild

### detectie van huidige status
 - Implicit Context-aware Learning and Discovery for Streaming Data Analytics
 - Detection of functional overreaching in endurance athletes using proteomics
 - On the physiological and psychological differences between functional overreaching and acute fatigue

feature extraction -> feature engineering

Concept drift [@Mulinka2018]

Adaptive learning

RNN -> LSTM -> Transformers?

Neural history compressor

Sequence Classification

FitzHugh Nagumo model [@Madl2016]

cycle length dependence (1).


LSTM

TCN

ConvLSTM

DeepHeart










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

