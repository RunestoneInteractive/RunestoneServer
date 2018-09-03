import click

res = db.executesql("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public' AND table_type='BASE TABLE'""")

click.echo("The following tables are defined")
for row in res:
    click.echo(row[0])
