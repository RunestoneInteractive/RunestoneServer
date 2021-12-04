import click
import datetime
from dateutil.parser import parse
import os.path
import re

res = db.executesql(
    """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public' AND table_type='BASE TABLE'"""
)
