# Convert project from Python 2 to Python 3 and test that JSON traces are
# unchanged for all examples.
#
# python3 convert_2to3.py
#
# Runs under Python 2.7 and Python 3.x without 2to3 conversion
#
# Created by John DeNero

import generate_json_trace
import os
import sys
import json


def write_trace(python, example_path, output_path):
  '''Use system call to generate a JSON trace using some python binary.'''
  example = os.path.split(example_path)[1]
  print('Generating JSON for "{0}" with {1}'.format(example, python))
  cmd = '{0} generate_json_trace.py {1} > {2}'
  os.system(cmd.format(python, example_path, output_path))


def write_py2_traces(examples_dir, traces_dir):
  '''Write JSON traces for all examples using Python 2.7.'''
  for path, _, filenames in os.walk(examples_dir):
    for example in filenames:
      example_path = os.path.join(path, example)
      outfile = path.replace(os.path.sep, '_') + '_' + example
      output_path = os.path.join(traces_dir, outfile)
      write_trace('python2.7', example_path, output_path)


def verify_py3_traces(examples_dir, traces_dir):
  '''Write and compare JSON traces for all examples using Python 3.'''
  diffs = []
  for path, _, filenames in os.walk(examples_dir):
    for example in filenames:
      example_path = os.path.join(path, example)
      outfile = path.replace(os.path.sep, '_') + '_' + example
      output_path = os.path.join(traces_dir, outfile + '.py3k')
      write_trace('python3', example_path, output_path)

      py2_path = os.path.join(traces_dir, outfile)
      py2_result = json.load(open(py2_path))
      py3_result = json.load(open(output_path))
      if py2_result['trace'] != py3_result['trace']:
        diffs.append(example)
  return diffs


known_differences = """Known differences include:

fib.txt: "while True:" is evaluated once in Python 3, but repeatedly in Python.

map.txt: 2to3 converts call to map() to a list comprehension.

OOP*.txt, ll2.txt: __init__ functions orphan a __locals__ dict on the heap in
                   Python 3, but it is not rendered in the front end.

wentworth_try_finally.txt: Python 3 integer division is true, not floor.
"""

if __name__ == '__main__':
  examples_dir = 'example-code'
  if not os.path.exists(examples_dir):
    print('Examples directory {0} does not exist.'.format(examples_dir))
    sys.exit(1)

  traces_dir = examples_dir + '-traces'
  if os.path.exists(traces_dir):
    print('Testing directory {0} already exists.'.format(traces_dir))
    sys.exit(1)
  os.mkdir(traces_dir)

  write_py2_traces(examples_dir, traces_dir)

  # Convert examples to Python 3
  os.system('2to3 -w -n --no-diffs {0}/*.txt {0}/*/*.txt'.format(examples_dir))

  diffs = verify_py3_traces(examples_dir, traces_dir)

  if diffs:
    print('Trace differences for: {0}'.format(diffs))
    print('See {0} for traces.'.format(traces_dir))
    print(known_differences)
  else:
    print('Traces are identical; cleaning up')
    shutil.rm(traces_dir)

