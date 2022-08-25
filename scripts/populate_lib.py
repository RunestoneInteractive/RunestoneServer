import os
import pathlib
from sqlalchemy import create_engine
import importlib
import pdb
import sys
import re

# This is a one-off script to populate the new library table.  Once that is populated
# this can be removed from the repo - or kept for posterity.

sys.path.insert(0, ".")
if os.environ["HOME"] == "/root":
    cwd = pathlib.Path("/srv/web2py/applications/runestone/books")
else:
    cwd = pathlib.Path(os.environ.get("HOME"), "Runestone", "books")


def _find_real_url(libdir, book):
    idx = pathlib.Path(libdir, book, "published", book, "index.html")
    if idx.exists():
        with open(idx, "r") as idxf:
            for line in idxf:
                if g := re.search(r"refresh.*URL='(.*?)'", line):
                    return g.group(1)
    return "index.html"


print("CWD = ", cwd)


def update_library(book):
    """
    Parameters:
    config : This originated as a config object from click -- a mock config will be provided by the AuthorServer
    mpath: Path to the runestone-manifest file which containes the library metadata
    course: the name of the course we are building

    Update the library table using meta data from the book

    Returns: Nothing
    """
    eng = create_engine(os.environ["DEV_DBURL"])
    print(f"BOOK = {book}")

    try:
        config = importlib.import_module(f"{book}.conf")
    except Exception as e:
        print(f"Error adding book {book} to library list: {e}")
        return

    book_info = {}
    book_info.update(description="")
    book_info.update(key_words="")
    book_info.update(basecourse=book)
    book_info.update(is_visible="T")
    book_info.update(subtitle="")
    if hasattr(config, "navbar_title"):
        book_info["title"] = config.navbar_title
    elif hasattr(config, "html_title"):
        book_info["title"] = config.html_title
    elif hasattr(config, "html_short_title"):
        book_info["title"] = config.html_short_title
    else:
        book_info["title"] = "Runestone Book"
    # update course description if found in the book's conf.py
    if hasattr(config, "course_description"):
        book_info.update(description=config.course_description)
    # update course key_words if found in book's conf.py
    if hasattr(config, "key_words"):
        book_info.update(key_words=config.key_words)
    if hasattr(config, "publisher") and config.publisher == "PTX":
        bks = "/ns"
        book_info["build_system"] = "PTX"
    else:
        bks = "/ns"
        book_info["build_system"] = "Runestone"

    if hasattr(config, "shelf_section"):
        book_info["shelf_section"] = config.shelf_section
    else:
        book_info["shelf_section"] = "Computer Science"

    book_info["main_page"] = _find_real_url(cwd, book)

    res = eng.execute(f"select * from library where basecourse = '{book}'")

    if res.rowcount == 0:
        eng.execute(
            """insert into library 
        (title, subtitle, description, shelf_section, basecourse, is_visible, main_page ) 
        values('{title}', '{subtitle}', '{description}', '{shelf_section}', 
        '{basecourse}', '{is_visible}', '{main_page}') """.format(
                **book_info
            )
        )
    else:
        eng.execute(
            """update library set
            title = '{title}',
            subtitle = '{subtitle}',
            description = '{description}',
            shelf_section = '{shelf_section}',
            main_page = '{main_page}'
        where basecourse = '{basecourse}'
        """.format(
                **book_info
            )
        )
    return True


os.chdir(cwd)
for path in cwd.iterdir():
    if path.is_dir():
        update_library(path.name)
