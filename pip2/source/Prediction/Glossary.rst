..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Glossary
--------


.. glossary::

    classifier
      A function that takes an object as input and assigns a label from a predefined set of alternatives

    default label
      In a rule-based classifier, the default label is the one that is returned if none of the classification rules applies. 

    default rule
      In a rule-based classifier/predictor, the default rule is the one that determines the output if none of the other rules are applicable. 

    overfitting
      Creating a classifier that performs very well on the training data, by using properties of the training data in way that isn't very useful when trying to apply the classifier to other data.
        
    predictor
      A function that takes an object as input and assigns a value to it that is a prediction of some property of it.
    
    rule-based classifier
      A classifer that includes an ordered list of rules. The first rule whose preconditions are met determines the label that is returned.
    
    test set
      A set of objects, not used during the training process, whose correct labels or properties is known and are used to assess whether a classifier/predictor is producing good outputs. 
    
    training data
      A set of objects whose correct labels or properties is known and are used to "train" the classifier to perform well. For example, the training data might be used to create rules in a rule-based classifier.
    
   