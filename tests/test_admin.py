

def test_add_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(div_id='subc_b_fitb',points=10)
    print(my_ass.questions())
    db = runestone_db_tools.db
    my_ass.save_assignment()
    res = db(db.assignments.name == 'test_assignment').select().first()
    assert res.description == my_ass.description
    assert str(res.duedate.date()) == str(my_ass.due.date())
    my_ass.autograde()
    my_ass.calculate_totals()
