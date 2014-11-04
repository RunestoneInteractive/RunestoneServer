import string
import random
import pprint
import json
import collections
import datetime

def schedule():
    if auth.user == None:
        redirect(URL('default', 'user/login'))
    else:
        dbfile = open('schedule_debug.log', 'a')
        if auth.user.cohort_id == None:
            session.flash = 'You must be a member of a team to schedule'
            redirect(URL('mygroup','manageGroup'))
        dbfile.write('%s : user = %s cohort_id = %d\n' % (datetime.datetime.now(), auth.user.username, auth.user.cohort_id))
        allProgress = db((db.user_sub_chapter_progress.chapter_id == db.chapters.chapter_label) &
                         (db.auth_user.course_name == auth.user.course_name) &
                         (db.chapters.course_id == auth.user.course_name) &
                         (db.user_sub_chapter_progress.user_id == db.auth_user.id) &
                         (db.auth_user.cohort_id == auth.user.cohort_id)).select(db.user_sub_chapter_progress.ALL,
                                                                                db.chapters.ALL,
                                                                                db.auth_user.ALL)

        allUsers = db(db.auth_user.cohort_id == auth.user.cohort_id).select(db.auth_user.ALL)

        allComments = db(db.user_comments.cohort_id == auth.user.cohort_id).select(orderby=~db.user_comments.id|db.user_comments.ALL)

        allPlans = db((db.cohort_plan.chapter_id == db.chapters.id) &
                      (db.cohort_plan.cohort_id == auth.user.cohort_id)).select(db.chapters.id,
                                                                                db.chapters.chapter_label,
                                                                                db.chapters.chapter_name,
                                                                                db.cohort_plan.status ,
                                                                                db.cohort_plan.start_date ,
                                                                                db.cohort_plan.end_date,
                                                                                db.cohort_plan.actual_end_date,
                                                                                db.cohort_plan.note,
                                                                                db.cohort_plan.created_by,
                                                                                db.cohort_plan.cohort_id,
                                                                                db.cohort_plan.id)
        dbfile.write('%s : %s\n' % (datetime.datetime.now(), 'before for plan'))
        for plan in allPlans:
            if plan.cohort_plan.status=='new' and plan.cohort_plan.start_date < datetime.datetime.now().date():
                plan.cohort_plan.status='active'
                db((db.cohort_plan.chapter_id==plan.chapters.id) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(status='active')
            for user in allUsers:
                count=0
                total=0
                dbfile.write('%s : %s\n' % (datetime.datetime.now(), 'before for allProgress'))
                for progress in allProgress:
                    if int(progress.user_sub_chapter_progress.user_id)==user.id and progress.chapters.id==plan.chapters.id: 
                        if progress.user_sub_chapter_progress.status > 0:
                            count += 1
                        total += 1
                if total > 0:
                    result = round(count*100/total)
                    db((db.user_chapter_progress.user_id==user.id) & (db.user_chapter_progress.chapter_id==plan.chapters.id)).update(status=result)

            userProgress = db(db.user_chapter_progress.chapter_id==plan.chapters.id).select(db.user_chapter_progress.status)
            completed = True
            dbfile.write('%s : %s\n' % (datetime.datetime.now(), 'before for userProgress'))
            for progress in userProgress:
                if progress.status<100:
                    completed=False

        cohortName = db(db.cohort_master.id == auth.user.cohort_id).select(db.cohort_master.cohort_name)

        dbfile.write('%s : %s\n' % (datetime.datetime.now(), 'done'))
        dbfile.close()
        return dict(allPlans=allPlans, allProgress=allProgress, allUsers=allUsers,
                    allComments=allComments, cohortName=cohortName)


def newschedule():
    if auth.user == None:
        redirect(URL('default', 'user/login'))
    else:
        chapters = db((db.chapters.id==db.cohort_plan.chapter_id) &
                      (db.cohort_plan.cohort_id == auth.user.cohort_id)).select(db.chapters.id, db.chapters.chapter_name, db.cohort_plan.status, db.cohort_plan.cohort_id)
        return dict(chapters=chapters)


def modifiedschedule():
    if auth.user == None:
        redirect(URL('default', 'user/login'))
    else:
        chapters = db(db.chapters.id==db.cohort_plan.chapter_id).select(db.chapters.id, db.chapters.chapter_name, db.cohort_plan.status,db.cohort_plan.start_date , db.cohort_plan.end_date)
        return dict(chapters=chapters)


def modify():
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(status='new')
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(start_date=request.vars.startDate)
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(end_date=request.vars.endDate)
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(note=request.vars.note)
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(created_by=auth.user)
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(created_on=datetime.datetime.now())
    plan = db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).select(db.cohort_plan.ALL).first()
    plan_fields = db.cohort_plan._filter_fields(plan)
    plan_fields['plan_id'] = plan.id
    db.cohort_plan_revisions.insert(**plan_fields)


def delete():
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(status='notStarted')
    plan = db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).select(db.cohort_plan.ALL).first()
    db.cohort_plan_revisions.insert(**db.cohort_plan._filter_fields(plan))
    db((db.cohort_plan_revisions.chapter_id==request.vars.chapter) & (db.cohort_plan_revisions.cohort_id==auth.user.cohort_id)).update(plan_id=plan.id)
    db((db.user_comments.cohort_id==auth.user.cohort_id) & (db.user_comments.chapter_id==request.vars.chapter)).delete()

def complete():
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(status='completed', actual_end_date=datetime.datetime.now())
    db((db.cohort_plan.chapter_id==request.vars.chapter) & (db.cohort_plan.cohort_id==auth.user.cohort_id)).update(actual_end_date=datetime.datetime.now())

def comment():
	db.user_comments.insert(cohort_id=auth.user.cohort_id,chapter_id=request.vars.chapter,comment=request.vars.text,comment_by=auth.user)


def initiateGroup():
    #if pprint.pprint(auth.user)
    if auth.user == None:
        redirect(URL('default', 'user/login'))
    elif db(db.chapters.course_id == auth.user.course_name).count() < 1:
        session.flash = 'Your course does not appear to support Study Groups'
        redirect(URL('default', 'user/login'))
    else:
        return dict(requestArgs=request.args(0))

def manageGroup():
    if auth.user == None:
        redirect(URL('default', 'user/login'))
    elif not auth.user.cohort_id:
        session.flash = 'You do not appear to belong to a study group yet'
        redirect(URL('mygroup', 'initiateGroup'))
    else:
        currentGroup = db(db.cohort_master.id == auth.user.cohort_id).select(db.cohort_master.id, db.cohort_master.cohort_name,
                                                                     db.cohort_master.invitation_id,
                                                                     db.cohort_master.is_active)
        allGroupMembers = db(db.auth_user.cohort_id == auth.user.cohort_id).select(db.auth_user.first_name, db.auth_user.last_name)
        return dict(currentGroup=currentGroup[0], allGroupMembers=allGroupMembers)

def createNewGroup():
    if auth.user == None:
        redirect(URL('default', 'user/login'))
    invitationId = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(5)])
    newGroupId = db.cohort_master.insert(cohort_name = request.vars.groupName, created_on=datetime.datetime.now(), is_active=1, invitation_id=invitationId, course_name=auth.user.course_name)
    db.executesql("INSERT INTO cohort_plan(cohort_id, chapter_id, status) SELECT "+str(newGroupId)+", id, 'notStarted' FROM chapters WHERE course_id = '"+auth.user.course_name+"';")    
    auth.user.cohort_id = newGroupId
    joinGroupParameterized(invitationId)
    return invitationId


def joinGroup():
    invitationId = request.vars.invitationId
    currentGroup = db(db.cohort_master.invitation_id==invitationId).select(db.cohort_master.id, db.cohort_master.cohort_name, db.cohort_master.is_active)
    db(db.auth_user.id==auth.user.id).update(cohort_id=currentGroup[0].id)
    auth.user.cohort_id = currentGroup[0].id
    res = {'joinStatus':1, 'groupName':currentGroup[0].cohort_name}
    return json.dumps(res)

def joinGroupParameterized(invitationId):
    currentGroup = db(db.cohort_master.invitation_id==invitationId).select(db.cohort_master.id, db.cohort_master.cohort_name, db.cohort_master.is_active)
    db(db.auth_user.id==auth.user.id).update(cohort_id=currentGroup[0].id)
    res = {'joinStatus':1, 'groupName':currentGroup[0].cohort_name}
    return json.dumps(res)

def lookupGroup():
    invitationId = request.vars.invitationId
    currentGroup = db(db.cohort_master.invitation_id==invitationId).select(db.cohort_master.id, db.cohort_master.cohort_name, db.cohort_master.is_active)
    if len(currentGroup) == 0:
        res = {'joinStatus':0}
    elif len(currentGroup) != 0 and currentGroup[0].is_active != 1:
        res = {'joinStatus':-1, 'groupName':currentGroup[0].cohort_name}
    else:
        allGroupMembers = db(db.auth_user.cohort_id==currentGroup[0].id).select(db.auth_user.first_name, db.auth_user.last_name)
        res = {'joinStatus':-1, 'groupName':currentGroup[0].cohort_name}
        allMembersArray = []
        for member in allGroupMembers:
            d = collections.OrderedDict()
            d['first_name'] = member.first_name
            d['last_name'] = member.last_name
            allMembersArray.append(d)
        res['members'] = json.dumps(allMembersArray)
    return json.dumps(res)

def leaveGroup():
    db(db.auth_user.id==auth.user.id).update(cohort_id='')
    auth.user.cohort_id = ""
    return 'success'
