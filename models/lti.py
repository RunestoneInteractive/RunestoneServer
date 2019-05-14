db.define_table('lti_keys', 
                Field('consumer'), 
                Field('secret'), 
                Field('application'),
                migrate = 'runestone_lti_keys.table'
                )


# insert the initial lti_keys; get the values from 1.py
# if db(db.lti_keys.id > 0).isempty():
#     db.lti_keys.insert(consumer=settings.lti_consumer, secret=settings.lti_secret, application='runestone') # should be id 1
