# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
# None.

# Third-party imports
# -------------------
import pytest
import io


# Local application imports
# -------------------------
# None.
#
#
# Globals
# =======
TEST_COURSE_NAME = 'course_name1'
TEST_SUBCHAPTER = 'team_evaluation_1'


# Test suite
# ==========
#
# Fixtures
# --------
# Set up the request to for testing team reports.
@pytest.fixture
def monkeypatch_request_folder(runestone_env, tmp_path):
    class _object(object):
        pass

    # Return an empty base course, which is appended to the request folder when definiing the location of the CSV file. See ``_load_teams()`` in ``models/team.py``.
    def mock_get_course_row():
        o = _object()
        o.base_course = ''
        return o

    runestone_env['get_course_row'] = mock_get_course_row

    # Use a temp directory for the request folder, where CSV files are stored. See ``make_csv``.
    request = runestone_env['request']
    request.folder = str(tmp_path)

    # Provide consistent dummy request arguments.
    request.args = ['books', 'published', TEST_COURSE_NAME]


# A fixtured version of importing ``get_team_members``.
@pytest.fixture
def get_team_members(runestone_env, monkeypatch_request_folder):
    return runestone_env['get_team_members']


# A fixtured version of importing ``team_report``.
@pytest.fixture
def team_report(runestone_env, monkeypatch_request_folder):
    return runestone_env['team_report']


# Create a CSV file for testing.
@pytest.fixture
def make_csv(tmp_path):

    def _make_csv(csv_contents, course_name=TEST_COURSE_NAME):
        csv_path = tmp_path / 'books/{}.csv'.format(course_name)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with io.open(str(csv_path), 'w', encoding='utf-8') as csv_file:
            csv_file.write(csv_contents)

    return _make_csv


# Make a CSV, then call ``get_team_members``.
@pytest.fixture
def get_team_members_from_csv(make_csv, get_team_members):

    def _get_team_members_from_csv(csv_contents, user_id, course_name=TEST_COURSE_NAME):
        make_csv(csv_contents, course_name)
        return get_team_members(user_id, course_name)

    return _get_team_members_from_csv


# Tests
# -----
# Test loading a non-existent file.
def test_1(get_team_members):
    team_name, team_member_list = get_team_members('', 'course_name1')
    assert 'No such file' in team_name


# Test an empty CSV file.
def test_2(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(u'', '')
    assert team_name.startswith('Error: User ID  not in')


# Test a one-line CSV file.
def test_3(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(u'\n', '')
    assert team_name.startswith('Error: Incorrect number of rows')


# Test wrong headings.
def test_4(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(u'user id,user name,team names\n', '')
    assert team_name.startswith('Error: Expected the third column')


# Test wrong number of rows.
def test_5(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(u'user id,user name,team name\n1,2,3,4,5', '')
    assert team_name.startswith('Error: Incorrect number of rows')


# Test newline before headings.
def test_5_1(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(u'\nuser id,user name,team name', '')
    assert team_name.startswith('Error: Incorrect number of rows')


# Test duplicate user ids.
def test_6(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(
        u'user id,user name,team name\n'
        'user_id1,user_name1,team_name1\n'
        'user_id1,user_name1,team_name1\n',
        'user_id1')
    assert team_name.startswith('Error: Duplicate user ID')


# Test incorrect user id.
def test_7(get_team_members_from_csv):
    team_name, team_member_list = get_team_members_from_csv(
        u'user id,user name,team name\n'
        'user_id1,user_name1,team_name1\n',
        'user_id2')
    assert team_name.startswith('Error: User ID user_id2 not in')


# Test the single-class, single-team case.
def test_8(get_team_members_from_csv):
    csv_contents = (
        u'user id,user name,team name\n'
        'user_id1,user_name1,team_name1\n'
        'user_id2,user_name2,team_name1\n'
        'user_id3,user_name3,team_name1\n'
        'user_id4,user_name4,team_name1\n'
    )
    team_name, team_member_list = get_team_members_from_csv(csv_contents, 'user_id1')
    assert team_name == 'team_name1'
    assert team_member_list == ['user_name2', 'user_name3', 'user_name4']

    team_name, team_member_list = get_team_members_from_csv(csv_contents, 'user_id2')
    assert team_name == 'team_name1'
    assert team_member_list == ['user_name1', 'user_name3', 'user_name4']


# Test multiple teams and courses with an empty row.
def test_9(get_team_members_from_csv):
    csv_contents = (
        u'user id,user name,team name\n'
        'user_id1,user_name1,team_name1\n'
        'user_id2,user_name2,team_name1\n'
        ',,\n'
        'user_id3,user_name3,team_name2\n'
        'user_id4,user_name4,team_name2\n'
    )
    team_name, team_member_list = get_team_members_from_csv(csv_contents, 'user_id1')
    assert team_name == 'team_name1'
    assert team_member_list == ['user_name2']

    team_name, team_member_list = get_team_members_from_csv(csv_contents, 'user_id3', 'course_name2')
    assert team_name == 'team_name2'
    assert team_member_list == ['user_name4']


# Test the team report function.
def test_team_report_1(make_csv, team_report):
    # Provide data and get the report.
    make_csv(
        u'user id,user name,team name\n'
        'user_id1,Alex Jones,team_name2\n'
        'user_id2,Cat Jones,team_name2\n'
        'user_id3,Ben Jones,team_name2\n'
        ',,\n'
        # Test users with no last name.
        'user_id4,user_name4,team_name1\n'
        'user_id5,user_name5,team_name1\n'
    )
    eval_data_dict, team_data_dict, grades = team_report(TEST_SUBCHAPTER, TEST_COURSE_NAME)

    # Check it.
    for user_id, name, teammate_netids in (
        ('user_id1', 'Alex Jones', ['user_id2', 'user_id3']),
        ('user_id2', 'Cat Jones', ['user_id1', 'user_id3']),
        ('user_id3', 'Ben Jones', ['user_id1', 'user_id2']),
        ('user_id4', 'user_name4', ['user_id5']),
        ('user_id5', 'user_name5', ['user_id4']),
    ):
        assert eval_data_dict[user_id].name == name
        assert eval_data_dict[user_id].teammate_netids == teammate_netids

    assert team_data_dict['team_name2'].team_netids == ['user_id1', 'user_id3', 'user_id2']
    assert team_data_dict['team_name1'].team_netids == ['user_id4', 'user_id5']
    assert list(team_data_dict) == ['team_name1', 'team_name2']


# Check that an empty CSV doesn't produce errors.
def test_team_report_2(make_csv, team_report):
    make_csv(
        u'user id,user name,team name\n'
    )
    eval_data_dict, team_data_dict, grades = team_report(TEST_SUBCHAPTER, TEST_COURSE_NAME)


# Check that a one-person team doesn't produce errors.
def test_team_report_3(make_csv, team_report):
    make_csv(
        u'user id,user name,team name\n'
        'user_id1,user_name1,team_name1\n'
    )
    eval_data_dict, team_data_dict, grades = team_report(TEST_SUBCHAPTER, TEST_COURSE_NAME)
    assert eval_data_dict['user_id1'].name == 'user_name1'
    assert eval_data_dict['user_id1'].teammate_netids == []
    assert team_data_dict['team_name1'].team_netids == ['user_id1']
