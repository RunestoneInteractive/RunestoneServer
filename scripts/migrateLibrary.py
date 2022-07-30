import os
import importlib
from sqlalchemy import create_engine

book_list = os.listdir("books")
book_list = [book for book in book_list if ".git" not in book]
eng = create_engine(os.environ["DEV_DBURL"])

for book in sorted(book_list):
    try:
        # WARNING: This imports from ``applications.<runestone application name>.books.<book name>``. Since ``runestone/books/<book_name>`` lacks an ``__init__.py``, it will be treated as a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_. Therefore, odd things will happen if there are other modules named ``applications.<runestone application name>.books.<book name>`` in the Python path.
        config = importlib.import_module("books.{}.conf".format(book))
    except Exception as e:
        print(f"Error adding book {book} to library list: {e}")
        continue
    book_info = {}
    book_info.update(course_description="")
    book_info.update(key_words="")
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
        book_info.update(course_description=config.course_description)
    # update course key_words if found in book's conf.py
    if hasattr(config, "key_words"):
        book_info.update(key_words=config.key_words)
    if hasattr(config, "publisher") and config.publisher == "PTX":
        bks = "ns"
        book_info["source"] = "PTX"
    else:
        bks = "ns"
        book_info["source"] = "Runestone"

    if hasattr(config, "shelf_section"):
        book_info["section"] = config.shelf_section
    else:
        book_info["section"] = "Computer Science"

    book_info["url"] = "/{}/books/published/{}/index.html".format(bks, book)
    book_info["regname"] = book

    if hasattr(config, "is_private") and config.is_private == True:
        pass
    else:
        title = book_info["title"]
        subtitle = ""
        description = book_info["course_description"]
        shelf = book_info["section"]
        course = book
        res = eng.execute(f"select * from library where basecourse = '{course}'")
        if res.rowcount == 0:
            eng.execute(
                f"""insert into library 
            (title, subtitle, description, shelf_section, basecourse ) 
            values('{title}', '{subtitle}', '{description}', '{shelf}', '{course}') """
            )
        else:
            eng.execute(
                f"""update library set
                title = '{title}',
                subtitle = '{subtitle}',
                description = '{description}',
                shelf_section = '{shelf}'
            where basecourse = '{course}'
            """
            )
