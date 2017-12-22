from os import path
import os
import shutil
import sys
import json
import logging
import datetime
from psycopg2 import IntegrityError

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

# def index():
#     if not auth.user:
#         session.flash = "Please Login"
#         return redirect(URL('default', 'index'))
#
#     course = db(db.courses.id == auth.user.course_id).select().first()
#     flashcards = db(db.user_topic_practice.user_id == auth.user.id).select()
#
#     chapters = db(db.chapters.course_id == course.course_name) \
#         .select(db.chapters.id, db.chapters.chapter_label,
#                 orderby=db.chapters.id)
#     subchapters = db((db.chapters.course_id == course.course_name) &
#                    (db.sub_chapters.chapter_id == db.chapters.id)) \
#         .select(db.chapters.id, db.sub_chapters.id, db.sub_chapters.sub_chapter_name, db.sub_chapters.sub_chapter_label,
#                 orderby=db.chapters.id | db.sub_chapters.id)
#
#     return dict(course_id=auth.user.course_name, chapters=chapters, subchapters=subchapters)


def checkanswer():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    flashcards = db(db.user_topic_practice.user_id == auth.user.id).select()

    lastQuestion = None
    if request.vars.QID:
        lastQuestion = db(db.questions.id == int(request.vars.QID)).select().first()

        flashcard = db((db.user_topic_practice.user_id == auth.user.id) &
                       (db.user_topic_practice.sub_chapter_label == lastQuestion.subchapter) &
                       (db.user_topic_practice.question_name == lastQuestion.name)).select().first()
        if 'q' in request.vars:
            q = int(request.vars.q)
        else:
            autograde = 'pct_correct'
            if lastQuestion.autograde is not None:
                autograde = lastQuestion.autograde
            q = round(_autograde_one_q(auth.user.course_name, auth.user.username, lastQuestion.name, 5,
                                 lastQuestion.question_type, None, autograde, 'last_answer', False,
                                 flashcard.last_practice))
        flashcard = _change_e_factor(flashcard, q)
        flashcard = _get_next_i_interval(flashcard, q)

        redirect(URL('index'))


def index():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    flashcards = db(db.user_topic_practice.user_id == auth.user.id).select()

    if len(flashcards) == 0:
        subchapters = db((db.chapters.course_id == course.course_name) &
                       (db.sub_chapters.chapter_id == db.chapters.id)) \
            .select(db.sub_chapters.id, db.sub_chapters.sub_chapter_name, db.sub_chapters.sub_chapter_label,
                    orderby=db.chapters.id | db.sub_chapters.id)

        for subchapter in subchapters:
            questions = db((db.questions.subchapter == subchapter.sub_chapter_label)) \
                .select()
            qIndex = 0
            question = _get_next_qualified_question(questions, qIndex)

            if question:
                db.user_topic_practice.insert(
                    user_id=auth.user.id,
                    sub_chapter_label=subchapter.sub_chapter_label,
                    question_name=question.name,
                    i_interval=0,
                    e_factor=2.5,
                    last_practice=datetime.date.today() - datetime.timedelta(1),
                )

        flashcards = db(db.user_topic_practice.user_id == auth.user.id).select()

    for counter, flashcard in enumerate(flashcards):
        if (datetime.datetime.now() - flashcard.last_practice).days >= flashcard.i_interval:
            questions = db(db.questions.subchapter == flashcard.sub_chapter_label).select()
            if len(questions) != 0:
                qIndex = 0
                while questions[qIndex].name != flashcard.question_name:
                    qIndex += 1
                qIndex += 1
                if qIndex == len(questions):
                    qIndex = 0

                question = _get_next_qualified_question(questions, qIndex)

                if question:
                    # This replacement is to render images
                    question.htmlsrc = bytes(question.htmlsrc).decode('utf8').replace('src="../_static/',
                                                                        'src="../static/' + course[
                                                                            'course_name'] + '/_static/')
                    question.htmlsrc = question.htmlsrc.replace("../_images",
                                                  "/{}/static/{}/_images".format(request.application, course.course_name))

                    autogradable = 1
                    if ((question.autograde is not None) or
                        (question.question_type is not None and question.question_type in ['mchoice', 'parsonsprob', 'fillintheblank', 'clickablearea', 'dragndrop'])):
                        autogradable = 2

                    questioninfo = [question.htmlsrc, question.name, question.id, autogradable]

                    flashcard.question_name = question.name
                    flashcard.last_practice = datetime.datetime.now()
                    flashcard.update_record()

                    return dict(course=course, course_name=auth.user.course_name,
                                course_id=auth.user.course_name, q=questioninfo, questionsExist=1)
    return dict(questionsExist=1)


def _get_next_qualified_question(questions, qIndex):
    iterations = 0
    question = questions[qIndex]
    if not _is_qualified_question(question):
        while not _is_qualified_question(question):
            qIndex += 1
            if qIndex == len(questions):
                qIndex = 0
            question = questions[qIndex]
            iterations += 1
            if iterations == len(questions):
                return False
    return question


def _is_qualified_question(question):
    isQualified = False
    if (question.htmlsrc is not None and question.htmlsrc != "" and
            ((question.question_type is not None and
              question.question_type in ['mchoice', 'parsonsprob', 'fillintheblank', 'clickablearea', 'dragndrop']) or
            ('exercise' in question.subchapter.lower()))):
        isQualified = True
    return isQualified


def _get_next_i_interval(flashcard, q):
    """Get next inter-repetition interval after the n-th repetition"""
    if q < 3:
        flashcard.i_interval = 0
    else:
        last_i_interval = flashcard.i_interval
        if last_i_interval == 0:
            flashcard.i_interval = 1
        elif last_i_interval == 1:
            flashcard.i_interval = 6
        else:
            flashcard.i_interval = math.ceil(last_i_interval * flashcard.e_factor)
    flashcard.update_record()
    return flashcard


def _change_e_factor(flashcard, q):
    if flashcard.e_factor >= 1.3:
        flashcard.e_factor = flashcard.e_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        if flashcard.e_factor < 1.3:
            flashcard.e_factor = 1.3
        flashcard.update_record()
    return flashcard
