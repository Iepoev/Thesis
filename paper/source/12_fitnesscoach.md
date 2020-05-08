# fitnesscoach

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