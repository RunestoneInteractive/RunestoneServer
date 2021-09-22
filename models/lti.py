db.define_table(
    "lti_keys",
    Field("consumer"),
    Field("secret"),
    Field("application"),
    migrate=bookserver_owned("lti_keys"),
)

# To generate keys, one choice is to invoke `import secrets; hex(secrets.randbits(256))[2:]`; this creates a `256-bit hexadecimal <https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/>`_ `secret key <https://docs.python.org/3/library/secrets.html>`_.

db.define_table(
    "course_lti_map",
    Field("lti_id", "integer"),
    Field("course_id", "integer"),
    migrate=bookserver_owned("course_lti_map"),
)
