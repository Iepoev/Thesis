\includepdf[pages=-]{source/figures/titel.pdf}


\pagenumbering{roman}


## Abstract (Dutch) {.unnumbered}

### Methode {.unnumbered}

Het doel van deze masterthesis is om machine learning te gebruiken voor een digitale personal coach te ontwikkelen. 2 onderdelen van deze coach zijn geïsoleerd: een model dat de huidige activiteit van een gebruiker kan classificeren en een model dat de cardiovasculaire fitness van de gebruiker kan meten. De belangrijkste metriek gebruikt is hartslagvariabiliteit. HSV is ruim onderzocht in de medische sector in de context van hartziektes en hartaandoeningen. Deze thesis poogt deze bestaande research te hergebruiken en toe te passen op cardiovasculaire fitness en machine learning. 

Gezonde jongvolwassenen werden gevraagd om een fitness-regime te fietsen op een hometrainer, hun hartslage werd gemeten en een aantal meta-data punten werden genoteerd. In totaal bestaat de dataset uit 23 testpersonen, voor een totaal van \~95000 hartslagen.

### Resultaten {.unnumbered}

De volgende netwerken werden gestest voor de classificatie van de huidige activiteit-staat: LSTM (\~58% accuraatheid), Deep LSTM (\~65% accuraatheid), DeepHeart (\~62% accuraatheid), DeepHeartV2 (\~75% accuraatheid), TCN (\~85% accuraatheid). De dataset voor het trainen van het fitheid-niveau model bleek te klein te zijn voor een resultaat te bereiken.

### Conclusie {.unnumbered}

De voorgestelde netwerken slaagden er in om tot \~85% accuraatheid te bereiken voor de activiteit-staat classification. Dit is een redelijk positief resultaat, maar nog niet toepasbaar voor een matuur product.

Echter, hoewel het onmogelijk is om de validiteit van de gebruikte methoden volledig aan te tonen totdat meer data verzameld is, beide onderdelen werden onderzocht en gevalideerd met behulp van vaak-geciteerde en collegiaal getoetste studies.

\newpage

## Abstract (English) {.unnumbered}

### Method {.unnumbered}

The goal of this master thesis is to use machine learning to develop a digital personal coach for sport activities. 2 subgoals have been isolated: A model capable of classifying the activity state of the user and a model to gauge the cardiovascular fitness level of the user. The primary measurement used is Heart Rate Variability. HRV has been a subject of research in the medical community and can be used to predict various cardiovascular diseases or conditions. This thesis attempts to reapproriate the existing HRV research for cardiovascular fitness and machine learning.

Healthy young adults were asked to perform a specific fitness training session on a stationary bicycle, their heart rate response was measured and various meta-datapoints were noted. In total 23 test subjects were added to the data set, resulting in \~95.000 timesteps of hearbeat data.

### Results {.unnumbered}

The following models were tested for activity state classification: LSTM (\~58% accuracy), Deep LSTM (\~65% accuracy), DeepHeart (\~62% accuracy), DeepHeartV2 (\~75% accuracy), TCN (\~85% accuracy). The number of participants in the study was too little to develop the base-level fitness regression.

### Conclusion {.unnumbered}

The proposed networks managed to achieve up to \~85\% accuracy on activity state classification. This is a fairly positive result, but not yet applicable for real-world scenarios. 

However, while it is impossible to fully prove the validity of the applied methods until more data is gathered, both subgoals were explored and validated using heavily cited, peer-reviewed studies.

\newpage


## Extended abstract {.unnumbered}

### Background {.unnumbered}

People who practice sports occasionally, often have no or very limited support and guidance. People can download a fitness scheme or app from the internet, but these schemes are rarely personalized to the physical capabilities of that person. Moreover, these schemes are usually static and do not take into account the real progress that a user has made or personal goals. Nowadays, the technological advances allow a more accurate monitoring of the user. Smart watches have become more and more popular. Heart rate sensors are becoming cheap and commonplace. Computational power of wearables and smartphones is increasing, which makes running complex tasks such as light-weight machine learning more of a reality.

### Method {.unnumbered}

The goal of this master thesis is to research the possibility of using machine learning to develop a digital personal coach for sport activities. 5 Subgoals were determined to be required to achieve this goal, 2 of which have been isolated for development. 

 - A model capable of classifying the state of the user. Are they resting, active, recovering, under intense exertion, ...
 - A model to gauge the cardiovascular fitness level of the user.

The primary measurement used is Heart Rate Variability. This is the miniscule variability in time between heartbeats and is the result of a multitude of complex interactions between various hormonal and nervous systems of the body. HRV has been a subject of research in the medical community and can be used to predict various cardiovascular diseases or conditions. Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning.

In this master thesis the Polar H7 (a HRV-capable chest strap) is used to measure heart rate data from test subjects. Healthy young adults were asked to perform a specific fitness training session on a Kettler ergometer x3, their heart rate response was measured and various meta-datapoints were noted. A Polar plug-in adapter was used to synchronise the measurements between the chest strap and the stationary bicycle. In total 27 test subjects were gathered, of which 23 were able to fully complete the session, resulting in \~95.000 timesteps of hearbeat data.

From the heart rate measurements extra features were engineered based on the established relevancy to physical fitness. These features were then labeled and used as training data for the heart rate classifier. For the base-level fitness regression, a formula is established to give a "fitness score" based on results of the test subject. With some post-processing the heart rate measurements are reduced to a fixed amount of datapoints as input. Multiple deep neural networks are tested and evaluated for the classifier and regression tasks. 

### Results {.unnumbered}

For the activity state classification task, the proposed networks stem from either natural language processing or earlier experimentations involving machine learning and heart rate data. The following accuracies were achieved:

Model          Accuracy
-----          --------
LSTM           \~58%
Deep LSTM      \~65%
DeepHeart      \~62%
DeepHeartV2    \~75%
TCN            \~85%

The number of participants in the study was too little to develop the base-level fitness regression. Additional test subjects would be required for a adequate conclusion.

### Conclusion {.unnumbered}

The proposed networks managed to achieve up to \~85\% accuracy on activity state classification. This is a fairly positive result, but not yet applicable for real-world scenarios. 

However, while it is impossible to fully prove the validity of the applied methods until more data is gathered, both subgoals were explored and validated using heavily cited, peer-reviewed studies.

\newpage

## Verlengd abstract  {.unnumbered}

### Achtergrond {.unnumbered}

Personen die af en toe sporten, krijgen vaak weinig tot geen ondersteuning en begeleiding. Deze personen kunnen een fitness-schema of app downloaden van het internet, maar deze schemas zijn zelden gepersonaliseerd op basis van de fysieke capabiliteiten van de gebruiker. Daarbovenop zijn deze schemas vaak statisch en houden ze geen rekening met de vooruitgang die de gebruiker boekt of de persoonlijke doelen van de gebruiker. Hedendaagse techonologische vooruitgang heeft er voor gezorgd dat accurate meting van de gebruiker gemakkelijk en bereikbaar zijn. Hartslagsensoren worden goedkoper en wijder gebruikt, de rekenkracht van deze draagbare toestellen en smartphones neemt gestaag toe, wat het steeds realistischer maakt om complexe taken (zoals simpele machine learning taken) hierop uit te voeren.

### Methode {.unnumbered}

Het doel van deze masterthesis is om machine learning te gebruiken voor een digitale personal coach te ontwikkelen. 5 onderdelen werden geïsoleerd, waarven er uiteindelijk 2 uitgewerkt zijn:

 - Een model dat de huidige activiteit van een gebruiker kan classificeren. Is de gebruiker in rust, actief, aan het recuperen, onder intense inspanning, ...?
 - Een model dat de cardiovasculaire fitness van de gebruiker kan meten. 

De belangrijkste metriek gebruikt is hartslagvariabiliteit. Dit is de miniscule variabiliteit in tijd tussen hartslagen en is het resultaat van een groot aantal complexe interacties tussen verschillende hormonale systemen en zenuwstelsels. HSV is ruim onderzocht in de medische sector in de context van hartziektes en hartaandoeningen. Nieuwe generatie hartslagmonitoren zijn in staat om deze HSV te meten op een niveau dat medische electrocardiogram-apparatuur bijna evenaart. Het is de opportune tijd om deze bestaande research pogen te hergebruiken en toe te passen op cardiovasculaire fitness en machine learning. 

In de thesis wordt de Polar H7 (een HSV-capabele borstband hartslagmonitor) gebruikt om hartslag data van proefpersonen te meten. Gezonde jongvolwassenen werden gevraagd om een fitness-regime te fietsen op een Kettler Ergometer X3 hometrainer, hun hartslagrespons werd gemeten en een aantal meta-data punten werden genoteerd. Een Polar plugin adapter werd gebruikt om deze data te synchroniseren tussen de borstband en de hometrainer. In totaal werden 27 proefpersonen verzameld, waarvan 23 in staat waren om het volledige regime te voltooien, met ca. 95.000 hartslagen aan data als resultaat.

Van deze hartslagdata werden een aantal features verwerkt, gebaseerd op de gevestigde relevante metrieken voor fysieke fitness. Deze features werden vervolgens gelabeled en gebruikt als trainings data voor de hartslag classificeerder. Voor de fitness-regressie werd een formule ontwikkeld om een "fitness score" toe te kennen aan de proefpersonen op basis van hun resultaten van het regime. Met een kleine hoeveelheid post-processing werd de hartslagdata van een regime verwerkt tot een vaste hoeveelheid datapunten die kan dienen als input. Verschillende netwerken worden getest en geëvalueerd voor beide taken.

### Resultaten {.unnumbered}

Voor de hartslag classificeerder werden netwerken gebruikt die ontwikkeld zijn voor Natural Language Processing, of netwerken die in eerdere experimenten m.b.t. hartslag data gebruikt zijn. De volgende accuraatheid werd behaald:

Model          Accuraatheid
-----          --------
LSTM           \~58%
Deep LSTM      \~65%
DeepHeart      \~62%
DeepHeartV2    \~75%
TCN            \~85%

De dataset voor het trainen van het fitheid-niveau model bleek te klein te zijn voor een resultaat te bereiken. Meer proefpersonen zouden nodig zijn om tot een conclusie te komen voor deze taak.

### Conclusie {.unnumbered}

De voorgestelde netwerken slaagden er in om tot \~85% accuraatheid te bereiken voor de activiteit-staat classification. Dit is een redelijk positief resultaat, maar nog niet toepasbaar voor een matuur product.

Echter, hoewel het onmogelijk is om de validiteit van de gebruikte methoden volledig aan te tonen totdat meer data verzameld is, beide onderdelen werden onderzocht en gevalideerd met behulp van vaak-geciteerde en collegiaal getoetste studies.

\newpage

## Lay summary {.unnumbered}

### Background {.unnumbered}

People who practice sports occasionally, often have no or very limited support and guidance. People can download a fitness scheme or app from the internet, but these schemes are rarely personalized to the physical capabilities of that person. Moreover, these schemes are usually the same for every participant and do not take into account the real progress that a user has made or personal goals. Nowadays, the technological advances allow a more accurate monitoring of the user. Smart watches have become more and more popular. Heart rate sensors are becoming cheap and commonplace. Processing power of these smartwatches and smartphones is increasing, which makes running complex tasks such as light-weight machine learning more of a reality.

### Method {.unnumbered}

The goal of this master thesis is to research the possibility of using AI to develop a digital personal coach for sport activities. Of the components determined to be required to achieve this goal, 2 were researched in this document. 

 - Software capable of determining how active the user is. Are they resting, active, recovering, under intense exertion, ...
 - Software capable of calculating how fit the user is and giving them a "fitness score".

The primary measurement used is Heart Rate Variability. This is the miniscule difference in time between heartbeats. HRV has been a subject of research in the medical field and can be used to predict various heart diseases or conditions. Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade monitors, so the timing is right to attempt to use the existing HRV research for calculating fitness in the human body using machine learning.

In this master thesis the Polar H7 (a HRV-capable chest strap) is used to measure heart rate data from test subjects. Healthy young adults were asked to perform a specific fitness training session on a Kettler ergometer x3, their heart rate response was measured and various extra information about the subject was noted.  In total 27 test subjects were gathered, of which 23 were able to fully complete the session, resulting in \~95.000 heartbeats data.

### On machine learning {.unnumbered}

Machine learning is a type of artificial intelligence where a stack of mathematical "neuron" layers is made to learn by example. Each of these layers is nothing more than an amount of cells, where each cell is able to receive various inputs, perform a calculation, and pass the result of this calculation on to one or more neurons in the next layer. The sequence of layers are called a "network" and are structured so that the output of the very last layer is a class (in the case of classifying networks) or a score (in case of regression networks). There are more possible use-cases of networks but the thesis is limited to these two.

If a network is designed to find the difference between a dog and a cat, we can show it 100 cat pictures and 100 dog pictures. The algorithm does not know which ones are which, but after letting the network decide on its own we can find out which pictures were predicted correctly and which weren't. Through a concept called "backpropagation" we are capable of showing the network where it went wrong so it can adjust its network to better predict this so-called "training data". By repeating this training session over and over with massive amounts of data, the network will eventually be able to accurately classify pictures as "Dog" or "Cat", even pictures that it has never seen before. 
 
In this thesis, the input data is not "Dog" or "Cat" pictures, but instead sequences of the timing measurements of 128 heartbeats. The output is not the type of animal, but rather how active the user was during time of measurement.

In the case of the fitness scorer, the output of the AI is a number roughly corresponding to how fit a user is.

### Results {.unnumbered}

For determining how active the user is, we based ourselves on existing networks, particulary ones designed and used in text recognition, or ones that were made to find heart conditions. Each model is graded on the percentage of sequences it could correctly classify:

Model          Accuracy
-----          --------
LSTM           \~58%
Deep LSTM      \~65%
DeepHeart      \~62%
DeepHeartV2    \~75%
TCN            \~85%

The number of participants in the study was too little to create a network that can give a fitness score. Additional test subjects would be required.

### Conclusion {.unnumbered}

The proposed networks achieved up to \~85\% accuracy. This is a fairly positive result, but not yet up to par for a real-life fitness coach.

However, while it is impossible to fully prove if the applied methods work until more data is gathered, both subgoals were heavily researched and validated using peer-reviewed studies. 

<!-- \pagenumbering{roman} -->
<!-- \setcounter{page}{1}
 -->
