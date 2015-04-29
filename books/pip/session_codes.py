## This file is a utility for finding the divids associated with particular class sessions, in order to do checkmark grading

def get_codes(fnames):
    res = []
    for fname in fnames:
        f = open("source/" + fname+".rst")
        for lin in f:
            words = lin.split()
            for directive in ["activecode::", "actex::", "mchoicemf::", "mchoicema::", "codelens::"]:
                if directive in words:
                    res.append(words[-1])
    return res

sessions = {}
sessions[2] = ["SimplePythonData/simpledata", "Debugging/debugIntro"]
sessions[3] = ["Sequences/index"]
sessions[4] = ["Iteration/iteration"]
sessions[5] = ["Selection/selection", "Files/files"]
sessions[6] = ["Dictionaries/dictionaries"]
sessions[7] = ["Debugging/debugTracers", "Dictionaries/dictionary_accum"]
sessions[8] = ["Functions/functions"]
sessions[9] = ["Functions/functions2"]
sessions[10] = ["Functions/optionalParams", "Sequences/tuples", "Sort/sorted"]
sessions[11] = ["PythonModules/modules", "Testing/simpleTest", "Functions/functions2"]
sessions[12] = ["NestedData/nested", "MoreAboutIteration/moreiteration"]
sessions[16] = ["Installation/installation"]
sessions[17] = ["Functions/KeywordParams", "StringFormatting/interpolation"]
sessions[18] = ["Assignments/week9"]
sessions[19] = ["Assignments/week9"]
sessions[20] = ["Classes/classesintro"]
sessions[21] = ["Assignments/week10"]
sessions[22] = ["Sequences/listcomprehensions"]
sessions[23] = ["Assignments/week11"]

f = open('session_codes.txt', 'w')
g = open('json_sessin_codes.txt', 'w')

for k in sessions:
    codes = get_codes(sessions[k])
    #print "session%d\t%d\t%s" % (k, len(codes), ', '.join(codes))
    f.write("session%d\t%d\t%s\n" % (k, len(codes), ', '.join(codes)))
    g.write("session%d\t%d\t%s\n" % (k, len(codes), codes))

f.close()
g.close()