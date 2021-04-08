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
import datetime

# Third-party imports
# -------------------
from polling2 import poll
import pytest
from runestone.clickableArea.test import test_clickableArea
from runestone.poll.test.test_poll import _test_poll
from runestone.shortanswer.test import test_shortanswer
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


# Tricky fixures
# --------------
# The URL to fetch in order to do testing varies by the type of test:
#
# #.    When performing client-side testing in Runestone Components, the URL is usually "/index.html". A fixture defined in client testing code handles this; see the ``selenium_utils_1`` fixture in ``test_clickableArea.py`` in the Runestone Component, for example. The client-side tests then use this fixture.
# #.    When performing plain server-side testing, the URL is "/path/to/book/index.html"; see ``selenium_utils_user.get_book_url``. The fixture below handles this. Then, inside a plain server-side test, the test invokes the client test directly, meaning that it passes its already-run fixture (which fetched the plain server-side testing page) to the client test, bypassing the client fixture.
# #.    When performing selectquestion server-side testing, the URL is "/path/to/book/selectquestion.html". The next figure handles this. It likewise calls the plain server-side text with its already-run fixture, which has fetched the selectquestion server-side testing page.
#
# A fixture for plain server-side testing.
@pytest.fixture
def selenium_utils_user_1(selenium_utils_user):
    selenium_utils_user.get_book_url("index.html")
    return selenium_utils_user


# A fixture for selectquestion server-side testing.
@pytest.fixture
def selenium_utils_user_2(selenium_utils_user):
    selenium_utils_user.get_book_url("selectquestion.html")
    return selenium_utils_user


# Tests
# =====
#
# ClickableArea
# -------------
def test_clickable_area_1(selenium_utils_user_1, runestone_db):
    div_id = "test_clickablearea_1"
    selenium_utils_user_1.wait_until_ready(div_id)

    def check_constant_ans(index):
        ans = get_answer(db, (db.clickablearea_answers.div_id == div_id), index + 1)[
            index
        ]
        assert ans.timestamp - datetime.datetime.now() < datetime.timedelta(seconds=5)
        assert ans.div_id == div_id
        assert ans.sid == selenium_utils_user_1.user.username
        assert ans.course_name == selenium_utils_user_1.user.course.course_name
        return ans

    test_clickableArea.test_ca1(selenium_utils_user_1)
    db = runestone_db
    ans = check_constant_ans(0)
    assert ans.answer == ""
    assert ans.correct == False
    assert ans.percent == None

    test_clickableArea.test_ca2(selenium_utils_user_1)
    ans = check_constant_ans(1)
    assert ans.answer == "0;2"
    assert ans.correct == True
    assert ans.percent == 1.0

    # TODO: There are a lot more clickable area tests that could be easily ported!


# Fitb
# ----
# Test server-side logic in FITB questions. TODO: lots of gaps in these tests.
def test_fitb(selenium_utils_user_1):
    # Browse to the page with a fitb question.
    d = selenium_utils_user_1.driver
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
        selenium_utils_user_1.wait.until(
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
def test_poll_1(selenium_utils_user_1, runestone_db):
    id = "test_poll_1"
    _test_poll(selenium_utils_user_1, id)
    db = runestone_db
    assert (
        get_answer(db, (db.useinfo.div_id == id) & (db.useinfo.event == "poll"), 1)[
            0
        ].act
        == "4"
    )


# Short answer
# ------------
def test_short_answer_1(selenium_utils_user_1, runestone_db):
    id = "test_short_answer_1"
    selenium_utils_user_1.wait_until_ready(id)

    # The first test doesn't click the submit button.
    db = runestone_db
    expr = db.shortanswer_answers.div_id == id
    test_shortanswer.test_sa1(selenium_utils_user_1)
    s = get_answer(db, expr, 0)

    # The second test clicks submit with no text.
    test_shortanswer.test_sa2(selenium_utils_user_1)
    s = get_answer(db, expr, 1)
    assert s[0].answer == ""

    # The third test types text then submits it.
    test_shortanswer.test_sa3(selenium_utils_user_1)
    s = get_answer(db, expr, 2)
    assert s[1].answer == "My answer"

    # The fourth test is just a duplicate of the third test.
    test_shortanswer.test_sa4(selenium_utils_user_1)
    s = get_answer(db, expr, 3)
    assert s[2].answer == "My answer"


# Selectquestion
# --------------
# Check rendering of selectquestion, which requires server-side support.
def test_selectquestion_1(selenium_utils_user_2, runestone_db):
    test_poll_1(selenium_utils_user_2, runestone_db)


@pytest.mark.skip(reason="The spreadsheet component doesn't support selectquestion.")
def test_selectquestion_2(selenium_utils_user_2):
    test_spreadsheet_1(selenium_utils_user_2)


def test_selectquestion_3(selenium_utils_user_2, runestone_db):
    test_clickable_area_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_20(selenium_utils_user_2, runestone_db):
    test_short_answer_1(selenium_utils_user_2, runestone_db)


# Spreadsheet
# -----------
def test_spreadsheet_1(selenium_utils_user_1):
    _test_ss_autograde(selenium_utils_user_1)
