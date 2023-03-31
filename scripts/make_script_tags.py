import json
import pyclip

import_file = "/Users/bmiller/Runestone/RunestoneComponents/runestone/dist/webpack_static_imports.json"

imports = json.load(open(import_file, "r"))
res = ""
for f in imports["js"]:
    res += f"""<script src="_static/{f}"></script>\n"""

for f in imports["css"]:
    res += f"""<link rel="stylesheet" type="text/css" href="_static/{f}" >\n"""

print(res)
pyclip.copy(res)
print("The New imports on on the clipboard.")
