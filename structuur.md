# introduction

# background
 
## Fysiologische werking van het hart
 - relevante uitleg samenstellen uit het "Anatomy & Physiology" textbook
 - Modelling heart rate kinetics
 - Analvsis of Heart Rate Dynamics During Exkrcise
 - Exercise and the autonomic nervous system.

Er wordt een overzicht gegeven over de functionaliteit van het hart, en een introductie in de termen die verder in de thesis gebruikt worden. Er wordt extra focus gelegd op het effect van fysieke inspanning op hartslag, en andere relevante info om het concept "fitheid" te verduidelijken. 

## metrieken

### Accelerometer

Dit is een moeilijke metriek om te betrekken, aangezien dit bijna enkel bruikbaar is in het geval van lopen. In deze sectie onderzoeken we in welke mate de accelerometer gebruikt kan worden in andere gevallen, en of dit een substantieel voordeel is om te betrekken in het algoritme.

### Verschillende soorten heartrate
 - Determining target heart rate for exercising in a cardiac rehabilitation program: a retrospective study.
 - Relationship between resting heart rate, blood pressure and pulse pressure in adolescents
 - Post-exercise heart-rate recovery correlates to resting heart-rate variability in healthy men

Heart Rate vs Heart Rate Variability (HRV)

Maximum heart rate bepalen
Resting heart rate bepalen -> metriek voor fitness
 -> Heart rate reserve deriveren
 -> Target heart rate opstellen met Karvonen method
Heart Rate Recovery -> metriek voor fitness
Heart rate variability -> metriek voor fitness

Hartslag kunnen we zelf meten. Momenteel nog niet accuraat genoeg om HRV te bepalen, maar in het onderzoek gaan we er van uit dat het wel mogelijk is. Zie sectie `Gevolgen van inaccurate metingen`

Dit zijn allemaal vaak gebruikte metrieken in medische literatuur, en komen vaak terug in het bepalen van inspanning en fysieke fitheid. Deze sectie overloopt ze allemaal, hun significantie in de context van dit onderzoek, en waar ze gebruikt worden.

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

Het probleem moet opgelost worden in de context van wearables. Er wordt een marktonderzoek gedaan naar de huidige markt, waar de processing power en accuraatheid van sensoren onderzocht. In de verdere secties wordt er dieper ingegaan op de gevolgen van deze limitaties.

Het is vrij onrealistisch om een volwaardig ML algoritme puur op de chip van een smartwatch te draaien. Er wordt dus ook onderzoek gedaan naar de mogelijkheid om deze berekeningen te offloaden naar een gepaarde smartphone, een eigen server (SaaS), of exotischere mogelijkheden om dit op te lossen.

### gevolgen van minimale computationele kracht

Zelfs als de berekeningen offloaded worden, gaat er nog steeds rekening gehouden moeten worden met minimale computationele kracht. Er wordt onderzocht welke ML subcategorien bestaan die functioneel blijven met weinig berekeningen.

### gevolgen van inaccurate metingen
 - Comparison of Polar M600 Optical Heart Rate and ECG Heart Rate during Exercise
 - Enabling Smartphone-based Estimation of Heart Rate
 - Can Wearable Devices Accurately Measure Heart Rate Variability? A Systematic Review

wearables zijn niet altijd even accuraat en kunnen een niveau van onzekerheid in de metingen bevatten. (specifiek, niet accuraat genoeg voor HRV en RR-interval te meten tijdens fysieke inspanning). Om dit te vermijden wordt de abstractie gemaakt naar "ideale" gesimuleerde hartmetingen, en doen we een onderzoek naar de verschillen tussen deze ideale simulatie en de reele metingen. Zo is de uiteindelijke fitnesscoach tevens futureproof aangezien het niet onrealistisch is dat toekomstige wearables wel deze accuraatheid bevatten.

## Fitheid

### Hoe manifesteert fitheid zichzelf

We onderzoeken het verschil tussen een fitte persoon en een onfitte persoon op fysiologisch vlak, en trekken conclusies over wat wel en niet relevant is voor ons programma

### Hoe wordt fitheid getrained
 - Recovery and performance in sport: Consensus statement
 - Overtraining syndrome

Functional overreaching
Overtraining
trainingsritme

# Probleemstelling

Enerzijds een optimate hartslagsimulator vinden of aanpassen aan de noden van het onderzoek (niet te complex maken, moet enkel complex genoeg zijn zodat de fitnesscoach geanalyseerd kan worden)

anderzijds een fitnesscoach die in staat is om op basis van verschillende metrieken, gedriveerd van enkel en alleen hartslag en user input, een fitnesscore toe kan wijzen. Het hoofddoel is om op basis van de historiek van deze fitness-score een adequaat trainingschema op te stellen, rekening houdend met de voorkeur die de gebruiker ook ingegeven heeft (aanbevelingsysteem) 

# Overzicht van de Hartslag-simulator
https://archive.physionet.org/challenge/2002/generators/

init waarbij we parameters geven aan een commanda, die dan een persoonprofiel kan creeren. Dit profiel geeft een lijst van bpm-metingen terug. we kunnen met commandos dit profiel ook verschillende niveaus aan fysieke intensiteit laten beleven, en het profiel fitter of minder fit maken.

# Overzicht van de fitnesscoach

## detectie van huidige status
in rust, actief, hoge fysieke inspanning, (slapen?)

## base level fitness bepalen in dagdagelijks leven
 - Long Short-Term Network Based Unobtrusive Perceived Workload Monitoring with Consumer Grade Smartwatches in the Wild

met behulp van permanente monitoring en andere variabelen zoals besproken in onderdeel `metrieken`. Dit onderdeel moet in staat zijn om het _verbeteren_ van de Base Level Fitness te detecteren.

## realtime feedback tijdens trainingsessie


## trainingsplanning opstellen (aanbevelingsysteem)


## gebruikte technieken

# resultaten

# conclusies