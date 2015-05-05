
import sys
import os
import shutil
from pkg_resources import resource_string, resource_filename


def init():
    print("This will create a new Runestone project in your current directory.")
    proceed = raw_input("Do you want to proceed? Y/n")
    if proceed[0].lower() == "n":
        sys.exit(0)
    project_name = raw_input("Project name: ")
    

def main(args=None):
    if not args:
        args = sys.argv[1:]
    foo_config = resource_filename('runestone', 'project/template/conf.py')
#    foo_string = resource_string('runestone', 'project/template/conf.py')    
    if args[0] == "init":
        init()
    elif args[0] == "build":
        build()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))