
# Conclusion \label{ch:conclusion}

## Learning points

The proposed Machine Learning networks managed to achieve up to \~82\% accuracy on sequenced heartbeat data. This is a fairly positive result, but not yet applicable for real-world scenarios.

Due to the current ministerial decree(s) in relation to the ongoing covid-19 pandemic, the number of participants to the study was unfortunately too limited to see any significant results. The datasets used during training of both subgoals resulted in short epochs, requiring high epoch counts (up to 500 epochs) to achieve a stable result. For the fitness base level regression, this became even more extreme resulting in the failure of the experiment.

However, while it is impossible to fully prove the validity of the applied methods until more data is gathered, both subgoals were explored and validated using heavily cited, peer-reviewed studies. The base level fitness goal in particular is a fairly simple computational task (regression), so the the eventual success of the methodology seems likely.


## Future work

There are several potential directions for extending this thesis. 

Being able to use PPG data from smartwatches would lower barrier of entry, users and test subjects would not have to strap on a special device for testing and could be monitored permanently. Using Pulse Rate Variability measurements instead of Heart Rate Variability measurements requires only minor changes to the code used in this thesis, but requires a completely new test setup.

Currently, the Activity Stage model does not use the potential gains from having the heart beat data streamed to the model. Accuracy could potentially improve by being able to use the previously labeled timesteps instead of only the unlabeled timesteps. So-called "Context Aware Learning" would be able to not only classify the activity state of the user based on short-term sequence data, but it would know a longer term "context" in which the data was generated (An increased heart rate during a High Intensity Interval Training versus running up the stairs during a regular work day) [@Lore2019]. Certain techniques are being discovered to not only classify this context, but also keep track of the "drift" of the context, mostly within the field of Anomaly Detection in streamed data w.r.t. network security [@Mulinka2018] [@Mulinka2019] 

An interesting concept was found but not expanded upon. The FitzHugh Nagumo model is the model of an a biological neuron proposed to account for cardiac impulse propagation. A study was able to achieve promising results by creating a Neural Network Layer based on this model, but these results were unable to be replicated in the experimental models of this thesis [@Madl2016].

The Base Level Fitness regression task is made to combine 2 subgoals (base level fitness \& increase/decrease of fitness) into 1 implementation. The disadvantage now is that tracking increase/decrease of fitness requires performing a predefined training session, which makes the entire coach much less integrable with daily life. Developing a custom solution for this subgoal made to work with unlabeled sequence data would solve this issue.

The implementation of the three remaining subgoals (tracking and coaching the user during a session, compiling a result from past sessions and recommending sessions that optimize fitness training) have not been addressed, but are required for a fully mature fitness coach. Various background information (such as fatigue states) have not been fully applied in the addressed subgoals, but might prove useful when implementing the remaining subgoals.


