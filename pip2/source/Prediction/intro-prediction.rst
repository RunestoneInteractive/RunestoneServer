..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _prediction_chap:

Prediction and Classification
-----------------------------

.. index:: prediction, classification, classifier, label, train, binary classification


One common use of data is to train a program to make predictions. For example, a supermarket would like to predict the likely sales of milk in its store, so that it can keep enough inventory to avoid disappointing customers, but not so much that some of the milk goes unsold and spoils. By analyzing past sales, at a particular store and other similar stores, it may be able to produce a predictive model. Some of the features, or independent variables, that help predict upcoming sales might include the recent and predicted future weather and any sale prices the store has advertised. 

Sometimes, computer-based prediction is helpful not just for future events, but as a way to save human labor in analyzing large datasets. For example, suppose a company has just introduced a new product, say a new smartphone model. Lots of blogs and tweets mention the product, perhaps hundreds of thousands of mentions in all. If the company wants to get an overall sense of the sentiment of consumer response to the product, it may want to run a computer program that processes all of posts that mention the product, and compute a sentiment score for each post, with positive scores indicating a favorable reaction and negative scores an unfavorable reaction. We would first have trusted people *label* some posts as to how favorable or unfavorable they are. Those labeled posts would then be used to *train* a prediction program, by identifying that are common in the favorable posts but not in the unfavorable posts. For example, the presence of the word "wonderful" might be an indicator of an overall favorable post while the presence of "disappointed" might indicate an unfavorable post. Once the scoring program is trained, it can be run against all the posts, far more than humans could label by hand.

Classification is a special case of prediction.  In this case, the outcome to be predicted is one of a set of discrete labels. For example, rather than predicting the number of gallons of milk a classifier might output one of three discrete labels, "low", "medium", or "high". Rather than predicting a favorability score for posts, a classifier might predict either "favorable" or "unfavorable". When there are only two possible labels, it is called *binary classification*.

There are a variety of algorithms available for training classifiers and other predictors, and they vary in their mathematical and computational sophistication. Some techniques for training classifiers include decision trees and support vector machines. You might learn about these in a future course on data mining or machine learning.

If you've already had a statistics course that covers linear regression, you have already seen one approach for training a predictor. With regression, you take a table of data, with one column representing the outcome or dependent variable, and the other columns representing features or independent variables. For example, the dependent variable might be milk sales and the independent variables whether conditinos and whether the price is discounted. When you "run a regression", you are using the table of past data as training examples, generating a "best fit" set of coefficients that express how much the values of each of the independent variables contributes to the value of the dependent variable. You can then use those coefficients to make predictions "out of sample", predicting how much milk sell even for a combination of weather and sale prices that has not been directly observed in the past.

In this chapter, we will focus on particularly simple prediction algorithms that consist of an ordered collection of independent if-then rules. They will help you understand the concepts of using data to train a prediction program which then makes predictions. This should provide you with a good foundation for later courses where you may encounter the same idea but using more complicated mathematics and algorithms.
