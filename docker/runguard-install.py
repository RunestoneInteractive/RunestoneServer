#!/usr/bin/env python3
# This installer sets up the required jobe users (i.e. the "users"
# that run submitted jobs) and compiles and adjusts the runguard sandbox.
# It must be run as root.

# If run with the parameter --purge, all files and users set up by a previous
# run of the script are deleted at the start.

from __future__ import print_function
import os
import subprocess
import re
import sys


JOBE_DIRS = ['/var/www/jobe', '/var/www/html/jobe']
LANGUAGE_CACHE_FILE = '/tmp/jobe_language_cache_file'
FILE_CACHE_BASE = '/home/jobe/files'

def get_config(param_name, install_dir):
    '''Get a config parameter from <<install_dir>>/application/config/config.php.
       An exception occurs if either the file or the required parameter
       is not found.
    '''
    with open('{}/application/config/config.php'.format(install_dir)) as config:
        lines = config.readlines()
    patterns = [
        r" *\$config\[ *'{}' *\] *= *\"([^\"]+)\";.*\n".format(param_name), # Double-quoted string
        r" *\$config\[ *'{}' *\] *= *'([^']+)';.*\n".format(param_name),    # Single-quoted string
        r" *\$config\[ *'{}' *\] *= *([^;]+);.*\n".format(param_name)       # Non-string literal
    ]
    for line in lines:
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                return match.group(1)
    raise Exception('Config param ' + param_name + ' not found')


def fail():
    print("Install failed")
    sys.exit(1);


def get_webserver():
    '''Find the user name used to run the Apache web server'''
    ps_cmd = "ps aux | grep -E '/usr/sbin/(apache2|httpd)'"
    try:
        ps_lines = subprocess.check_output(ps_cmd, shell=True).decode('utf8').split('\n')
    except subprocess.CalledProcessError:
        raise Exception("ps command to find web-server user id failed. Is the web server running?")
    names = {ps_line.split(' ')[0] for ps_line in ps_lines}
    candidates = names.intersection(set(['apache', 'www-data']))
    if len(candidates) != 1:
        raise Exception("Couldn't determine web-server user id. Is the web server running?")
    return list(candidates)[0]


def do_command(cmd, ignore_errors=False):
    '''Execute the given OS command user subprocess.call.
       Raise an exception on failure unless ignore_errors is True.
    '''
    try:
        returncode = subprocess.call(cmd, shell=True)
    except subprocess.SubprocessError:
        returncode = -1
    if returncode != 0:
        if ignore_errors:
            print("Command '{}' failed. Ignoring.".format(cmd))
        else:
            raise OSError("Command ({}) failed".format(cmd))


def check_php_version():
    '''Check that the installed PHP version is at least 5.5.
       Raise an exception on failure.
    '''
    if subprocess.call("php -r 'exit(version_compare(PHP_VERSION, \"5.5.0\", \"lt\"));'", shell=True) != 0:
            raise OSError("Jobe requires at least PHP 5.5.")


def make_sudoers(install_dir, webserver_user, num_jobe_users):
    '''Build a custom jobe-sudoers file for include in /etc/sudoers.d.
       It allows the webserver to run the runguard program as root and also to
       kill any jobe tasks and delete the run directories.
    '''
    commands = [install_dir + '/runguard/runguard']
    commands.append('/bin/rm -R /home/jobe/runs/*')
    for i in range(num_jobe_users):
        commands.append('/usr/bin/pkill -9 -u jobe{:02d}'.format(i))
        for directory in get_config('clean_up_path', install_dir).split(';'):
            commands.append('/usr/bin/find {}/ -user jobe{:02d} -delete'.format(directory, i))

    sudoers_file_name = '/etc/sudoers.d/jobe-sudoers'
    with open(sudoers_file_name, 'w') as sudoers:
        os.chmod(sudoers_file_name, 0o440)
        for cmd in commands:
            sudoers.write('{} ALL=(root) NOPASSWD: {}\n'.format(webserver_user, cmd))


def make_user(username, comment, make_home_dir=False, group='jobe'):
    ''' Check if user exists. If not, add the named user with the given comment.
        Make a home directory only if make_home_dir is true.
    '''
    try:
        do_command('id ' + username + '> /dev/null 2>&1')
        print(username, 'already exists')
    except:
        opt = '--home /home/jobe -m' if make_home_dir else ' -M'
        if group is None:
            group_opt = ''
        else:
            group_opt = ' -g ' + group
        do_command('useradd -r {} -s "/bin/false"{} -c "{}" {}'.format(opt, group_opt, comment, username))


def make_directory(dirpath, owner, group, permissions=771):
    '''If dirpath doesn't exist, make a directory and give it
       the given owner, group and permissions'''
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    do_command('chown {0}:{1} {2}; chmod {3} {2}'.format(owner, group, dirpath, permissions))


def do_purge(install_dir, num_runners):
    '''Purge existing users and extra files set up by a previous install'''
    for i in range(num_runners):
        do_command('userdel jobe{:02d}'.format(i), ignore_errors=True)

    do_command('userdel jobe', ignore_errors=True)
    do_command('groupdel jobe', ignore_errors=True)
    do_command('rm -rf /home/jobe')
    do_command('rm -rf /var/log/jobe')
    do_command('rm -rf {}/files'.format(install_dir), ignore_errors=True)
    do_command('rm -rf ' + FILE_CACHE_BASE + '/*', ignore_errors=True)


def main():
    if len(sys.argv) > 2 or (len(sys.argv) > 1 and sys.argv[1] != '--purge'):
        print("Usage: install [--purge]")
        sys.exit(0)

    purging = len(sys.argv) == 2

    install_dir = os.getcwd()
    if install_dir not in JOBE_DIRS:
        print("WARNING: Jobe appears not to have been installed in /var/www")
        print ("or /var/www/html as expected. Things might turn ugly.")

    if subprocess.check_output('whoami', shell=True) != b'root\n':
            print("****This script must be run by root*****")
            fail()
    else:
        try:
            check_php_version()

            num_jobe_users = int(get_config('jobe_max_users', install_dir))
            if purging:
                print('Purging all prior jobe users and files')
                do_purge(install_dir, num_jobe_users)

            print('Configuring for', num_jobe_users, 'simultaneous job runs')
            webserver_user = get_webserver()
            print("Web server is", webserver_user)
            print("Make user jobe")
            make_user('jobe', 'Jobe user. Provides home for runs and files.', True, None)
            # make sure webuser can reach /home/jobe/runs despite its not being in jobe group
            do_command("chmod 751 /home/jobe")
            print("Setting up file cache")
            make_directory(FILE_CACHE_BASE, 'jobe', webserver_user)

            # Ensure install directory subtree owned by webuser and not readable by others
            do_command('chown -R {0}:{0} {1}'.format(webserver_user, install_dir))
            do_command('chmod -R o-rwx,g+w {}'.format(install_dir))

            print("Making required job-runner users")
            for i in range(num_jobe_users):
                username = 'jobe{:02d}'.format(i)
                make_user(username, 'Jobe server task runner')

            print("Set up Jobe runs directory (/home/jobe/runs)")
            make_directory('/home/jobe/runs', 'jobe', webserver_user)
            print("Set up Jobe files directory (/home/jobe/files)")
            make_directory('/home/jobe/files', 'jobe', webserver_user)
            print("Set up Jobe log directory (/var/log/jobe)")
            make_directory('/var/log/jobe', 'jobe', webserver_user)

            print("Building runguard")
            runguard_commands = [
                "cd {0}".format(install_dir + '/runguard'),
                "gcc -o runguard runguard.c", # TODO Add -lcgroups  if using cgroups
                "chmod 700 runguard"
            ]
            cmd = ';'.join(runguard_commands)
            do_command(cmd)

            make_sudoers(install_dir, webserver_user, num_jobe_users)
            try:
                os.remove(LANGUAGE_CACHE_FILE)
            except:
                pass

            print("Runguard installation complete")

        except Exception as e:
            print("Exception during install: " + str(e))
            fail()

main()
