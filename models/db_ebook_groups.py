db.define_table('cohort_plan',
  Field('cohort_id','reference cohort_master'), #The cohort this plan belongs to
  Field('chapter_id','reference chapters'),
  Field('start_date','datetime'),                
  Field('end_date','datetime'),  
  Field('note','string'),                
  Field('actual_end_date','datetime'), #actual date when everyone completed the chapter
  Field('status','string'), #notStarted / new / modified / active / completed
  Field('created_on','datetime'),
  Field('created_by','reference auth_user'),
  Field('is_active','integer', default=1), #0 - deleted / inactive. 1 - active
  migrate='runestone_cohort_plan.table'
)

db.define_table('cohort_plan_revisions',
  Field('plan_id','reference cohort_plan'),
  Field('revision_no','integer'), #Revision no of the modified plan. Calculated by max(revision_no) + 1 where cohort_id and chapter_id are matched.
  Field('cohort_id','reference cohort_master'),
  Field('chapter_id','reference chapters'),
  Field('start_date','datetime'),                
  Field('end_date','datetime'),
  Field('note','string'),                     
  Field('actual_end_date','datetime'), 
  Field('status','string'),
  Field('created_on','datetime', default=request.now),
  Field('created_by','reference auth_user'),
  Field('is_active','integer', default=1),
  migrate='runestone_cohort_plan_revisions.table'
)

db.define_table('cohort_plan_responses',
  Field('plan_id','integer'), #combination of plan and revision define which iteration was this response for
  Field('response','integer'), #-1 - awaitnig response. 0 - rejected. 1 - accepted           
  Field('response_by','reference auth_user'),           
  Field('response_on','datetime', default=request.now),
  migrate='runestone_cohort_plan_responses.table'
)

db.define_table('user_comments',
  Field('cohort_id','reference cohort_master'),
  Field('chapter_id','reference chapters'),
  Field('comment','text'),
  Field('comment_by','reference auth_user'),
  Field('comment_parent','reference user_comments'), #a comment as a reply to an existing comment
  Field('comment_on','datetime', default=request.now),
  migrate='runestone_user_comments.table'
)
