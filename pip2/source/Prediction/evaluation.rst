
Evaluating a Classifier/Predictor
---------------------------------

.. index:: overfitting, validation, test set

When you use training data to create a classifier or predictor, there is always a danger of *overfitting*, making a predictor that works well on the labeled training data but is not sufficiently general to work on other items. For example, when making a name classifier, you could treat entire names as a feature. You would have a rule that says "Julia" is a female name and another one one that says "Julian" is a male name. If you made one such rule for every labeled name in your training data, and no other rules, your classifier would have perfect accuracy on training data but have no clue how to classify any other names; not very useful.

To prevent tricking ourselves into thinking that we've made a useful classifier when instead we've overfit the training data, the normal practice is to hold out a *test set*. That is, you use part of the labeled data as a training set. Then you see how well the classifier does on the test set, which wasn't used for training.

In the Shannon Game, this isn't particularly a problem. The rest of the text, which hasn't been revealed yet, provides a fair test for the predictor. It can train itself as it goes along, using the already revealed text, without having any kind of unfair advantage.
