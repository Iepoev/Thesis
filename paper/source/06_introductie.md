# Introduction

People who practice sports occasionally, often have no or very limited support and guidance. People can download a fitness scheme or app from the internet, but these schemes are often not personalized to the physical capabilities of that person. Moreover, these schemes are often static and do not take into account the real progress that a user has made or personal goals. Nowadays, the technological advances allow a more accurate monitoring of the user. Smart watches are become more and more popular. These are equipped with a bunch of sensors such as heart rate sensor, accelerometer, gyroscope, GPS, … These data can be used to monitor the user in detail, and provide a more personalized sport/fitness experience.

## Goal of the thesis

The goal of this master thesis is to design and develop a digital personal coach for sport activities. This personal coach can be implemented as an Android application that uses data from wearables to assess the physical efforts and capabilities of a user. More specifically, in this master thesis the Polar H7 (a chest strap with heart rate sensor) and the Polar M600 (an Android Wear smart watch designed for fitness and sport purposes) can be used. These devices can provide data regarding heart rate and movement (through heart rate sensor, accelerometer and GPS).

The fitness coach consists of 5 elements:
 - at first, a quick physical exam and questionnaires will be used to determine heart rate and fitness values. By relating heart rate data with the intensity of the physical activities, the physical capabilities of the user will be derived.
 
 - A detector recognises the current state of the subject, in rest or active, mild of high intensity,... this is able to prompt the user if he/she wants to start a training session when activity is detected.

 - Once a base fitness level is established, a recommendation system will recommend training sessions based on previously attained result, time since last session,... A variety of possible sessions is presented such as interval training, endurace aerobic training, weight lifting, extra rest day,...

 - During a training session, real-time feedback is provided to guide the user so that the goals of the session are achieved.

 - When a session completes it is analysed and the fitness model of the subject is updated.

## Summary of chapters

**Chapter \ref{ch:goal}** Describes in detail what the problem entails, the challenges that were faced and how they were overcome.

in the next couple of chapters an in depth explanation is given:
 - **Chapter \ref{ch:med}** Will give an overview of the physiology and medical terms relevant to this thesis. 
 - In **Chapter \ref{ch:metrics}** We go further in depth and describe how this knowledge can be transformed into useful metrics for our problem. 
 - **Chapter \ref{ch:hardware}** analyses that current state of the art of wearables and discusses its strenghts and limits for measuring these metrics.

These are followed by an overview of the implementations:
 - **Chapter \ref{ch:hr_sim}** 
 - **Chapter \ref{ch:fitnesscoach}** 

To conclude, the implementation is tested in **Chapter \ref{ch:val}** and a detailed conclusion is made in **Chapter \ref{ch:conclusion}** 
