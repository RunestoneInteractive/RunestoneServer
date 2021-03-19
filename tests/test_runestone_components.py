# *********************************************
# |docname| - Tests of the Runestone Components
# *********************************************
# These tests check both client-side and server-side aspects of the Runestone Components.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
# None.
#
# Third-party imports
# -------------------
from polling2 import poll
from runestone.poll.test.test_poll import _test_poll

#
# Local imports
# -------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Utilities
# =========
# Poll the database waiting for the client to perform an update via Ajax.
def get_answer(db, expr, expected_len):
    return poll(
        lambda: db(expr).select(),
        check_success=lambda s: len(s) == expected_len,
        step=0.1,
        timeout=10,
    )


# Tests
# =====
# Test server-side logic in FITB questions.
def test_fitb(selenium_utils_user):
    # Browse to the page with a fitb question.
    d = selenium_utils_user.driver
    selenium_utils_user.get("books/published/test_course_1/index.html")
    id = "test_fitb_numeric"
    fitb = d.find_element_by_id(id)
    blank = fitb.find_elements_by_tag_name("input")[0]
    check_me_button = fitb.find_element_by_tag_name("button")
    feedback_id = id + "_feedback"

    # Enter a value and check it
    def check_val(val, feedback_str="Correct"):
        # Erase any previous answer text.
        blank.clear()
        blank.send_keys(val)
        check_me_button.click()
        selenium_utils_user.wait.until(
            EC.text_to_be_present_in_element((By.ID, feedback_id), feedback_str)
        )

    check_val("10")
    # Check this next, since it expects a different answer -- two correct answers in a row are harder to distinguish (has the new text been updated yet or not?).
    check_val("11", "Close")
    # Ensure spaces don't prevent correct numeric parsing.
    check_val(" 10 ")


def _test_poll_1(selenium_utils_user, runestone_db, relative_url):
    selenium_utils_user.get(f"books/published/test_course_1/{relative_url}")

    id = "test_poll_1"
    _test_poll(selenium_utils_user, id)
    db = runestone_db
    assert (
        get_answer(db, (db.useinfo.div_id == id) & (db.useinfo.event == "poll"), 1)[
            0
        ].act
        == "4"
    )


def test_poll_1(selenium_utils_user, runestone_db):
    _test_poll_1(selenium_utils_user, runestone_db, "index.html")


# Check rendering of selectquestion, which requires server-side support.
def test_selectquestion_1(selenium_utils_user, runestone_db):
    _test_poll_1(selenium_utils_user, runestone_db, "selectquestion.html")
