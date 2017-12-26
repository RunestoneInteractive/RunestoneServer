# Forked from - Wed Jun 21 09:01:59 EDT 2017
# https://github.com/tophatmonocle/ims_lti_py

# Interestingly, the code in Pypi fails:
# https://pypi.python.org/pypi/ims_lti_py/0.5

# And the code in the Harvard fork fails:
# https://github.com/harvard-dce/dce_lti_py

# But the trunk of this works
# https://github.com/tophatmonocle/ims_lti_py

from uuid import uuid1

def generate_identifier():
    return uuid1().__str__()

class InvalidLTIConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidLTIRequestError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)