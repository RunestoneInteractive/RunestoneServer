from gluon.scheduler import Scheduler
import shutil
from os import path
import os
import sys
import re
from paver.easy import sh
from sphinx.application import Sphinx
import logging


################
## This task will run as a scheduled task using the web2py scheduler.
## It's dispached from build() and build_custom() in controllers/designer.py
################
def run_sphinx(rvars=None, folder=None, application=None, http_host=None, base_course=None):
    # workingdir is the application folder
    workingdir = folder
    mylog = logging.getLogger('web2py.root')
    # sourcedir holds the all sources temporarily
    sourcedir = path.join(workingdir,rvars['projectname'])

    # create the custom_courses dir if it doesn't already exist
    if not os.path.exists(path.join(workingdir, 'custom_courses')):
        os.mkdir(path.join(workingdir, 'custom_courses'))

    # confdir holds the conf and index files
    confdir = path.join(workingdir, 'custom_courses', rvars['projectname'])
    custom_dir = confdir
    if not os.path.exists(confdir):
        os.mkdir(confdir)

    # ## check for base_course  if base_course == None
    ### read conf.py and look for How to Think to determine coursetype
    if base_course == None:
        conf_file = open(path.join(confdir, 'conf.py'), 'r')
        conf_text = conf_file.read()
        if 'How to Think' in conf_text:
            base_course = 'thinkcspy'
        elif 'Programs, Information' in conf_text:
            base_course = 'pip'
        else:
            base_course = 'pythonds'
        conf_file.close()
        db(db.courses.course_name == rvars['projectname']).update(base_course=base_course)

    #########
    # We're rebuilding a course
    #########
    if rvars['coursetype'] == 'rebuildcourse':
        try:
            # copy all the sources into the temporary sourcedir
            if os.path.exists(sourcedir):
                shutil.rmtree(sourcedir)
            shutil.copytree(path.join(workingdir, base_course, 'source'), sourcedir)
        except:
            raise OSError("Problems with source directory: workingdir = %s, sourcedir = %s base_course = %s" % (workingdir, sourcedir, base_course))

        try:
            # copy the index and conf files to the sourcedir
            shutil.copy(path.join(confdir, 'conf.py'), path.join(sourcedir, 'conf.py'))
            shutil.copy(path.join(confdir, 'index.rst'), path.join(sourcedir, 'index.rst'))

            # copy the assignments.rst file from confidir as it may contain assignments written
            # by the instructor
            shutil.copy(path.join(confdir, 'assignments.rst'),
                        path.join(sourcedir, 'assignments.rst'))

        except OSError:
            # Either the sourcedir already exists (meaning this is probably devcourse, thinkcspy, etc,
            # or the conf.py or index.rst files are missing for some reason.
            raise OSError("missing conf, index, or assignments file")

        # for old legacy courses that may not have a base_course value
        # read conf.py and look for 'How to Think'
            # do we care about a totally custom course?

            # now update the database so we don't have to do this again





    ########
    # we're just copying one of the pre-existing books
    ########
    else:
        # copy all the sources into the temporary sourcedir
        shutil.copytree(path.join(workingdir, base_course, 'source'), sourcedir)

        # copy the config file. We save it in confdir (to allow rebuilding the course at a later date),
        # and we also copy it to the sourcedir (which will be used for this build and then deleted.
        for template_file in ['template_conf.py', 'index.rst', 'assignments.rst']:
            if 'template' in template_file:
                dest_file = template_file.replace('template_', '')
            else:
                dest_file = template_file
            shutil.copy(path.join(workingdir, base_course, template_file),
                        path.join(confdir, dest_file))
            shutil.copy(path.join(workingdir, base_course, template_file),
                        path.join(sourcedir, dest_file))


    ###########
    # Set up and run Sphinx
    ###########
    coursename = rvars['projectname']
    confdir = sourcedir  # Sphinx build actually gets conf stuff from temp sourcedir
    outdir = path.join(folder, 'static', coursename)
    doctreedir = path.join(outdir, 'doctrees')
    buildername = 'html'
    confoverrides = {}
    confoverrides['html_context.appname'] = application
    confoverrides['html_context.course_id'] = coursename
    confoverrides['html_context.loglevel'] = 10
    confoverrides['html_context.course_url'] = settings.server_type + http_host

    cwd = os.getcwd()
    os.chdir(path.join('applications',application))
    build_info = sh("git describe --long", capture=True)
    bi = open(path.join('custom_courses',coursename,'build_info'),'w')
    bi.write(build_info)
    bi.close()
    os.chdir(cwd)    
    build_split = build_info.split('-')
    confoverrides['html_context.build_info'] = build_split[0]

    if 'loginreq' in rvars:
        confoverrides['html_context.login_required'] = 'true'
    else:
        confoverrides['html_context.login_required'] = 'false'
    status = sys.stdout
    warning = sys.stdout
    freshenv = True
    warningiserror = False
    tags = []

    sys.path.insert(0,path.join(folder,'modules'))
    from chapternames import addChapterInfoFromScheduler, findChaptersSubChapters

    force_all = True
    filenames = []

    app = Sphinx(sourcedir, confdir, outdir, doctreedir, buildername,
                confoverrides, status, warning, freshenv,
                warningiserror, tags)
    app.build(force_all, filenames)



    if base_course == 'thinkcspy':
        idxname = 'toc.rst'
    else:
        idxname = 'index.rst'

    scd, ct = findChaptersSubChapters(path.join(sourcedir, idxname))
    addChapterInfoFromScheduler(scd, ct, rvars['projectname'],db)

    for root, dirs, files in os.walk(sourcedir):
        for fn in files:
            if fn.endswith('.rst'):
                fh = open(path.join(root, fn), 'r')
                populateSubchapter(root, fn, fh, sourcedir, rvars['projectname'])

    shutil.rmtree(sourcedir)


    donefile = open(os.path.join(custom_dir, 'done'), 'w')
    donefile.write('success')
    donefile.close()


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
            print chapter, subchapter, mo.group(1), mo.group(2)
            divt = mo.group(1)
            divid = mo.group(2)
            if divt == 'actex' and divid in odd_ex_list:
                divt = 'actex_answered'
            if chapter not in ['Test', 'ExtraStuff', sourcedir]:
                div = db.div_ids.update_or_insert(chapter=chapter, subchapter=subchapter, div_type=divt,
                                                  div_id=divid, course_name=base_course)

    db.commit()


scheduler = Scheduler(db)
