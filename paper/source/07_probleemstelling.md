
# Introduction \ref{ch:goal}
 - Measurement, prediction, and control of individual heart rate responses to exercise-basics and options for wearable devices
}

## 

## Why only heart rate

## Goal

The goal of this master thesis is to research the possibility of using Machine Learning to develop a digital personal coach for sport activities. It should be able to measure and track the performance of the user and suggest appropriate training sessions that result in an increase in cardiovascular fitness. In ideal conditions, a fully mature fitness coach should therefor be able to:

 - Be able to determine a "base fitness level" of the user during initialisation of the coaching program. This would be a machine learning regression task on labeled, batched sequence data to determine a certain "fitness level score"

 - Be able to determine the increase or decrease of the cardiovascular fitness of the user throught unlabeled monitoring. This would be a machine learning regression task on unlabeled, batched sequence data to update the previously acquired "fitness level score"

 - permanently track the user and classify his/her current state, optionally be able to automatically count periods of increased activity as a workout session. This would be a machine learning multi-label classification task on unlabeled, real-time sequenced data to determine the current exertion leven on a short-term timescale (30-60 seconds).

 - be able to track a user during his/her training session and provide feedback to keep the user in the optimal exertion range. This is a machine learning multi-label classification task on unlabeled, real-time sequence data to determine the current exertion leven on a very short-term timescale (5-10 seconds).

 - compile the result of a workout session to guage the intensity and the effect on the body of the user. At this point it should be able to determine the fatigue state of the user so that the coach can take this into account. This would be a machine learning classification task on labeled, batched sequence data to determine a fatigue state.

 - Suggest the user what kind of workout to perform next and how long to recover from recent workouts. This would be a recommender system task that can accurately predict overreaching in the user.

## scope of the thesis

to limit the scope of this master thesis, only 2 of these goals will be researched in depth

 - A model that can classify the state of the user. Is he/she resting, active, recovering, under intense exertion,...

 - A model to gauge the cardiovascular fitness level of the user.

The primary measurement used is Heart Rate Variability. This is the miniscule variability in time between heartbeats and is the result of a multitude of complex interactions between various hormonal and nervous systems of the body. HRV has been a subject of research in the medical community and can be used to predect various cardiovascular diseases or conditions. Current generation heart rate monitors are able to monitor HRV to a respectable degree compared to medical grade electrocardiogram machines, so the timing is right to attempt to reappropriate the existing HRV research for cardiovascular fitness and machine learning.

## usage of wearables