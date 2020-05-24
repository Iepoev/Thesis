# Hardware \ref{ch:hardware}


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