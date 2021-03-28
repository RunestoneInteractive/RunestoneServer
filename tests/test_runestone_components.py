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
import pytest
from runestone.poll.test.test_poll import _test_poll
from runestone.spreadsheet.test.test_spreadsheet import _test_ss_autograde
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Local imports
# -------------
# None.


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
# Fitb
# ----
# Test server-side logic in FITB questions. TODO: lots of gaps in these tests.
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


# Lp
# --
def test_lp_1(selenium_utils_user):
    su = selenium_utils_user
    href = "books/published/test_course_1/lp_demo.py.html"
    su.get(href)
    id = "test_lp_1"
    su.wait_until_ready(id)

    snippets = su.driver.find_elements_by_class_name("code_snippet")
    assert len(snippets) == 1
    check_button = su.driver.find_element_by_id(id)
    result_id = "lp-result"
    result_area = su.driver.find_element_by_id(result_id)

    # Set snippets.
    code = "def one(): return 1"
    su.driver.execute_script(f'LPList["{id}"].textAreas[0].setValue("{code}");')
    assert not result_area.text

    # Click the test button.
    check_button.click()
    su.wait.until(
        EC.text_to_be_present_in_element_value((By.ID, "lp-result"), "Building...")
    )

    # Wait until the build finishes. To find this, I used the Chrome inspector; right-click on the element, then select "Copy > Copy full XPath".
    su.wait.until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "/html/body/div[3]/div[1]/div[3]/div"), "Correct. Grade: 100%"
        )
    )

    # Refresh the page. See if saved snippets are restored.
    su.get(href)
    su.wait_until_ready(id)
    assert (
        su.driver.execute_script(f'return LPList["{id}"].textAreas[0].getValue();')
        == code
    )


# Poll
# ----
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


# Selectquestion
# --------------
# Check rendering of selectquestion, which requires server-side support.
def test_selectquestion_1(selenium_utils_user, runestone_db):
    _test_poll_1(selenium_utils_user, runestone_db, "selectquestion.html")


@pytest.mark.skip(reason="The spreadsheet component doesn't support selectquestion.")
def test_selectquestion_2(selenium_utils_user):
    _test_spreadsheet_1(selenium_utils_user, "selectquestion.html")
