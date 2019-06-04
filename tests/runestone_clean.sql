--- ************************************************
--- |docname|: Remove data that web2py can re-create
--- ************************************************
-- Any table in ``models/`` whose ``migrate`` parameter includes ``table_migrate_prefix`` will be re-created by web2py.

drop table if exists
    acerror_log,
    coach_hints,
    cohort_plan_responses, cohort_plan_revisions, cohort_plan,
    course_practice,
    deadlines,
    lp_answers,
    lti_keys,
    payments,
    pipactex_deadline,
    problems,
    question_tags,
    user_topic_practice_log, user_topic_practice,
    section_users,
    scheduler_run, scheduler_task, scheduler_task_deps, scheduler_worker,
    tags,
    sub_chapter_taught,
    timed_exam,
    user_biography, user_comments, user_state,
    "user_topic_practice_Completion", user_topic_practice_feedback, user_topic_practice_survey,
    web2py_session_runestone;
