''' 
A simple framework for regression testing based on golden files
by Philip Guo

(sloppily) customized for the Online Python Tutor project
'''

import os, re, shutil, optparse, difflib
from subprocess import *


def filter_output(s):
  return s


def execute(input_filename):
  assert os.path.isfile(input_filename)
  (base, ext) = os.path.splitext(input_filename)
  assert ext == INPUT_FILE_EXTENSION

  (stdout, stderr) = Popen(PROGRAM + [input_filename], stdout=PIPE, stderr=PIPE).communicate()

  if stderr:
    print '(has stderr)'
  #  print '  stderr {'
  #  print stderr, '}'
  else:
    print

  # capture stdout into outfile, filtering out machine-specific addresses
  outfile = base + OUTPUT_FILE_EXTENSION
  outf = open(outfile, 'w')

  for line in stdout.splitlines():
    filtered_line = re.sub(' 0x.+?>', ' 0xADDR>', line)
    print >> outf, filtered_line

  outf.close()


def clobber_golden_file(golden_file):
  (base, ext) = os.path.splitext(golden_file)
  outfile = base + OUTPUT_FILE_EXTENSION
  assert os.path.isfile(outfile)
  print '  Clobber %s => %s' % (outfile, golden_file)
  shutil.copy(outfile, golden_file)


# returns True if there is a diff, False otherwise
def golden_differs_from_out(golden_file):
  (base, ext) = os.path.splitext(golden_file)
  outfile = base + OUTPUT_FILE_EXTENSION
  assert os.path.isfile(outfile)
  assert os.path.isfile(golden_file)

  golden_s = open(golden_file).readlines()
  out_s = open(outfile).readlines()

  golden_s_filtered = filter_output(golden_s)
  out_s_filtered = filter_output(out_s)

  return out_s_filtered != golden_s_filtered


def diff_test_output(test_name):
  (base, ext) = os.path.splitext(test_name)

  golden_file = base + GOLDEN_FILE_EXTENSION
  assert os.path.isfile(golden_file)
  outfile = base + OUTPUT_FILE_EXTENSION
  assert os.path.isfile(outfile)

  golden_s = open(golden_file).readlines()
  out_s = open(outfile).readlines()

  golden_s_filtered = filter_output(golden_s)
  out_s_filtered = filter_output(out_s)

  first_line = True
  for line in difflib.unified_diff(golden_s_filtered, out_s_filtered, \
                                   fromfile=golden_file, tofile=outfile):
    if first_line:
      print # print an extra line to ease readability
      first_line = False
    print line,


def run_test(input_filename, clobber_golden=False):
  print 'Testing', input_filename,

  (base, ext) = os.path.splitext(input_filename)
  assert ext == INPUT_FILE_EXTENSION

  # to eliminate possibility of using stale output:
  outfile = base + OUTPUT_FILE_EXTENSION
  if os.path.isfile(outfile):
    os.remove(outfile)

  input_fullpath = input_filename
  execute(input_fullpath)

  golden_file = base + GOLDEN_FILE_EXTENSION
  if os.path.isfile(golden_file):
    if golden_differs_from_out(golden_file):
      print "  FAILED!!!"
    if clobber_golden:
      clobber_golden_file(golden_file)
  else:
    clobber_golden_file(golden_file)


def run_all_tests(clobber=False):
  for t in ALL_TESTS:
    run_test(t, clobber)

def diff_all_test_outputs():
  for t in ALL_TESTS:
    diff_test_output(t)


if __name__ == "__main__":
  parser = optparse.OptionParser()
  parser.add_option("--all", action="store_true", dest="run_all",
                    help="Run all tests")
  parser.add_option("--only-clobber", action="store_true", dest="only_clobber",
                    help="Clobber ALL golden files WITHOUT re-running tests")
  parser.add_option("--clobber", action="store_true", dest="clobber",
                    help="Clobber golden files when running tests")
  parser.add_option("--test", dest="test_name",
                    help="Run one test")
  parser.add_option("--difftest", dest="diff_test_name",
                    help="Diff against golden file for one test")
  parser.add_option("--diffall", action="store_true", dest="diff_all",
                    help="Diff against golden file for all tests")
  parser.add_option("--py3", action="store_true", dest="py3",
                    help="Run tests using Python 3.2 (rather than Python 2.7)")
  (options, args) = parser.parse_args()


  INPUT_FILE_EXTENSION = '.txt' # input test files are .txt, NOT .py

  if options.py3:
    PROGRAM = ['python3.2', '../generate_json_trace.py']
    OUTPUT_FILE_EXTENSION = '.out_py3'
    GOLDEN_FILE_EXTENSION = '.golden_py3'
  else:
    PROGRAM = ['python2.7', '../generate_json_trace.py']
    OUTPUT_FILE_EXTENSION = '.out'
    GOLDEN_FILE_EXTENSION = '.golden'

  ALL_TESTS = []

  for (pwd, subdirs, files) in os.walk('.', followlinks=True): # need to follow example-code symlink
    for f in files:
      (base, ext) = os.path.splitext(f)
      if ext == INPUT_FILE_EXTENSION:
        fullpath = os.path.join(pwd, f)
        ALL_TESTS.append(fullpath)


  if options.run_all:
    if options.clobber:
      print 'Running all tests and clobbering results ...'
    else:
      print 'Running all tests ...'
    run_all_tests(options.clobber)

  elif options.diff_all:
    diff_all_test_outputs()
  elif options.diff_test_name:
    assert options.diff_test_name in ALL_TESTS
    diff_test_output(options.diff_test_name)
  elif options.test_name:
    assert options.test_name in ALL_TESTS
    run_test(options.test_name, options.clobber)
  elif options.only_clobber:
    for t in ALL_TESTS:
      (base, ext) = os.path.splitext(t)
      golden_file = base + GOLDEN_FILE_EXTENSION
      clobber_golden_file(golden_file)
  else:
    parser.print_help()

