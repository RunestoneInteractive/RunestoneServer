db.define_table('lti_keys', 
                Field('consumer'), 
                Field('secret'), 
                Field('application'),
                migrate = False
                )