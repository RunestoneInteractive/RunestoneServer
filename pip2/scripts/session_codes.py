## This file is a utility for finding the divids associated with particular class sessions, in order to do checkmark grading
import psycopg2
import connection_string
# make DB connection; import connection string from other file,
# "dbname= user= password=" 
conn = psycopg2.connect(connection_string.connection)
cur = conn.cursor()

def get_codes(fnames):
    res = []
  
    for fname in fnames:
        fname = fname[:-4]  # get rid of '.rst'
        # append the URL for the subchapter as an activity, so that when the user opens that subchapter, it counts as an activity
        res.append("/runestone/static/pip2/" + fname + ".html")
        
        # extract the Chapter and Subchapter labels
        try:
            [ch, sub_ch] = fname.split("/")
        except:
            print fname
        # get all the div_ids for problems in the chapter and append them as well
        cur.execute("select div_id from div_ids where chapter = %s and subchapter = %s", (ch, sub_ch))
        for row in cur.fetchall():
            res.append(row[0])
    return res

# For each session, provide a list of subchapter .rst files (find them in the toc.rst file)

sessions = {}
sessions[1] = ["GeneralIntro/intro-TheWayoftheProgram.rst", "GeneralIntro/Algorithms.rst", "GeneralIntro/ThePythonProgrammingLanguage.rst", "GeneralIntro/SpecialWaystoExecutePythoninthisBook.rst", "GeneralIntro/MoreAboutPrograms.rst", "GeneralIntro/WhatisDebugging.rst", "GeneralIntro/Syntaxerrors.rst", "GeneralIntro/RuntimeErrors.rst", "GeneralIntro/SemanticErrors.rst", "GeneralIntro/ExperimentalDebugging.rst", "GeneralIntro/FormalandNaturalLanguages.rst", "GeneralIntro/ATypicalFirstProgram.rst", "GeneralIntro/Comments.rst", "GeneralIntro/Glossary.rst"]
sessions[2] = ["SimplePythonData/intro-VariablesExpressionsandStatements.rst", "SimplePythonData/Values.rst", "SimplePythonData/Operators.rst", "SimplePythonData/FunctionCalls.rst", "SimplePythonData/DataTypes.rst", "SimplePythonData/Typeconversionfunctions.rst", "SimplePythonData/Variables.rst", "SimplePythonData/VariableNamesandKeywords.rst", "SimplePythonData/StatementsandExpressions.rst", "SimplePythonData/OrderofOperations.rst", "SimplePythonData/BooleanValuesandBooleanExpressions.rst", "SimplePythonData/Logicaloperators.rst", "SimplePythonData/PrecedenceofOperators.rst", "SimplePythonData/Reassignment.rst", "SimplePythonData/UpdatingVariables.rst", "SimplePythonData/Input.rst", "SimplePythonData/Glossary.rst", "SimplePythonData/Exercises.rst"]
sessions[3] = ["PythonTurtle/intro-HelloLittleTurtles.rst", "PythonTurtle/OurFirstTurtleProgram.rst", "PythonTurtle/InstancesAHerdofTurtles.rst", "PythonTurtle/ObjectInstances.rst"]
sessions[4] = ["Sequences/intro-Sequences.rst", "Sequences/OperationsonStrings.rst", "Sequences/IndexOperatorWorkingwiththeCharactersofaString.rst", "Sequences/OperationsandStrings.rst", "Sequences/StringMethods.rst", "Sequences/Length.rst", "Sequences/TheSliceOperator.rst", "Sequences/StringsareImmutable.rst", "Sequences/Theinandnotinoperators.rst", "Sequences/Characterclassification.rst", "Sequences/Lists.rst", "Sequences/ListValues.rst", "Sequences/ListLength.rst", "Sequences/AccessingElements.rst", "Sequences/ListMembership.rst", "Sequences/ConcatenationandRepetition.rst", "Sequences/ListSlices.rst", "Sequences/ListsareMutable.rst", "Sequences/ListDeletion.rst", "Sequences/ObjectsandReferences.rst", "Sequences/Aliasing.rst", "Sequences/CloningLists.rst", "Sequences/ListMethods.rst", "Sequences/AppendversusConcatenate.rst", "Sequences/SplitandJoin.rst", "Sequences/Glossary.rst", "Sequences/Exercises.rst"]
sessions[5] = ["Iteration/intro-Iteration.rst", "Iteration/TheforLoop.rst", "Iteration/FlowofExecutionoftheforLoop.rst", "Iteration/Stringsandforloops.rst", "Iteration/TraversalandtheforLoopByIndex.rst", "Iteration/Listsandforloops.rst", "Iteration/TheAccumulatorPattern.rst", "Iteration/TheAccumulatorPatternwithStrings.rst", "Iteration/Glossary.rst", "Iteration/Exercises.rst"]
sessions[6] = ["Selection/BooleanValuesandBooleanExpressions.rst", "Selection/Logicaloperators.rst", "Selection/PrecedenceofOperators.rst", "Selection/ConditionalExecutionBinarySelection.rst", "Selection/OmittingtheelseClauseUnarySelection.rst", "Selection/Nestedconditionals.rst", "Selection/Chainedconditionals.rst", "Selection/Glossary.rst", "Selection/Exercises.rst"  
]
sessions[6]+= ["Files/intro-WorkingwithDataFiles.rst", "Files/FindingaFileonyourDisk.rst", "Files/ReadingaFile.rst", "Files/AlternativeFileReadingMethods.rst", "Files/Iteratingoverlinesinafile.rst", "Files/WritingTextFiles.rst", "Files/Glossary.rst", "Files/Exercises.rst", "Installation/FirstSteps.rst", "Unix/CommandPrompt.rst", "Unix/FoldersAndPaths.rst"]
sessions[7] = ["Dictionaries/intro-Dictionaries.rst", "Dictionaries/Dictionaryoperations.rst", "Dictionaries/Dictionarymethods.rst", "Dictionaries/Aliasingandcopying.rst", "Dictionaries/Glossary.rst", "Dictionaries/Exercises.rst"]
sessions[8] = ["DictionaryAccumulation/intro-AccumulatingMultipleResultsInaDictionary.rst", "DictionaryAccumulation/AccumulatingResultsFromaDictionary.rst", "DictionaryAccumulation/AccumulatingaMaximumValue.rst", "DictionaryAccumulation/AccumulatingtheBestKey.rst", "DictionaryAccumulation/Exercises.rst", "Unix/lessCommand.rst"]
sessions[9] = ["Functions/FunctionDefinitions.rst", "Functions/FunctionInvocation.rst", "Functions/FunctionParameters.rst", "Functions/Returningavaluefromafunction.rst", "Functions/Afunctionthataccumulates.rst", "Functions/DecodingaFunction.rst", "Functions/MethodInvocations.rst", "Functions/Variablesandparametersarelocal.rst", "Functions/GlobalVariables.rst", "Functions/Functionscancallotherfunctions.rst", "Functions/FlowofExecutionSummary.rst", "Functions/Printvs.return.rst", "Functions/PassingMutableObjects.rst", "Functions/SideEffects.rst", "Functions/Glossary.rst"]
sessions[10] = ["IndefiniteIteration/intro-indefiniteiteration.rst", "IndefiniteIteration/ThewhileStatement.rst", "IndefiniteIteration/listenerLoop.rst", "Debugging/intro-HowtobeaSuccessfulProgrammer.rst", "Debugging/BeginningtipsforDebugging.rst", "Debugging/KnowyourerrorMessages.rst", "Debugging/Summary.rst", "BuildingAProgram/TheStrategy.rst", "BuildingAProgram/UnderstandingCode.rst"]
sessions[11] = ["OptionalAndKeywordParameters/OptionalParameters.rst", "OptionalAndKeywordParameters/KeywordParameters.rst", "OptionalAndKeywordParameters/exercises.rst"]
sessions[12] = ["Tuples/Tuples.rst", "Tuples/TuplePacking.rst", "Tuples/TuplesasReturnValues.rst", "Tuples/TupleAssignmentwithunpacking.rst", "Tuples/UnpackingDictionaryItems.rst", "Tuples/Glossary.rst", "Tuples/Exercises.rst", "NestedData/ListswithComplexItems.rst", "NestedData/NestedDictionaries.rst", "NestedData/NestedIteration.rst"]
sessions[13] =  ["Sort/intro-SortingwithSortandSorted.rst", "Sort/Optionalreverseparameter.rst", "Sort/Optionalkeyparameter.rst", "Sort/Anonymousfunctionswithlambdaexpressions.rst", "Sort/SortingaDictionary.rst", "Sort/Glossary.rst", "Sort/Exercises.rst"]
sessions[14] = ["Prediction/intro-prediction.rst", "Prediction/hangman_guesser.rst", "Prediction/rule-based.rst", "Prediction/shannon_guesser.rst", "Prediction/training.rst", "Prediction/evaluation.rst"]  
sessions[15] = ["PythonModules/intro-ModulesandGettingHelp.rst", "PythonModules/Therandommodule.rst", "PythonModules/Glossary.rst", "PythonModules/Exercises.rst"]
sessions[16] = ["StringFormatting/intro-PrintinginPython2.7.rst", "StringFormatting/Interpolation.rst", "StringFormatting/CSV.rst", "StringFormatting/Exercises.rst"]
sessions[17] = ["RESTAPIs/intro.rst", "RESTAPIs/RequestURLs.rst", "RESTAPIs/jsonlib.rst", "RESTAPIs/unicode.rst", "RESTAPIs/flickr.rst"]
sessions[18] = ["Classes/intro-ClassesandObjectstheBasics.rst", "Classes/ObjectsRevisited.rst", "Classes/UserDefinedClasses.rst", "Classes/ImprovingourConstructor.rst", "Classes/AddingOtherMethodstoourClass.rst", "Classes/ObjectsasArgumentsandParameters.rst", "Classes/ConvertinganObjecttoaString.rst", "Classes/InstancesasReturnValues.rst", "Classes/sorting_instances.rst", "Classes/Glossary.rst", "Classes/Exercises.rst"]
sessions[19] = ["Assignments/session21.rst"]
sessions[20] = ["AdvancedAccumulation/intro.rst", "AdvancedAccumulation/map.rst", "AdvancedAccumulation/filter.rst", "AdvancedAccumulation/listcomp.rst", "AdvancedAccumulation/reduce.rst", "AdvancedAccumulation/zip.rst", "AdvancedAccumulation/exercises.rst"]
sessions[21] = []
sessions[22] = ["Testing/intro-TestCases.rst", "Testing/TestCasesRevisited.rst", "Testing/Testingfunctions.rst", "Testing/Testingclasses.rst", "Testing/Glossary.rst"]
sessions[23] = ["NestedData/DebuggingNestedData.rst"]
f = open('session_codes.txt', 'w')
g = open('json_sessin_codes.txt', 'w')

for k in sessions:
    codes = get_codes(sessions[k])
    #print "session%d\t%d\t%s" % (k, len(codes), ', '.join(codes))
    f.write("session%d\t%d\t%s\n" % (k, len(codes), ', '.join(codes)))
    g.write("session%d\t%d\t%s\n" % (k, len(codes), codes))

f.close()
g.close()