# Generates a JSON trace that is compatible with the js/pytutor.js frontend

import sys, pg_logger, json
from optparse import OptionParser

# To make regression tests work consistently across platforms,
# standardize display of floats to 3 significant figures
#
# Trick from:
# http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module
json.encoder.FLOAT_REPR = lambda f: ('%.3f' % f)

def json_finalizer(input_code, output_trace):
  ret = dict(code=input_code, trace=output_trace)
  json_output = json.dumps(ret, indent=INDENT_LEVEL)
  return json_output

def js_var_finalizer(input_code, output_trace):
  global JS_VARNAME
  ret = dict(code=input_code, trace=output_trace)
  json_output = json.dumps(ret, indent=None)
  return "var %s = %s;" % (JS_VARNAME, json_output)

parser = OptionParser(usage="Generate JSON trace for pytutor")
parser.add_option('-c', '--cumulative', default=False, action='store_true',
        help='output cumulative trace.')
parser.add_option('-p', '--heapPrimitives', default=False, action='store_true',
        help='render primitives as heap objects.')
parser.add_option('-o', '--compact', default=False, action='store_true',
        help='output compact trace.')
parser.add_option('-i', '--input', default=False, action='store',
        help='JSON list of strings for simulated raw_input.', dest='raw_input_lst_json')
parser.add_option("--create_jsvar", dest="js_varname", default=None,
                  help="Create a JavaScript variable out of the trace")

(options, args) = parser.parse_args()
INDENT_LEVEL = None if options.compact else 2

fin = sys.stdin if args[0] == "-" else open(args[0])

if options.js_varname:
  JS_VARNAME = options.js_varname
  print(pg_logger.exec_script_str_local(fin.read(), options.raw_input_lst_json, options.cumulative, options.heapPrimitives, js_var_finalizer))
else:
  print(pg_logger.exec_script_str_local(fin.read(), options.raw_input_lst_json, options.cumulative, options.heapPrimitives, json_finalizer))
