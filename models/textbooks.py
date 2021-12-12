# textbooks
# ===============
db.define_table(
    "textbooks",
    Field("path", type="string", notnull=True), # combination of runestone_account and regname, useful as unique identifier
    Field("github_account", type="string", notnull=True),
    Field("runestone_account", type="string", notnull=True),
    Field("github_repo_name", type="string", notnull=True),
    Field("regname", type="string", notnull=True),
    Field("base_book", type="string", notnull=True),
    Field("webhook_code", type="string", notnull=True),
    Field("published", type="boolean"),
    Field("draft_commit", type="string"),
    Field("published_commit",type="string"),
    Field("drafts_directory",type="string"),
    Field("published_directory",type="string"),
    migrate=table_migrate_prefix + "textbooks.table",
)