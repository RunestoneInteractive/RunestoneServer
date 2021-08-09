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
import json

# Third-party imports
# -------------------
from polling2 import poll
import pytest
from runestone.activecode.test import test_activecode
from runestone.clickableArea.test import test_clickableArea
from runestone.dragndrop.test import test_dragndrop
from runestone.fitb.test import test_fitb
from runestone.mchoice.test import test_assess
from runestone.parsons.test import test_parsons
from runestone.poll.test import test_poll
from runestone.shortanswer.test import test_shortanswer
from runestone.spreadsheet.test import test_spreadsheet
from runestone.timed.test import test_timed
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Local imports
# -------------
# None.


# Utilities
# =========
# Poll the database waiting for the client to perform an update via Ajax.
def get_answer(db, expr, minimum_len):
    return poll(
        lambda: db(expr).select(),
        check_success=lambda s: len(s) >= minimum_len,
        step=0.1,
        timeout=10,
    )


# Check the fields common to the tables of most Runestone components.
def check_common_fields_raw(selenium_utils_user, db, query, index, div_id):
    row = get_answer(db, query, index + 1)[index]
    assert row.timestamp - datetime.datetime.now() < datetime.timedelta(seconds=5)
    assert row.div_id == div_id
    assert row.sid == selenium_utils_user.user.username
    assert row.course_name == selenium_utils_user.user.course.course_name
    return row


# Return the answer, correct, and percent fields after checking common fields.
def check_common_fields(selenium_utils_user, db, query, index, div_id):
    row = check_common_fields_raw(selenium_utils_user, db, query, index, div_id)
    return row.answer, row.correct, row.percent


# Tricky fixures
# --------------
# The URL to fetch in order to do testing varies by the type of test:
#
# #.    When performing client-side testing in Runestone Components, the URL is usually "/index.html". A fixture defined in client testing code handles this; see the ``selenium_utils_1`` fixture in ``test_clickableArea.py`` in the Runestone Component, for example. The client-side tests then use this fixture.
# #.    When performing server-side testing, the URL is "/path/to/book/<url_here>.html"; see ``selenium_utils_user.get_book_url``. The fixture below provides one example of this. Then, inside a server-side test, the test invokes the client test directly, meaning that it passes its already-run fixture (which fetched the plain server-side testing page) to the client test, bypassing the client fixture.
#
# Both client-side and server-side tests must be structured carefully for this to work:
# - Client-side tests must invoke ``selenium_utils.wait_until_ready(div_id)``.
# - Client-side tests must **not** invoke ``selenium_utils.get`` in the body of the test, since this prevents server-side tests from fetching from the correct server-side location. Instead, invoke this in a fixture passed to the test, allow server-side tests to override this by passing a different fixture.
# - The ``div_id`` of client-side tests must match the div_id of server-side tests, meaning the two ``.rst`` files containing tests must use the same ``div_id``.
#
# A fixture for plain server-side testing.
@pytest.fixture
def selenium_utils_user_1(selenium_utils_user):
    selenium_utils_user.get_book_url("index.html")
    return selenium_utils_user


# Tests
# =====
#
# Active code
# -----------
# A fixture for active code server-side testing.
@pytest.fixture
def selenium_utils_user_ac(selenium_utils_user):
    selenium_utils_user.get_book_url("activecode.html")
    return selenium_utils_user


def test_activecode_1(selenium_utils_user_ac, runestone_db):
    db = runestone_db

    def ac_check_fields(index, div_id):
        row = get_answer(db, db.code.acid == div_id, index + 1)[index]
        assert row.timestamp - datetime.datetime.now() < datetime.timedelta(seconds=5)
        assert row.acid == div_id
        assert row.sid == selenium_utils_user_ac.user.username
        assert row.course_id == selenium_utils_user_ac.user.course.course_id
        return row

    test_activecode.test_history(selenium_utils_user_ac)
    row = ac_check_fields(0, "test_activecode_2")
    assert row.emessage == "success"
    assert row.code == "print('Goodbye')"
    assert row.grade == None
    assert row.comment == None
    assert row.language == "python"

    # TODO: There are a lot more activecode tests that could be easily ported!


# ClickableArea
# -------------
def test_clickable_area_1(selenium_utils_user_1, runestone_db):
    db = runestone_db
    div_id = "test_clickablearea_1"

    def ca_check_common_fields(index):
        return check_common_fields(
            selenium_utils_user_1,
            db,
            db.clickablearea_answers.div_id == div_id,
            index,
            div_id,
        )

    test_clickableArea.test_ca1(selenium_utils_user_1)
    assert ca_check_common_fields(0) == ("", False, None)

    test_clickableArea.test_ca2(selenium_utils_user_1)
    assert ca_check_common_fields(1) == ("0;2", True, 1)

    # TODO: There are a lot more clickable area tests that could be easily ported!


# Drag-n-drop
# -----------
def test_dnd_1(selenium_utils_user_1, runestone_db):
    db = runestone_db
    div_id = "test_dnd_1"

    def dnd_check_common_fields(index):
        return check_common_fields(
            selenium_utils_user_1,
            db,
            db.dragndrop_answers.div_id == div_id,
            index,
            div_id,
        )

    test_dragndrop.test_dnd1(selenium_utils_user_1)
    assert dnd_check_common_fields(0) == ("-1;-1;-1", False, None)

    # TODO: There are more dnd tests that could easily be ported!


# Fitb
# ----
# Test server-side logic in FITB questions.
def test_fitb_1(selenium_utils_user_1, runestone_db):
    db = runestone_db

    def fitb_check_common_fields(index, div_id):
        answer, correct, percent = check_common_fields(
            selenium_utils_user_1,
            db,
            db.fitb_answers.div_id == div_id,
            index,
            div_id,
        )
        return json.loads(answer), correct, percent

    test_fitb.test_fitb1(selenium_utils_user_1)
    assert fitb_check_common_fields(0, "test_fitb_string") == (["", ""], False, 0)

    test_fitb.test_fitb2(selenium_utils_user_1)
    assert fitb_check_common_fields(1, "test_fitb_string") == (["red", ""], False, 0.5)

    test_fitb.test_fitb3(selenium_utils_user_1)
    assert fitb_check_common_fields(2, "test_fitb_string") == (["red", "away"], True, 1)

    test_fitb.test_fitb4(selenium_utils_user_1)
    assert fitb_check_common_fields(3, "test_fitb_string") == (["red", "away"], True, 1)

    test_fitb.test_fitboneblank_too_low(selenium_utils_user_1)
    assert fitb_check_common_fields(0, "test_fitb_number") == ([" 6"], False, 0)

    test_fitb.test_fitboneblank_wildcard(selenium_utils_user_1)
    assert fitb_check_common_fields(1, "test_fitb_number") == (["I give up"], False, 0)

    test_fitb.test_fitbfillrange(selenium_utils_user_1)
    assert fitb_check_common_fields(2, "test_fitb_number") == ([" 6.28 "], True, 1)

    test_fitb.test_fitbregex(selenium_utils_user_1)
    assert fitb_check_common_fields(0, "test_fitb_regex_1") == (
        [" maire ", "LITTLE", "2"],
        True,
        1,
    )

    test_fitb.test_regexescapes1(selenium_utils_user_1)
    assert fitb_check_common_fields(0, "test_fitb_regex_2") == (
        [r"C:\windows\system"],
        True,
        1,
    )

    test_fitb.test_regexescapes2(selenium_utils_user_1)
    assert fitb_check_common_fields(0, "test_fitb_regex_3") == (["[]"], True, 1)


# Lp
# --
def test_lp_1(selenium_utils_user):
    su = selenium_utils_user
    href = "lp_demo.py.html"
    su.get_book_url(href)
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

    # Wait until the build finishes.
    su.wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#lp-result ~ div"), "Correct. Grade: 100%"
        )
    )

    # Refresh the page. See if saved snippets are restored.
    su.get_book_url(href)
    su.wait_until_ready(id)
    assert (
        su.driver.execute_script(f'return LPList["{id}"].textAreas[0].getValue();')
        == code
    )


# Mchoice
# -------
def test_mchoice_1(selenium_utils_user_1, runestone_db):
    su = selenium_utils_user_1
    db = runestone_db
    div_id = "test_mchoice_1"

    def mc_check_common_fields(index):
        return check_common_fields(
            su, db, db.mchoice_answers.div_id == div_id, index, div_id
        )

    test_assess.test_ma1(selenium_utils_user_1)
    assert mc_check_common_fields(0) == ("", False, None)

    test_assess.test_ma2(selenium_utils_user_1)
    assert mc_check_common_fields(1) == ("0,2", True, 1)

    # TODO: There are a lot more multiple choice tests that could be easily ported!


# Parsons's problems
# =================
def test_parsons_1(selenium_utils_user_1, runestone_db):
    db = runestone_db

    def pp_check_common_fields(index, div_id):
        row = check_common_fields_raw(
            selenium_utils_user_1,
            db,
            db.parsons_answers.div_id == div_id,
            index,
            div_id,
        )
        return row.answer, row.correct, row.percent, row.source

    test_parsons.test_general(selenium_utils_user_1)
    assert pp_check_common_fields(0, "test_parsons_1") == (
        "-",
        False,
        None,
        "0_0-1_2_0-3_4_0-6_0-5_0",
    )
    assert pp_check_common_fields(1, "test_parsons_1") == (
        "0_0-1_2_1-3_4_1-5_1",
        True,
        1.0,
        "6_0",
    )

    # TODO: There are several more Parsons's problems tests that could be easily ported.


# Poll
# ----
def test_poll_1(selenium_utils_user_1, runestone_db):
    id = "test_poll_1"
    test_poll.test_poll(selenium_utils_user_1)
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
# A fixture for selectquestion server-side testing.
@pytest.fixture
def selenium_utils_user_2(selenium_utils_user):
    selenium_utils_user.get_book_url("selectquestion.html")
    return selenium_utils_user


# Check rendering of selectquestion, which requires server-side support.
def test_selectquestion_1(selenium_utils_user_2, runestone_db):
    test_poll_1(selenium_utils_user_2, runestone_db)


@pytest.mark.skip(reason="The spreadsheet component doesn't support selectquestion.")
def test_selectquestion_2(selenium_utils_user_2):
    test_spreadsheet_1(selenium_utils_user_2)


def test_selectquestion_3(selenium_utils_user_2, runestone_db):
    test_clickable_area_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_4(selenium_utils_user_2, runestone_db):
    test_fitb_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_5(selenium_utils_user_2, runestone_db):
    test_mchoice_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_6(selenium_utils_user_2, runestone_db):
    test_parsons_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_7(selenium_utils_user_2, runestone_db):
    test_dnd_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_8(selenium_utils_user_2, runestone_db):
    test_activecode_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_10(selenium_utils_user_2, runestone_db):
    test_short_answer_1(selenium_utils_user_2, runestone_db)


def test_selectquestion_11(selenium_utils_user_2, runestone_db):
    _test_timed_1(selenium_utils_user_2, runestone_db, "test_timed_2")


# Spreadsheet
# -----------
def test_spreadsheet_1(selenium_utils_user_1):
    test_spreadsheet.test_ss_autograde(selenium_utils_user_1)


# Timed questions
# ---------------
@pytest.fixture
def selenium_utils_user_timed(selenium_utils_user):
    selenium_utils_user.get_book_url("multiquestion.html")
    return selenium_utils_user


# Provide the ability to invoke tests with a specific div_id, since the selectquestion test is a different problem with a different div_id than the plain test.
def _test_timed_1(selenium_utils_user_timed, runestone_db, timed_divid):
    db = runestone_db

    def tt_check_common_fields(index, div_id):
        row = check_common_fields_raw(
            selenium_utils_user_timed, db, db.timed_exam.div_id == div_id, index, div_id
        )
        # The tests should finish the timed exam in a few seconds.
        assert row.time_taken < 10
        return row.correct, row.incorrect, row.skipped, row.reset

    test_timed._test_1(selenium_utils_user_timed, timed_divid)
    # import pdb; pdb.set_trace()
    assert tt_check_common_fields(0, timed_divid) == (0, 0, 0, None)
    assert tt_check_common_fields(1, timed_divid) == (6, 0, 1, None)


def xtest_timed_1(selenium_utils_user_timed, runestone_db):
    _test_timed_1(selenium_utils_user_timed, runestone_db, "test_timed_1")
