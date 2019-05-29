# ************************************************
# |docname| - Provide feedback for student answers
# ************************************************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import re
import ast
import os
import tempfile
import shutil
import subprocess
from threading import Timer
from io import open
import json
import time
import sys

# Third-party imports
# -------------------
from gluon import current

# Local imports
# -------------
from runestone.server.lp_common_lib import STUDENT_SOURCE_PATH, \
    code_here_comment, read_sphinx_config, BUILD_SYSTEM_PATH, get_sim_str_sim30


# Return ``(True, feedback)`` if feedback should be computed on the server,
# instead of the client. This function assumes that the inputs have already been validated.
def is_server_feedback(div_id, course):
    # Get the information about this question. Per the `web2py docs
    # <http://web2py.com/books/default/chapter/29/04/the-core?search=import+module#Sharing-the-global-scope-with-modules-using-the-current-object>`_,
    # an assignment in ``models/db.py`` makes ``current.db`` available.
    query_results = current.db(
        (current.db.questions.name == div_id) &
        (current.db.questions.base_course == current.db.courses.base_course) &
        (current.db.courses.course_name == course)
    ).select(
        current.db.questions.feedback,
        current.db.courses.login_required
    ).first()

    # check for query_results
    if not query_results:
        return False, None
    # If feedback is present, decode it.
    feedback = query_results and query_results.questions.feedback
    if feedback is not None:
        feedback = json.loads(feedback)
        return query_results.courses.login_required, feedback
    else:
        # If feedback isn't present, use client-side grading.
        return False, None


# Provide feedback for a fill-in-the-blank problem. This should produce
# identical results to the code in ``evaluateAnswers`` in ``fitb.js``.
def fitb_feedback(answer_json, feedback):
    # Grade based on this feedback. The new format is JSON; the old is
    # comma-separated.
    try:
        answer = json.loads(answer_json)
        # Some answers may parse as JSON, but still be in the old format. The
        # new format should always return an array.
        assert isinstance(answer, list)
    except:
        answer = answer_json.split(',')
    displayFeed = []
    isCorrectArray = []
    # The overall correctness of the entire problem.
    correct = True
    for blank, feedback_for_blank in zip(answer, feedback):
        if not blank:
            isCorrectArray.append(None)
            displayFeed.append('No answer provided.')
            correct = False
        else:
            # The correctness of this problem depends on if the first item matches.
            is_first_item = True
            # Check everything but the last answer, which always matches.
            for fb in feedback_for_blank[:-1]:
                if 'regex' in fb:
                    if re.search(fb['regex'], blank,
                                 re.I if fb['regexFlags'] == 'i' else 0):
                        isCorrectArray.append(is_first_item)
                        if not is_first_item:
                            correct = False
                        displayFeed.append(fb['feedback'])
                        break
                else:
                    assert 'number' in fb
                    min_, max_ = fb['number']
                    try:
                        val = ast.literal_eval(blank)
                        in_range = val >= min_ and val <= max_
                    except:
                        # In case something weird or invalid was parsed (dict, etc.)
                        in_range = False
                    if in_range:
                        isCorrectArray.append(is_first_item)
                        if not is_first_item:
                            correct = False
                        displayFeed.append(fb['feedback'])
                        break
                is_first_item = False
            # Nothing matched. Use the last feedback.
            else:
                isCorrectArray.append(False)
                correct = False
                displayFeed.append(feedback_for_blank[-1]['feedback'])

    # Return grading results to the client for a non-test scenario.
    res = dict(
        correct=correct,
        displayFeed=displayFeed,
        isCorrectArray=isCorrectArray)
    return 'T' if correct else 'F', res


# lp feedback
# ===========
def lp_feedback(code_snippets, feedback_struct):
    db = current.db
    base_course = db(
        (db.courses.id == current.auth.user.course_id)
    ).select(db.courses.base_course).first().base_course
    sphinx_base_path = os.path.join(current.request.folder, 'books', base_course)
    source_path = feedback_struct['source_path']
    # Read the Sphinx config file to find paths relative to this directory.
    sphinx_config = read_sphinx_config(sphinx_base_path)
    if not sphinx_config:
        return {
            'errors': ['Unable to load Sphinx configuration file from {}'.format(sphinx_base_path)]
        }
    sphinx_source_path = sphinx_config['SPHINX_SOURCE_PATH']
    sphinx_out_path = sphinx_config['SPHINX_OUT_PATH']

    # Next, read the student source in for the program the student is working on.
    try:
        # Find the path to the student source file.
        abs_source_path = os.path.normpath(os.path.join(sphinx_base_path,
            sphinx_out_path, STUDENT_SOURCE_PATH, source_path))
        with open(abs_source_path, encoding='utf-8') as f:
            source_str = f.read()
    except Exception as e:
        return { 'errors': ['Cannot open source file {}: {}.'
                 .format(abs_source_path, e)] }

    # Create a snippet-replaced version of the source, by looking for "put code
    #   here" comments and replacing them with the provided code. To do so,
    # first split out the "put code here" comments.
    split_source = source_str.split(code_here_comment(source_path))
    # Sanity check! Source with n "put code here" comments splits into n+1
    # items, into which the n student code snippets should be interleaved.
    if len(split_source) - 1 != len(code_snippets):
        return { 'errors': ['Wrong number of snippets.'] }
    # Interleave these with the student snippets.
    interleaved_source = [None]*(2*len(split_source) - 1)
    interleaved_source[::2] = split_source
    try:
        interleaved_source[1::2] = _platform_edit(feedback_struct['builder'],
                                                  code_snippets, source_path)
    except Exception as e:
        return { 'errors': ['An exception occurred: {}'.format(e)] }
    # Join them into a single string. Make sure newlines separate everything.
    source_str = '\n'.join(interleaved_source)

    # Create a temporary directory, then write the source there. Horrible kluge
    # for Python 2.7. Much better: use tempfile.TemporaryDirectory instead.
    try:
        temp_path = tempfile.mkdtemp()
        temp_source_path = os.path.join(temp_path, os.path.basename(source_path))
        with open(temp_source_path, 'w', encoding='utf-8') as f:
            f.write(source_str)

        # Schedule the build. Omitting this commit causes tests to fail. ???
        current.db.commit()
        task = current.scheduler.queue_task(_scheduled_builder, pargs=[
            feedback_struct['builder'], temp_source_path, sphinx_base_path,
            sphinx_source_path, sphinx_out_path, source_path], immediate=True)
        if task.errors:
            return {
                'errors': ['Error in scheduling build task: {}'
                    .format(task.errors)]
            }
        # In order to monitor the status of the scheduled task, commit it now. (web2py assumes that the current request wouldn't want to monitor its own scheduled task.) This allows the workers to see it and begin work.
        current.db.commit()
        # Poll until the scheduled build completes.
        while True:
            time.sleep(0.5)
            task_status = current.scheduler.task_status(task.id, output=True)
            if task_status.scheduler_task.status == 'EXPIRED':
                # Remove the task entry, since it's no longer needed.
                del current.db.scheduler_task[task_status.scheduler_task.id]
                return { 'errors': ['Build task expired.'] }
            elif task_status.scheduler_task.status == 'TIMEOUT':
                del current.db.scheduler_task[task_status.scheduler_task.id]
                return { 'errors': ['Build task timed out.'] }
            elif task_status.scheduler_task.status == 'FAILED':
                # This also deletes the ``scheduler_run`` record.
                del current.db.scheduler_task[task_status.scheduler_task.id]
                return {
                    'errors': ['Exception during build: {}'.
                        format(task_status.scheduler_run.traceback)]
                }
            elif task_status.scheduler_task.status == 'COMPLETED':
                # This also deletes the ``scheduler_run`` record.
                del current.db.scheduler_task[task_status.scheduler_task.id]
                output, is_correct = json.loads(task_status.scheduler_run.run_result)

                return {
                    # The answer.
                    'answer': {
                        # Strip whitespace and return only the last 4K or data or so.
                        # There's no need for more -- it's probably just a crashed or
                        # confused program spewing output, so don't waste bandwidth or
                        # storage space on it.
                        'resultString': output.strip()[-4096:],
                    },
                    'correct': is_correct,
                }
    finally:
        shutil.rmtree(temp_path)


# This function should take a list of code snippets and modify them to prepare
# for the platform-specific compile. For example, add a line number directive
# to the beginning of each.
def _platform_edit(
    # The builder which will be used to build these snippets.
    builder,
    # A list of code snippets submitted by the user.
    code_snippets,
    # The name of the source file into which these snippets will be inserted.
    source_path):

    # Prepend a line number directive to each snippet. I can't get this to work
    # in the assembler. I tried:
    #
    # - From Section 4.11 (Misc directives):
    #
    #   -   ``.appline 1``
    #   -   ``.ln 1`` (produces the message ``Error: unknown pseudo-op: `.ln'``.
    #       But if I use the assembly option ``-a``, the listing file show that
    #       this directive inserts line 1 of the source .s file into the listing
    #       file. ???
    #   -   ``.loc 1 1`` (trying ``.loc 1, 1`` produces ``Error: rest of line
    #       ignored; first ignored character is `,'``)
    #
    # - From Section 4.12 (directives for debug information):
    #
    #   -   ``.line 1``. I also tried this inside a ``.def/.endef`` pair, which
    #       just produced error messages.
    #
    # Perhaps saving each snippet to a file, then including them via
    # ``.include`` would help. Ugh.
    #
    # Select what to prepend based on the language.
    ext = os.path.splitext(source_path)[1]
    if ext == '.c':
        # See https://gcc.gnu.org/onlinedocs/cpp/Line-Control.html.
        fmt = '#line 1 "box {}"\n'
    elif ext == '.s':
        fmt = ''
    elif ext == '.py':
        # Python doesn't (easily) support `setting line numbers <https://lists.gt.net/python/python/164854>`_.
        fmt = ''
    else:
        # This is an unsupported language. It would be nice to report this as an error instead of raising an exception.
        raise RuntimeError('Unsupported extension {}'.format(ext))
    return [fmt.format(index + 1) + code_snippets[index]
            for index in range(len(code_snippets))]


# Transform the arguments to ``subprocess.run`` into a string showing what
# command will be executed.
def _subprocess_string(*args, **kwargs):
    return kwargs.get('cwd', '') + '% ' + ' '.join(args[0]) + '\n'


# This function should run the provided code and report the results. It will
# vary for a given compiler and language.
def _scheduled_builder(
    # The name of the builder to use.
    builder,
    # An absolute path to the file which contains code to test. The file resides in a
    # temporary directory, which should be used to hold any additional files
    # produced by the test.
    file_path,
    # An absolute path to the Sphinx root directory.
    sphinx_base_path,
    # A relative path to the Sphinx source path from the ``sphinx_base_path``.
    sphinx_source_path,
    # A relative path to the Sphinx output path from the ``sphinx_base_path``.
    sphinx_out_path,
    # A relative path to the source file from the ``sphinx_source_path``, based
    # on the submitting web page.
    source_path):

    if builder == 'unsafe-python' and os.environ.get('WEB2PY_CONFIG') == 'test':
        # Run the test in Python. This is for testing only, and should never be used in production; instead, this should be run in a limited Docker container. For simplicity, it lacks a timeout.
        #
        # First, copy the test to the temp directory. Otherwise, running the test file from its book location means it will import the solution, which is in the same directory.
        cwd = os.path.dirname(file_path)
        test_file_name = os.path.splitext(os.path.basename(file_path))[0] + '-test.py'
        dest_test_path = os.path.join(cwd, test_file_name)
        shutil.copyfile(os.path.join(sphinx_base_path, sphinx_source_path,
                os.path.dirname(source_path), test_file_name),
                dest_test_path)
        try:
            str_out = subprocess.check_output([sys.executable, dest_test_path],
                stderr=subprocess.STDOUT, universal_newlines=True, cwd=cwd)
            return str_out, 100
        except subprocess.CalledProcessError as e:
            #from gluon.debug import dbg; dbg.set_trace()
            return e.output, 0
    elif builder != 'pic24-xc16-bullylib':
        raise RuntimeError('Unknown builder {}'.format(builder))

    # Assemble or compile the source. We assume that the binaries are already in the path.
    xc16_path = ''
    # Compile in the temporary directory, in which ``file_path`` resides.
    sp_args = dict(
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        cwd=os.path.dirname(file_path),
    )
    o_path = file_path + '.o'
    extension = os.path.splitext(file_path)[1]
    if extension == '.s':
        args = [os.path.join(xc16_path, 'xc16-as'), '-omf=elf', '-g',
                '--processor=33EP128GP502', file_path, '-o' + o_path]
    elif extension == '.c':
        args = [os.path.join(xc16_path, 'xc16-gcc'), '-mcpu=33EP128GP502', '-omf=elf', '-g', '-O0', '-msmart-io=1', '-Wall', '-Wextra', '-Wdeclaration-after-statement', '-I' + os.path.join(sphinx_base_path, sphinx_source_path, 'lib/include'), '-I' + os.path.join(sphinx_base_path, sphinx_source_path, 'tests'), '-I' + os.path.join(sphinx_base_path, sphinx_source_path, 'tests/platform/Microchip_PIC24'), '-I' + os.path.join(sphinx_base_path, sphinx_source_path, os.path.dirname(source_path)), file_path, '-c', '-o' + o_path]
    else:
        raise RuntimeError('Unknown file extension in {}.'.format(file_path))
    out = _subprocess_string(args, **sp_args)
    try:
        out += subprocess.check_output(args, **sp_args)
    except subprocess.CalledProcessError as e:
        out += e.output
        return out, 0

    # Link.
    elf_path = file_path + '.elf'
    waf_root = os.path.normpath(os.path.join(sphinx_base_path, sphinx_out_path,
        BUILD_SYSTEM_PATH, sphinx_source_path))
    test_object_path = os.path.join(waf_root,
        os.path.splitext(source_path)[0] + '-test.c.1.o')
    args = [os.path.join(xc16_path, 'xc16-gcc'), '-omf=elf', '-Wl,--heap=100,--stack=16,--check-sections,--data-init,--pack-data,--handles,--isr,--no-gc-sections,--fill-upper=0,--stackguard=16,--no-force-link,--smart-io', '-Wl,--script=' + os.path.join(sphinx_base_path, sphinx_source_path, 'lib/lkr/p33EP128GP502_bootldr.gld'), test_object_path, o_path, os.path.join(waf_root, 'lib/src/pic24_clockfreq.c.1.o'), os.path.join(waf_root, 'lib/src/pic24_configbits.c.1.o'), os.path.join(waf_root, 'lib/src/pic24_serial.c.1.o'), os.path.join(waf_root, 'lib/src/pic24_timer.c.1.o'), os.path.join(waf_root, 'lib/src/pic24_uart.c.1.o'), os.path.join(waf_root, 'lib/src/pic24_util.c.1.o'), os.path.join(waf_root, 'tests/test_utils.c.1.o'), os.path.join(waf_root, 'tests/test_assert.c.1.o'), '-o' + elf_path, '-Wl,-Bstatic', '-Wl,-Bdynamic']
    out += '\n' + _subprocess_string(args, **sp_args)
    try:
        out += subprocess.check_output(args, **sp_args)
    except subprocess.CalledProcessError as e:
        out += e.output
        return out, 0

    # Simulate. Create the simulation commands.
    simout_path = file_path + '.simout'
    ss = get_sim_str_sim30('dspic33epsuper', elf_path, simout_path)
    # Run the simulation. This is a re-coded version of ``wscript.sim_run`` -- I
    # couldn't find a way to re-use that code.
    sim_ret = 0
    args = [os.path.join(xc16_path, 'sim30')]
    out += '\nTest results:\n' + _subprocess_string(args, **sp_args)
    timeout_list = []
    try:
        p = subprocess.Popen(args, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, **sp_args)
        # Horrible kludge: implement a crude timeout. Instead, use ``timeout``
        # with Python 3.
        def on_timeout(msg_list):
            p.terminate()
            msg_list += ['\n\nTimeout.']
        t = Timer(3, on_timeout, [timeout_list])
        t.start()
        p.communicate(ss)
        sim_ret = p.returncode
    except subprocess.CalledProcessError as e:
        sim_ret = 1
    # Check the output.
    t.cancel()
    with open(simout_path, encoding='utf-8') as f:
        out += f.read().rstrip()
    # Put the timeout string at the end of all the simulator output.
    out += ''.join(timeout_list)
    return out, (100 if not sim_ret and out.endswith('Correct.') else 0)
