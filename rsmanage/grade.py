import applications.runestone.controllers.assignments
import json, datetime, sys

userinfo = json.loads(os.environ['RSM_USERINFO'])
print(userinfo['course'], userinfo['pset'])
# print(db.keys())
print(settings)