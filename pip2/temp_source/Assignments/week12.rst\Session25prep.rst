..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Session 25 prep
---------------

When you create a user-defined class in python, the class should represent a category (type) of objects that all share some properties and operations (methods). Each instance will represent one object of that type.

To help you think about creating a user-defined class, for your final project, I've posed a series of fill-in-the-blank questions. And I've strung the answers to those questions together into a little story about the class you're defining. Think of it as a MadLib, for those of you who know what those are, except the story at the end is supposed to make sense, not make people laugh.

.. actex:: session25_1

   # The name of my class will be...
   example_name = "Dog"
   your_name = ""
   
   # Each instance of my class will represent one...
   example_inst_represents = "dog"
   your_inst_represents = ""
   
   # Each instance of my class will have ... instance variables
   example_inst_var_count = 2
   your_inst_var_count = 0
   
   # Each instance will have instance variables that keep track of...
   example_inst_vars = "how many barks it makes when it barks, and what sound it makes for each bark"
   your_inst_vars = ""
   
   # One method of my class, other than __init__, will be named...
   example_method_name = "bark"
   your_method_name = ""
   
   # When invoked, that method will...
   example_method_description = "print to the output screen the sounds that that dog makes when it barks" 
   your_method_description = ""
   
   print "The name of the example class is %s. Each instance of my class will represent one %s. Each instance will have %d instance variables. The instance variables will keep track of %s. One method of my class, other than __init__, will be named %s. When invoked, that method will %s." % (example_name, example_inst_represents, example_inst_var_count, example_inst_vars, example_method_name, example_method_description)
   print
   print "----"
   print "The name of my class will be %s. Each instance of my class will represent one %s. Each instance will have %d instance variables. The instance variables will keep track of %s. One method of my class, other than __init__, will be named %s. When invoked, that method will %s." % (your_name, your_inst_represents, your_inst_var_count, your_inst_vars, your_method_name, your_method_description)
   
