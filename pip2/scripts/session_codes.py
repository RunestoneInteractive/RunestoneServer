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
sessions[2] = ["GeneralIntro/intro-TheWayoftheProgram.rst", "GeneralIntro/Algorithms.rst", "GeneralIntro/ThePythonProgrammingLanguage.rst", "GeneralIntro/SpecialWaystoExecutePythoninthisBook.rst", "GeneralIntro/MoreAboutPrograms.rst", "GeneralIntro/WhatisDebugging.rst", "GeneralIntro/Syntaxerrors.rst", "GeneralIntro/RuntimeErrors.rst", "GeneralIntro/SemanticErrors.rst", "GeneralIntro/ExperimentalDebugging.rst", "GeneralIntro/FormalandNaturalLanguages.rst", "GeneralIntro/ATypicalFirstProgram.rst", "GeneralIntro/Comments.rst", "GeneralIntro/Glossary.rst"]
sessions[2] += ["SimplePythonData/intro-VariablesExpressionsandStatements.rst", "SimplePythonData/Values.rst", "SimplePythonData/Operators.rst", "SimplePythonData/FunctionCalls.rst", "SimplePythonData/DataTypes.rst", "SimplePythonData/Typeconversionfunctions.rst", "SimplePythonData/Variables.rst", "SimplePythonData/VariableNamesandKeywords.rst", "SimplePythonData/StatementsandExpressions.rst", "SimplePythonData/OrderofOperations.rst", "SimplePythonData/Reassignment.rst", "SimplePythonData/UpdatingVariables.rst", "SimplePythonData/Input.rst", "SimplePythonData/Glossary.rst", "SimplePythonData/Exercises.rst"]
sessions[3] = ["PythonTurtle/intro-HelloLittleTurtles.rst", "PythonTurtle/OurFirstTurtleProgram.rst", "PythonTurtle/InstancesAHerdofTurtles.rst", "PythonTurtle/ObjectInstances.rst"]
sessions[4] = ["Sequences/intro-Sequences.rst", "Sequences/OperationsonStrings.rst", "Sequences/IndexOperatorWorkingwiththeCharactersofaString.rst", "Sequences/OperationsandStrings.rst", "Sequences/StringMethods.rst", "Sequences/Length.rst", "Sequences/TheSliceOperator.rst", "Sequences/StringsareImmutable.rst", "Sequences/Theinandnotinoperators.rst", "Sequences/Characterclassification.rst", "Sequences/Lists.rst", "Sequences/ListValues.rst", "Sequences/ListLength.rst", "Sequences/AccessingElements.rst", "Sequences/ListMembership.rst", "Sequences/ConcatenationandRepetition.rst", "Sequences/ListSlices.rst", "Sequences/ListsareMutable.rst", "Sequences/ListDeletion.rst", "Sequences/ObjectsandReferences.rst", "Sequences/Aliasing.rst", "Sequences/CloningLists.rst", "Sequences/ListMethods.rst", "Sequences/AppendversusConcatenate.rst", "Sequences/SplitandJoin.rst", "Sequences/Glossary.rst", "Sequences/Exercises.rst"]
sessions[5] = ["Iteration/intro-Iteration.rst", "Iteration/TheforLoop.rst", "Iteration/FlowofExecutionoftheforLoop.rst", "Iteration/Stringsandforloops.rst", "Iteration/TraversalandtheforLoopByIndex.rst", "Iteration/Listsandforloops.rst", "Iteration/TheAccumulatorPattern.rst", "Iteration/TheAccumulatorPatternwithStrings.rst", "Iteration/Glossary.rst", "Iteration/Exercises.rst"]
sessions[6] = ["Selection/BooleanValuesandBooleanExpressions.rst", "Selection/Logicaloperators.rst", "Selection/PrecedenceofOperators.rst", "Selection/ConditionalExecutionBinarySelection.rst", "Selection/OmittingtheelseClauseUnarySelection.rst", "Selection/Nestedconditionals.rst", "Selection/Chainedconditionals.rst", "Selection/Glossary.rst", "Selection/Exercises.rst"  
]
sessions[6]+= ["Files/intro-WorkingwithDataFiles.rst", "Files/FindingaFileonyourDisk.rst", "Files/ReadingaFile.rst", "Files/AlternativeFileReadingMethods.rst", "Files/Iteratingoverlinesinafile.rst", "Files/WritingTextFiles.rst", "Files/Glossary.rst", "Files/Exercises.rst", "Installation/FirstSteps.rst"]


f = open('session_codes.txt', 'w')
g = open('json_sessin_codes.txt', 'w')

for k in sessions:
    codes = get_codes(sessions[k])
    #print "session%d\t%d\t%s" % (k, len(codes), ', '.join(codes))
    f.write("session%d\t%d\t%s\n" % (k, len(codes), ', '.join(codes)))
    g.write("session%d\t%d\t%s\n" % (k, len(codes), codes))

f.close()
g.close()