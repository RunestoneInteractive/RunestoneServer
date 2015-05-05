
import sys
import os
import shutil
import getpass
from pkg_resources import resource_string, resource_filename


def init():
    template_base_dir = resource_filename('runestone', 'common/newproject_copy_me')
    config_stuff = resource_string('runestone','common/newproject_copy_me/conf.py')
    paver_stuff = resource_string('runestone','common/newproject_copy_me/pavement.py')    
    conf_dict = {}
    print("This will create a new Runestone project in your current directory.")
    proceed = raw_input("Do you want to proceed? Y/n") or "Y"
    if proceed[0].lower() == "n":
        sys.exit(0)
    print("Next we need to gather a few pieces of information to create your configuration files")
    conf_dict['project_name'] = raw_input("Project name: (one word, no spaces)")
    conf_dict['build_dir'] = raw_input("path to build dir [./build] ") or "build"
    conf_dict['login_req'] = raw_input("require login [false] ") or "false"
    conf_dict['master_url'] = raw_input("URL for ajax server [http://127.0.0.1:8000] ") or "http://127.0.0.1:8000"
    conf_dict['author'] = raw_input("your Name ") or getpass.getuser()
    conf_dict['project_title'] = raw_input("Title for this project [Runestone Default]") or "Runestone Default"
    
    shutil.copytree(os.path.join(template_base_dir,'_sources'),'_sources')
    shutil.copytree(os.path.join(template_base_dir,'_static'),'_static')
    shutil.copytree(os.path.join(template_base_dir,'_templates'),'_templates')
    os.makedirs(conf_dict['build_dir'])
    paver_final = paver_stuff % conf_dict
    config_final = config_stuff % conf_dict

    with open('pavement.py','w') as pvf:
        pvf.write(paver_final)

    with open('conf.py','w') as pvf:
        pvf.write(config_final)

    print("Done.  Type runestone build to build your project")

def build():
    from paver.tasks import main as paver_main
    sys.argv[0] = "build"
    paver_main()
    
def serve():
    import SimpleHTTPServer
    import SocketServer
    sys.path.insert(0,os.getcwd())
    try:
        import pavement
    except:
        print("Error, you must be in your project root directory")
        return
    
    os.chdir(pavement.serving_dir)

    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT

    httpd.serve_forever()

def main(args=None):
    if not args:
        args = sys.argv[1:]
    foo_config = resource_filename('runestone', 'common')
#    foo_string = resource_string('runestone', 'project/template/conf.py')    
    if args[0] == "init":
        init()
    elif args[0] == "build":
        build()
    elif args[0] == "serve":
        serve()
    else:
        print("Error:  I only understand init, build, and serve")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))