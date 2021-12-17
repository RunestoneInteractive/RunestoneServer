# textbooks
# ===============
db.define_table(
    "textbooks",
    Field(
        "path", type="string", notnull=True
    ),  # combination of runestone_account and regname, useful as unique identifier
    Field("github_account", type="string", notnull=True),
    Field("runestone_account", type="string", notnull=True),
    Field("github_repo_name", type="string", notnull=True),
    Field("regname", type="string", notnull=True),
    Field(
        "base_book", type="string", notnull=True
    ),  # regname of the original book that this copy was created from
    Field(
        "webhook_code", type="string", notnull=True
    ),  # randomly generated on book creation, used for verifying authenticity of recieved webhook data
    Field("published", type="boolean"),
    Field("draft_commit", type="string"),  # github commit id for the draft book
    Field("published_commit", type="string"),  # github commit id for the published book
    Field(
        "drafts_directory", type="string"
    ),  # directory created by runestone build + runestone deploy (for the draft book)
    Field(
        "published_directory", type="string"
    ),  # directory created by runestone build + runestone deploy (for the published book)
    migrate=table_migrate_prefix + "textbooks.table",
)
