from gluon.scheduler import Scheduler
import shutil
from os import path
import os
import sys
import re
from paver.easy import sh
import logging
from pkg_resources import resource_string, resource_filename
from runestone.server.chapternames import addChapterInfoFromScheduler, findChaptersSubChapters

rslogger = logging.getLogger('web2py.app.runestone')
rslogger.setLevel('DEBUG')


################
## This task will run as a scheduled task using the web2py scheduler.
## It's dispached from build() and build_custom() in controllers/designer.py
################
def run_sphinx(rvars=None, folder=None, application=None, http_host=None, base_course=None):
    # workingdir is the application folder
    workingdir = folder
    # sourcedir holds the all sources temporarily
    sourcedir = path.join(workingdir, 'build', rvars['projectname'])

    rslogger.debug("Starting to build {}".format(rvars['projectname']))

    # create the custom_courses dir if it doesn't already exist
    if not os.path.exists(path.join(workingdir, 'custom_courses')):
        os.mkdir(path.join(workingdir, 'custom_courses'))

    # confdir holds the conf and index files
    custom_dir = path.join(workingdir, 'custom_courses', rvars['projectname'])


    if not os.path.exists(custom_dir):
        os.mkdir(custom_dir)

    # ## check for base_course  if base_course == None
    ### read conf.py and look for How to Think to determine coursetype
    if base_course == None:
        base_course = 'thinkcspy'

    # copy all the sources into the temporary sourcedir
    if os.path.exists(sourcedir):
        shutil.rmtree(sourcedir)
    shutil.copytree(path.join(workingdir, 'books', base_course), sourcedir)

    makePavement(http_host, rvars, sourcedir, base_course)
    shutil.copy(path.join(sourcedir,'pavement.py'),custom_dir)

    #########
    # We're rebuilding a course
    #########
    if rvars['coursetype'] == 'rebuildcourse':

        try:
            # copy the index and conf files to the sourcedir
            shutil.copy(path.join(custom_dir, 'pavement.py'), path.join(sourcedir, 'pavement.py'))
            shutil.copy(path.join(custom_dir, 'index.rst'), path.join(sourcedir, '_sources', 'index.rst'))

            # copy the assignments.rst file from confidir as it may contain assignments written
            # by the instructor
            shutil.copy(path.join(custom_dir, 'assignments.rst'),
                        path.join(sourcedir, '_sources', 'assignments.rst'))

            # this check should allow for backward compatibility
            if os.path.exists(os.path.join(custom_dir,'assignments')):
                shutil.copytree(path.join(custom_dir,'assignments'),
                                path.join(sourcedir,'_sources','assignments'))

        except OSError:
            # Either the sourcedir already exists (meaning this is probably devcourse, thinkcspy, etc,
            # or the conf.py or index.rst files are missing for some reason.
            raise OSError("missing paver, index, or assignments file")

    ########
    # we're just copying one of the pre-existing books
    ########
    else:
        # Save copies of files that the instructor may customize
        shutil.copy(path.join(sourcedir,'_sources', 'index.rst'),custom_dir)
        shutil.copy(path.join(sourcedir,'_sources', 'assignments.rst'),custom_dir)


    ###########
    # Set up and run Paver build
    ###########

    from paver.tasks import main as paver_main
    os.chdir(sourcedir)
    paver_main(args=["build"])
    rslogger.debug("Finished build of {}".format(rvars['projectname']))
    try:
        shutil.copy('build_info',custom_dir)
    except IOError as copyfail:
        rslogger.debug("Failed to copy build_info_file")
        rslogger.debug(copyfail.message)
        idxname = 'index.rst'

    #
    # Build the completion database
    #
    rslogger.debug("Starting to populate chapters for {}".format(rvars['projectname']))
    scd, ct = findChaptersSubChapters(path.join(sourcedir, '_sources', 'index.rst'))
    addChapterInfoFromScheduler(scd, ct, rvars['projectname'],db)

    for root, dirs, files in os.walk(sourcedir):
        for fn in files:
            if fn.endswith('.rst'):
                fh = open(path.join(root, fn), 'r')
                populateSubchapter(root, fn, fh, sourcedir, rvars['projectname'])

    #
    # move the sourcedir/build/projectname folder into static
    #
    shutil.rmtree(os.path.join(workingdir,'static',rvars['projectname']),ignore_errors=True)
    shutil.move(os.path.join(sourcedir,'build',rvars['projectname']),
                os.path.join(workingdir,'static',rvars['projectname']) )
    #
    # clean up
    #

    shutil.rmtree(sourcedir)
    rslogger.debug("Completely done with {}".format(rvars['projectname']))


def makePavement(http_host, rvars, sourcedir, base_course):
    paver_stuff = resource_string('runestone', 'common/project_template/pavement.tmpl')
    opts = {'master_url': settings.server_type + http_host,
            'project_name': rvars['projectname'],
            'build_dir': 'build',
            'log_level': 10,
            'use_services': 'true',
            'dburl': settings.database_uri,
            'basecourse': base_course,
            }
    if 'loginreq' in rvars:
        opts['login_req'] = 'true'
    else:
        opts['login_req'] = 'false'
    if 'python3' in rvars:
        opts['python3'] = 'true'
    else:
        opts['python3'] = 'false'

    opts['dest'] = '../../static'

    paver_stuff = paver_stuff % opts
    with open(path.join(sourcedir, 'pavement.py'), 'w') as fp:
        fp.write(paver_stuff)


div_re = re.compile(
    r'\s*\.\.\s+(activecode|codelens|mchoicemf|mchoicema|parsonsprob|animation|actex|fillintheblank|mcmfrandom|video)\s*::\s+(.*)$'
)

odd_ex_list = [
'ch02_ex1',
'ex_2_3',
'ex_2_5',
'ex_2_7',
'ex_2_9',
'ex_2_11',
'ex_3_1',
'ex_3_3',
'ex_3_5',
'ex_3_7',
'ex_3_9',
'ex_3_11',
'ex_3_13',
'mod_q1',
'ex_5_1',
'ex_5_3',
'ex_5_5',
'ex_5_7',
'ex_5_9',
'ex_5_11',
'ex_5_13',
'ex_5_15',
'ex_5_17',
'ex_6_1',
'ex_6_3',
'ex_6_5',
'ex_6_7',
'ex_6_9',
'ex_6_11',
'ex_6_13',
'ex_7_7',
'ex_7_9',
'ex_7_13',
'ex_7_15',
'ex_7_17',
'ex_7_19',
'ex_7_21',
'ex_7_23',
'ex_7_10',
'ex_8_3',
'ex_8_6',
'ex_8_8',
'ex_8_10',
'ex_8_12',
'ex_8_14',
'ex_8_16',
'ex_8_18',
'ex_8_20',
'ex_9_3',
'ex_9_5',
'ex_9_6',
'ex_9_8',
'ex_9_10',
'ex_9_12',
'ex_9_14',
'ex_6_1',
'ex_6_3',
'ex_10_5',
'ex_11_01',
'ex_11_02',
'ex_11_04',
'ex_rec_1',
'ex_rec_3',
'ex_rec_5',
'ex_rec_7']



def populateSubchapter(fpath, fn, fh, sourcedir, base_course):
    chapter = fpath.replace(sourcedir+'/', '')
    subchapter = fn.replace('.rst', '')
    for line in fh:
        mo = div_re.match(line)
        if mo:
            #rslogger.debug("{} {} {} {}".format(chapter, subchapter, mo.group(1), mo.group(2)))
            divt = mo.group(1)
            divid = mo.group(2)
            if divt == 'actex' and divid in odd_ex_list:
                divt = 'actex_answered'
            if chapter not in ['Test', 'ExtraStuff', sourcedir]:
                div = db.div_ids.update_or_insert(chapter=chapter, subchapter=subchapter, div_type=divt,
                                                  div_id=divid, course_name=base_course)

    db.commit()


scheduler = Scheduler(db)
