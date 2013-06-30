#!/usr/local/bin/python

from subprocess import call
import sys

# Define the parameters for the POST request and encode them in
# a URL-safe format.

outdir = sys.argv[1] + "/_static/"

#outdir = "static/thinkcspy/" + "_static/"

filenames = [outdir + "bookfuncs.js",
             outdir + "activecode.js",
             outdir + "animationbase.js",
             outdir + "assess.js",
             outdir + "bootstrap-sphinx.js",
             outdir + "codemirror.js",
             outdir + "doctools.js",
             outdir + "edu-python.js",
             outdir + "jquery.tablesorter.js",
             outdir + "python.js",
             outdir + "rangy-cssclassapplier.js",
             outdir + "searchtools.js",
             outdir + "simplemodal.js",
             outdir + "sortmodels.js",
             outdir + "sortviewers.js",
             outdir + "user-highlights.js",
             outdir + "websupport.js",
             outdir + "user-highlights.js",
             outdir + "js-parsons/lib/lis.js",
             outdir + "js-parsons/lib/prettify.js",
             outdir + "js-parsons/parsons.js"]

for filename in filenames:
    print "Minifying " + filename

    call(["mv", filename, "a.js"])

    call(["java",
          "-jar", "closure-compiler.jar",
          "--js", "a.js",
          "--js_output_file", filename,
          "--compilation_level", "SIMPLE_OPTIMIZATIONS",
          "--warning_level", "QUIET"])

call(["rm", "a.js"])
print "Done."
