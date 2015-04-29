Split chapters into sub chapters
================================


The script ``split.py`` splits the rst files for each chapter into multiple rst files for each sub section of that chapter. 
The script first creates a copy of the source folder as source_original, as a backup, if something goes wrong with the script. 
A file ``allChapterFiles.txt`` get created in the same folder as ``split.py``. This lists all the new rst files grouped together by chapters. This can be used to create a new ``toc.rst`` file based on the new structure.

Things to note for Thinkcspy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. You do not need to run the script ``split.py`` again for this course. It has already been executed and the new rst files are available in the ``source`` folder. A backup of the old structure is availble as ``source_original``. 
2. The folder Classes has been split to two seperate chapters - ``ClassesBasics`` and ``ClassesDiggingDeeper`` to maintain a consistent hierarchy or chapters. 
3. A new toc.rst file has been created. 
4. The source folder contains many folders which are not chapters in the book. Hence, the rst files inside those folders should not be splitted. We need to inform the code, the list of chapters, so splitting is performed only for the desired folders. The following code instructs the code, which directories to include:

.. sourcecode:: python
include_directories = ['GeneralIntro', 'SimplePythonData', 'Debugging', 'PythonTurtle', 'PythonModules', 'Functions', 'Selection', 'MoreAboutIteration', 'Strings', 'Lists', 'Files', 'Dictionaries',  'Recursion', 'ClassesBasics', 'ClassesDiggingDeeper'] 

Execute split.py for other courses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provide a new list of directories to be included. The script will look for these directories in the source folder and perform split. 
