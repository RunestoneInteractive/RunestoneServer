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
import json

# Third-party imports
# -------------------
from gluon import current

# Local imports
# -------------
# None.


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
    if answer_json is None:
        return "F"

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
                        # Note that ``literal_eval`` does **not** discard leading / trailing spaces, but considers them indentation errors. So, explicitly invoke ``strip``.
                        val = ast.literal_eval(blank.strip())
                        in_range = val >= min_ and val <= max_
                    except Exception:
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

    # Note that this isn't a percentage, but a ratio where 1.0 == all correct.
    percent = (
        isCorrectArray.count(True) / len(isCorrectArray) if len(isCorrectArray) else 0
    )

    # Return grading results to the client for a non-test scenario.
    if current.settings.is_testing:
        res = dict(
            correct=True,
            displayFeed=["Response recorded."] * len(answer),
            isCorrectArray=[True] * len(answer),
            percent=1,
        )
    else:
        res = dict(
            correct=correct,
            displayFeed=displayFeed,
            isCorrectArray=isCorrectArray,
            percent=percent,
        )
    return "T" if correct else "F", res
