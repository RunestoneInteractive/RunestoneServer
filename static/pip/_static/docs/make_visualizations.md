# Using make_visualizations.py to build visualization embeddings

The program `make_visualizations.py` can be used to simplify the task of building visualization embeddings. The user can describe the required details as a `.json` file (a 'Makefile') and `make_visualizations.py` is a 'make' program that will build all the required visualizations and supporting bookkeeping. 

For an example of how to use this program and to embed visualizations we will assume that the current working directory contains the `.html` files that will have visualizations embedded in them, that the sub-directory `examples` contains all the python files that are to be visualized and that the sub-directories `js` and `css` have been created. Further assume `$OPT` is the directory containing the OPT release.

The first step is to copy across some `.js` files and `.css` files.

    cp -r $OPT/js/* js
    cp -r $OPT/css/* css

The next step is to create the Makefile - say `make_viz.json` and to add the required information to the file. An example of such a file is given below. The required visualizations can be built as follows.

    python $OPT/make_visualizations.py make_viz.json

Calling this again will rebuild everything. Alternatively, the program can be used to build visualizations for particular `.html` files listed in `make_viz.json` by listing them at the end of the command. For example

    python $OPT/make_visualizations.py make_viz.json file1.html file3.html

For the example we assume the `.html` files are `file1.html`, `file2.html` and `file3.html` and that `file1.html` will have visualizations for `prog1_1.py` and `prog1_2.py`; `file2.html` will have a visualization for `prog2_1.py`; and `file3.html` will have a visualization for `prog3_1.py`. Further we assume that a local OPT server has been set up at the URL http://my.local.server/visualize.html.

The following is a possible example for `make_viz.json`

    {       
     "visualizer_url": 
           "http://my.local.server/visualize.html",
    
     "default_viz_config": 
           {
             "embeddedMode": true, 
             "codeDivWidth": 500
           },
    
     "file1.html":
           [
             "js/file1.js",
             {
                "examples/prog1_1.py":{},
                "examples/prog1_2.py":{"codeDivWidth": 400}
             }
           ],
     
     # hash to end of line is a comment
     
     "file2.html":
           [
             "js/file2.js",
             {
                "examples/prog2_1.py":{}
             }
           ],
    
     "file3.html":
           [
             "js/file3.js",
             {
                "examples/prog3_1.py":{"codeDivWidth": ""}
             }
           ]
    }

The first entry specifies the location of the server. If this is not present, the default is http://pythontutor.com/visualize.html.

The second entry is the default configuration for the visualization paramenter used for the given html files. If this is not present the visualization parameters are set to the system defaults.

All other top-level entries are for the `.html` files. The information for a given `.html` file consists of a `.js` file in which to put the trace and other bookkeeping information and a dictionary containing information for each program. The key is the file and the value is for visualization parameters. Any parameters given here override the corresponding value for the parameter in `default_viz_config`. The special value of the empty string removes that parameter from `default_viz_config`. In this example, when visualizing `prog1_2.py`, the code textbox width will be reduced to 400 pixels and for `prog3_1.py`, the code textbox width will be set to the system-wide default.

If you already have a visualization set up and you would like to use this approach you will need to remove the OPT dependencies before `<body>` in the `.html` file. When you then run the 'make' program it will re-introduce the dependencies in such a way that subseqent makes will replace this information with the updated information.

At the end of the dependencies information injected into the `.html` file is a comment containing div entries that you can cut-and-paste into the position within the `.html` file where you would like the visualization to appear. The Makefile does not know where this is to be added and so this step needs to be done manually. Re-making this file will not remove this infomation from the body of the file. So, for example, in the header of `file3.html` you should find
the following.

    <!-- Cut and paste the following lines to the place where the visualizations are to be inserted
    
    <div id="prog3_1_pyDiv"></div>
    -->


For reference, we list the possible visualization parameters (with system-wide defaults - based on comments in `pytutor.js`) below.

- heightChangeCallback: the function to call whenever the height of the visualization changes. If using the make program this is hard-wired in and can't be changed.
- updateOutputCallback: the function to call before rendering output. Disabled for the make program.
- executeCodeWithRawInputFunc: function to call when you want to re-execute the given program with some new user input. Disabled for the make program.
- embeddedMode: if true, it is a shorthand for hideOutput = true, allowEditAnnotations = false (default : false)
- startingInstruction: the trace entry to start execution at (0-indexed) (default : 0).
- verticalStack: if true then place code display above visualization, else place side-by-side (default: false)
- jumpToEnd: if true jump to the end of execution - the same as setting startingInstruction to the last trace entry (default:false).
- codeDivWidth: the width of the code text window in pixels (default : 350).
- codeDivHeight: the height of the code text window in pixels (default : 400).
- hideOutput: hide "Program output" display (default : false).
- editCodeBaseURL: the URL to visit when the user clicks 'Edit code'.
- allowEditAnnotations: allow user to edit per-step annotations (default: false).
- disableHeapNesting: if true, then render all heap objects at the top level (i.e., no nested objects) (default : true).
- drawParentPointer: if true, then draw environment diagram parent pointers for all frames (default : true).
- textualMemoryLabels: render references using textual memory labels rather than as jsPlumb arrows (default : true).
- showOnlyOutputs: show only program outputs and NOT internal data structures (default : true).
