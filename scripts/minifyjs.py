#!/usr/bin/env python

from subprocess import call
import sys
import os

outdir = sys.argv[1] + "/_static/"

filenames = [outdir + "activecode.js",
             outdir + "animationbase.js",
             outdir + "assess.js",
             outdir + "bookfuncs.js",
             outdir + "bootstrap-sphinx.js",
             outdir + "codemirror.js",
             outdir + "doctools.js",
             outdir + "edu-python.js",
             outdir + "guiders-1.3.0.js",
             outdir + "jquery.highlight.js",
             outdir + "jquery.idle-timer.js",
             outdir + "navhelp.js",
             outdir + "poll.js",
             outdir + "python.js",
             outdir + "rangy-cssclassapplier.js",
             outdir + "searchtools.js",
             outdir + "sortmodels.js",
             outdir + "sortviewers.js",
             outdir + "user-highlights.js",
             outdir + "websupport.js",
             outdir + "lib/lis.js",
             outdir + "lib/prettify.js",
             outdir + "js/jquery.corner.js",
             outdir + "js/opt-frontend.js",
             outdir + "js/opt-lessons.js",
             outdir + "js/pytutor.js"]

for filename in filenames:
    print("Minifying " + filename)

    call(["mv", filename, "a.js"])

    call(["java",
          "-jar", "scripts/closure-compiler.jar",
          "--js", "a.js",
          "--js_output_file", filename,
          "--compilation_level", "SIMPLE_OPTIMIZATIONS",
          "--warning_level", "QUIET",
          "--jscomp_off", "internetExplorerChecks"])

call(["rm", "a.js"])
print("Done.")
