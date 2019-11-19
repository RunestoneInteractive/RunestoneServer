import datetime
from random import shuffle


# Get practice data for this student and create flashcards for them is they are newcomers.
def _get_practice_data(user, timezoneoffset, db):
    practice_message1 = ""
    practice_message2 = ""
    practice_completion_count = 0
    remaining_days = 0
    max_days = 0
    max_questions = 0
    day_points = 0
    question_points = 0
    presentable_flashcards = []
    available_flashcards_num = 0
    practiced_today_count = 0
    practice_today_left = 0
    points_received = 0
    total_possible_points = 0
    flashcard_creation_method = 0
    questions_to_complete_day = 0
    practice_graded = 1
    spacing = 0
    interleaving = 0

    now = datetime.datetime.utcnow()
    now_local = now - datetime.timedelta(hours=timezoneoffset)

    # Since each authenticated user has only one active course, we retrieve the course this way.
    course = db(db.courses.id == user.course_id).select().first()

    practice_settings = db(db.course_practice.course_name == user.course_name)
    if (
        practice_settings.isempty()
        or practice_settings.select().first().end_date is None
    ):
        practice_message1 = "Practice tool is not set up for this course yet."
        practice_message2 = "Please ask your instructor to set it up."
    else:
        practice_settings = practice_settings.select().first()
        practice_start_date = practice_settings.start_date
        flashcard_creation_method = practice_settings.flashcard_creation_method
        # Calculates the remaining days to the end of the semester.
        remaining_days = (practice_settings.end_date - now_local.date()).days
        max_days = practice_settings.max_practice_days
        max_questions = practice_settings.max_practice_questions
        day_points = practice_settings.day_points
        question_points = practice_settings.question_points
        # Define how many questions you expect your students practice every day.
        questions_to_complete_day = practice_settings.questions_to_complete_day
        practice_graded = practice_settings.graded
        spacing = practice_settings.spacing
        interleaving = practice_settings.interleaving

        if practice_start_date > now_local.date():
            days_to_start = (practice_start_date - now_local.date()).days
            practice_message1 = (
                "Practice period will start in this course on "
                + str(practice_start_date)
                + "."
            )
            practice_message2 = (
                "Please return in "
                + str(days_to_start)
                + " day"
                + ("." if days_to_start == 1 else "s.")
            )
        else:
            # Check whether flashcards are created for this user in the current course.
            flashcards = db(
                (db.user_topic_practice.course_name == user.course_name)
                & (db.user_topic_practice.user_id == user.id)
            )
            if flashcards.isempty():
                if flashcard_creation_method == 0:
                    practice_message1 = (
                        "Only pages that you mark as complete, at the bottom of the page, are the"
                        + " ones that are eligible for practice."
                    )
                    practice_message2 = (
                        "You've not marked any pages as complete yet. Please mark some pages first"
                        + " to practice them."
                    )
                else:
                    # new student; create flashcards
                    # We only create flashcards for those sections that are marked by the instructor as taught.
                    subchaptersTaught = db(
                        (db.sub_chapter_taught.course_name == user.course_name)
                        & (
                            db.sub_chapter_taught.chapter_label
                            == db.chapters.chapter_label
                        )
                        & (
                            db.sub_chapter_taught.sub_chapter_label
                            == db.sub_chapters.sub_chapter_label
                        )
                        & (db.chapters.course_id == user.course_name)
                        & (db.sub_chapters.chapter_id == db.chapters.id)
                    )
                    if subchaptersTaught.isempty():
                        practice_message1 = (
                            "The practice period is already started, but your instructor has not"
                            + " added topics of your course to practice."
                        )
                        practice_message2 = (
                            "Please ask your instructor to add topics to practice."
                        )
                    else:
                        subchaptersTaught = subchaptersTaught.select(
                            db.chapters.chapter_label,
                            db.chapters.chapter_name,
                            db.sub_chapters.sub_chapter_label,
                            orderby=db.chapters.id | db.sub_chapters.id,
                        )
                        for subchapterTaught in subchaptersTaught:
                            # We only retrieve questions to be used in flashcards if they are marked for practice
                            # purpose.
                            questions = _get_qualified_questions(
                                course.base_course,
                                subchapterTaught.chapters.chapter_label,
                                subchapterTaught.sub_chapters.sub_chapter_label,
                            )
                            if len(questions) > 0:
                                # There is at least one qualified question in this subchapter, so insert a flashcard for
                                # the subchapter.
                                db.user_topic_practice.insert(
                                    user_id=user.id,
                                    course_name=user.course_name,
                                    chapter_label=subchapterTaught.chapters.chapter_label,
                                    sub_chapter_label=subchapterTaught.sub_chapters.sub_chapter_label,
                                    question_name=questions[0].name,
                                    # Treat it as if the first eligible question is the last one asked.
                                    i_interval=0,
                                    e_factor=2.5,
                                    q=0,
                                    next_eligible_date=now_local.date(),
                                    # add as if yesterday, so can practice right away
                                    last_presented=now - datetime.timedelta(1),
                                    last_completed=now - datetime.timedelta(1),
                                    creation_time=now,
                                    timezoneoffset=timezoneoffset,
                                )

            # Retrieve all the flashcards created for this user in the current course and order them by their order of
            # creation.
            flashcards = db(
                (db.user_topic_practice.course_name == user.course_name)
                & (db.user_topic_practice.user_id == user.id)
            ).select(orderby=db.user_topic_practice.id)

            # We need the following `for` loop to make sure the number of repetitions for both blocking and interleaving
            # groups are the same.
            for f in flashcards:
                f_logs = db(
                    (db.user_topic_practice_log.course_name == user.course_name)
                    & (db.user_topic_practice_log.user_id == user.id)
                    & (db.user_topic_practice_log.chapter_label == f.chapter_label)
                    & (
                        db.user_topic_practice_log.sub_chapter_label
                        == f.sub_chapter_label
                    )
                ).select(orderby=db.user_topic_practice_log.end_practice)
                f["blocking_eligible_date"] = f.next_eligible_date
                if len(f_logs) > 0:
                    days_to_add = sum([f_log.i_interval for f_log in f_logs[0:-1]])
                    days_to_add -= (
                        f_logs[-1].end_practice - f_logs[0].end_practice
                    ).days
                    if days_to_add > 0:
                        f["blocking_eligible_date"] += datetime.timedelta(
                            days=days_to_add
                        )

            if interleaving == 1:
                # Select only those where enough time has passed since last presentation.
                presentable_flashcards = [
                    f for f in flashcards if now_local.date() >= f.next_eligible_date
                ]
                available_flashcards_num = len(presentable_flashcards)
            else:
                # Select only those that are not mastered yet.
                presentable_flashcards = [
                    f
                    for f in flashcards
                    if (
                        f.q * f.e_factor < 12.5
                        and f.blocking_eligible_date < practice_settings.end_date
                        and (
                            f.q != -1
                            or (f.next_eligible_date - now_local.date()).days != 1
                        )
                    )
                ]
                available_flashcards_num = len(presentable_flashcards)
                if len(presentable_flashcards) > 0:
                    # It's okay to continue with the next chapter if there is no more question in the current chapter
                    # eligible to be asked (not postponed). Note that this is not an implementation of pure
                    # blocking, because a postponed question from the current chapter could be asked tomorrow, after
                    # some questions from the next chapter that are asked today.
                    presentable_chapter = presentable_flashcards[0].chapter_label
                    presentable_flashcards = [
                        f
                        for f in presentable_flashcards
                        if f.chapter_label == presentable_chapter
                    ]
                    shuffle(presentable_flashcards)

            # How many times has this user submitted their practice from the beginning of today (12:00 am) till now?
            practiced_log = db(
                (db.user_topic_practice_log.course_name == user.course_name)
                & (db.user_topic_practice_log.user_id == user.id)
                & (db.user_topic_practice_log.q != 0)
                & (db.user_topic_practice_log.q != -1)
            ).select()
            practiced_today_count = 0
            for pr in practiced_log:
                if pr.end_practice - datetime.timedelta(
                    hours=pr.timezoneoffset
                ) >= datetime.datetime(
                    now_local.year, now_local.month, now_local.day, 0, 0, 0, 0
                ):
                    practiced_today_count += 1

            practice_completion_count = _get_practice_completion(
                user.id, user.course_name, spacing, db
            )

            if practice_graded == 1:
                if spacing == 1:
                    total_possible_points = practice_settings.day_points * max_days
                    points_received = round(day_points * practice_completion_count, 2)
                else:
                    total_possible_points = (
                        practice_settings.question_points * max_questions
                    )
                    points_received = round(
                        question_points * practice_completion_count, 2
                    )

            # Calculate the number of questions left for the student to practice today to get the completion point.
            if spacing == 1:
                practice_today_left = min(
                    available_flashcards_num,
                    max(0, questions_to_complete_day - practiced_today_count),
                )
            else:
                practice_today_left = available_flashcards_num

    return (
        now,
        now_local,
        practice_message1,
        practice_message2,
        practice_graded,
        spacing,
        interleaving,
        practice_completion_count,
        remaining_days,
        max_days,
        max_questions,
        day_points,
        question_points,
        presentable_flashcards,
        available_flashcards_num,
        practiced_today_count,
        questions_to_complete_day,
        practice_today_left,
        points_received,
        total_possible_points,
        flashcard_creation_method,
    )


def _get_practice_completion(user_id, course_name, spacing, db):
    if spacing == 1:
        return db(
            (db.user_topic_practice_Completion.course_name == course_name)
            & (db.user_topic_practice_Completion.user_id == user_id)
        ).count()
    return db(
        (db.user_topic_practice_log.course_name == course_name)
        & (db.user_topic_practice_log.user_id == user_id)
        & (db.user_topic_practice_log.q != 0)
        & (db.user_topic_practice_log.q != -1)
    ).count()
