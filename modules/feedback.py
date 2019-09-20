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
from io import open
import json

# Third-party imports
# -------------------
from gluon import current
from runestone.lp.lp_common_lib import (
    STUDENT_SOURCE_PATH,
    code_here_comment,
    read_sphinx_config,
)

# Local imports
# -------------
from scheduled_builder import _scheduled_builder


# Return ``(True, feedback)`` if feedback should be computed on the server,
# instead of the client. This function assumes that the inputs have already been validated.
def is_server_feedback(div_id, course):
    # Get the information about this question. Per the `web2py docs
    # <http://web2py.com/books/default/chapter/29/04/the-core?search=import+module#Sharing-the-global-scope-with-modules-using-the-current-object>`_,
    # an assignment in ``models/db.py`` makes ``current.db`` available.
    query_results = (
        current.db(
            (current.db.questions.name == div_id)
            & (current.db.questions.base_course == current.db.courses.base_course)
            & (current.db.courses.course_name == course)
        )
        .select(current.db.questions.feedback, current.db.courses.login_required)
        .first()
    )

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
        answer = answer_json.split(",")
    displayFeed = []
    isCorrectArray = []
    # The overall correctness of the entire problem.
    correct = True
    for blank, feedback_for_blank in zip(answer, feedback):
        if not blank:
            isCorrectArray.append(None)
            displayFeed.append("No answer provided.")
            correct = False
        else:
            # The correctness of this problem depends on if the first item matches.
            is_first_item = True
            # Check everything but the last answer, which always matches.
            for fb in feedback_for_blank[:-1]:
                if "regex" in fb:
                    if re.search(
                        fb["regex"], blank, re.I if fb["regexFlags"] == "i" else 0
                    ):
                        isCorrectArray.append(is_first_item)
                        if not is_first_item:
                            correct = False
                        displayFeed.append(fb["feedback"])
                        break
                else:
                    assert "number" in fb
                    min_, max_ = fb["number"]
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
                        displayFeed.append(fb["feedback"])
                        break
                is_first_item = False
            # Nothing matched. Use the last feedback.
            else:
                isCorrectArray.append(False)
                correct = False
                displayFeed.append(feedback_for_blank[-1]["feedback"])

    # Return grading results to the client for a non-test scenario.
    res = dict(correct=correct, displayFeed=displayFeed, isCorrectArray=isCorrectArray)
    return "T" if correct else "F", res


# lp feedback
# ===========
def lp_feedback(code_snippets, feedback_struct):
    db = current.db
    base_course = (
        db((db.courses.id == current.auth.user.course_id))
        .select(db.courses.base_course)
        .first()
        .base_course
    )
    sphinx_base_path = os.path.join(current.request.folder, "books", base_course)
    source_path = feedback_struct["source_path"]
    # Read the Sphinx config file to find paths relative to this directory.
    sphinx_config = read_sphinx_config(sphinx_base_path)
    if not sphinx_config:
        return {
            "errors": [
                "Unable to load Sphinx configuration file from {}".format(
                    sphinx_base_path
                )
            ]
        }
    sphinx_source_path = sphinx_config["SPHINX_SOURCE_PATH"]
    sphinx_out_path = sphinx_config["SPHINX_OUT_PATH"]

    # Next, read the student source in for the program the student is working on.
    try:
        # Find the path to the student source file.
        abs_source_path = os.path.normpath(
            os.path.join(
                sphinx_base_path, sphinx_out_path, STUDENT_SOURCE_PATH, source_path
            )
        )
        with open(abs_source_path, encoding="utf-8") as f:
            source_str = f.read()
    except Exception as e:
        return {
            "errors": ["Cannot open source file {}: {}.".format(abs_source_path, e)]
        }

    # Create a snippet-replaced version of the source, by looking for "put code
    #   here" comments and replacing them with the provided code. To do so,
    # first split out the "put code here" comments.
    split_source = source_str.split(code_here_comment(source_path))
    # Sanity check! Source with n "put code here" comments splits into n+1
    # items, into which the n student code snippets should be interleaved.
    if len(split_source) - 1 != len(code_snippets):
        return {"errors": ["Wrong number of snippets."]}
    # Interleave these with the student snippets.
    interleaved_source = [None] * (2 * len(split_source) - 1)
    interleaved_source[::2] = split_source
    try:
        interleaved_source[1::2] = _platform_edit(
            feedback_struct["builder"], code_snippets, source_path
        )
    except Exception as e:
        return {"errors": ["An exception occurred: {}".format(e)]}
    # Join them into a single string. Make sure newlines separate everything.
    source_str = "\n".join(interleaved_source)

    # Create a temporary directory, then write the source there.
    with tempfile.TemporaryDirectory() as temp_path:
        temp_source_path = os.path.join(temp_path, os.path.basename(source_path))
        with open(temp_source_path, "w", encoding="utf-8") as f:
            f.write(source_str)

        try:
            res = _scheduled_builder.delay(
                feedback_struct["builder"],
                temp_source_path,
                sphinx_base_path,
                sphinx_source_path,
                sphinx_out_path,
                source_path,
            )
            output, is_correct = res.get(timeout=60)
        except Exception as e:
            return {"errors": ["Error in build task: {}".format(e)]}
        else:
            return {
                # The answer.
                "answer": {
                    # Strip whitespace and return only the last 4K or data or so.
                    # There's no need for more -- it's probably just a crashed or
                    # confused program spewing output, so don't waste bandwidth or
                    # storage space on it.
                    "resultString": output.strip()[-4096:]
                },
                "correct": is_correct,
            }


# This function should take a list of code snippets and modify them to prepare
# for the platform-specific compile. For example, add a line number directive
# to the beginning of each.
def _platform_edit(
    # The builder which will be used to build these snippets.
    builder,
    # A list of code snippets submitted by the user.
    code_snippets,
    # The name of the source file into which these snippets will be inserted.
    source_path,
):

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
    if ext == ".c":
        # See https://gcc.gnu.org/onlinedocs/cpp/Line-Control.html.
        fmt = '#line 1 "box {}"\n'
    elif ext == ".s":
        fmt = ""
    elif ext == ".py":
        # Python doesn't (easily) support `setting line numbers <https://lists.gt.net/python/python/164854>`_.
        fmt = ""
    else:
        # This is an unsupported language. It would be nice to report this as an error instead of raising an exception.
        raise RuntimeError("Unsupported extension {}".format(ext))
    return [
        fmt.format(index + 1) + code_snippets[index]
        for index in range(len(code_snippets))
    ]
