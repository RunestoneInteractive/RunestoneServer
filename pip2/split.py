import os
import shutil
import errno

def splitFiles(filename, directory):
    f = open(filename)
    lines = f.readlines()
    f.close()
     
    os.unlink(filename)

    sectionStart = 0
    startComments = ''
    startCommentsTraversed = False
    topicName=''

    print filename
    newFilename = filename.replace('src_original','source')
    newFilePath = newFilename.rsplit('\\',1)[0]
    print newFilePath
    for idx, val in enumerate(lines):
        if val.startswith('----') or val.startswith('~~~~~'): #a new subsection is identified by ----- or ~~~~~. Enter if when a new subsection starts
            if not startCommentsTraversed: #enters this if only for the first section, to handle the chapter comments
                startComments = ['..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris\n', '    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute\n', '    and/or modify this document under the terms of the GNU Free Documentation\n', '    License, Version 1.3 or any later version published by the Free Software\n', '    Foundation; with Invariant Sections being Forward, Prefaces, and\n', '    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of\n', '    the license is included in the section entitled "GNU Free Documentation\n', '    License".\n','\n']
                for sub_idx, sub_val in enumerate(lines[0:(idx-1)]):
                    if sub_val.startswith('===='): #handle the introduction section of the chapter
                        topicName = removeChars(lines[sub_idx-1].strip(), '\/:*?"-+`,!<>|')
                        newFile = newFilePath+'\\intro-'+topicName.replace(" ", "")+'.rst'
                        ocf.writelines("   "+directory+"/intro-"+topicName.replace(" ", "")+'.rst\n') #write new filename to file, for TOC
                        lines[sub_idx-1] = 'Introduction: '+lines[sub_idx-1]
                        introductionContent = lines[sub_idx-1:(idx-1)]
                        o = open(newFile, 'w')
                        o.writelines(startComments)
                        o.writelines(introductionContent)
                        o.close()
                        break
                topicName = removeChars(lines[idx-1].strip(), '\/:*?"-+`,!<>|')
                startCommentsTraversed = True
                sectionStart = idx-1
            else: #enters this for every other subsection apart from the first one
                newFile = newFilePath+'\\'+topicName.replace(" ", "")+'.rst'
                ocf.writelines("   "+directory+"/"+topicName.replace(" ", "")+'.rst\n') #write new filename to file, for TOC
                o = open(newFile, 'w')
                subSection = lines[sectionStart:(idx-1)]
                o.writelines(startComments)
                o.writelines(subSection)
                o.close()
                topicName = removeChars(lines[idx-1].strip(), '\/:*?"-+`,!<>|')
                sectionStart = idx-1
        elif idx == (len(lines) -1): #enters for the last line, to create last file 
            newFile = newFilePath+'\\'+topicName.replace(" ", "")+'.rst'
            ocf.writelines("   "+directory+"/"+topicName.replace(" ", "")+'.rst\n') #write new filename to file, for TOC
            o = open(newFile, 'w')
            subSection = lines[sectionStart:idx]
            o.writelines(startComments)
            o.writelines(subSection)
            o.close()

def dirEntries(dir_name, subdir, *args):
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if not args:
                fileList.append(dirfile)
            else:
                if os.path.splitext(dirfile)[1][1:] in args:
                    fileList.append(dirfile)
        # recursively access file names in subdirectories
        elif os.path.isdir(dirfile) and subdir:
            fileList.extend(dirEntries(dirfile, subdir, *args))
    return fileList

def removeChars(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value;

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            print('Directory not copied. Error: %s' % e)

include_directories = ['Assignments', 'GeneralIntro', 'SimplePythonData', 'Debugging', 'Sequences', 'Iteration', 'Selection', 'Files', 'Dictionaries', 'Functions', 'Sequences', 'Sort', 'PythonModules', 'Testing', 'NestedData', 'MoreAboutIteration', 'Installation', 'StringFormatting', 'Classes']

allChapterFiles = 'allChapterFiles.txt'
ocf = open(allChapterFiles, 'w')

os.chdir('..')
copy("source", "source_original")
os.chdir('source')

for directory in include_directories: 
    os.chdir(directory)
    fileList = dirEntries(os.getcwd(), True, 'rst')
    for file in fileList:
        splitFiles(file, directory)
        ocf.writelines('\n\n\n')
    os.chdir("..")

ocf.close()
