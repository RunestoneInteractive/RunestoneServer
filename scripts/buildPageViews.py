#!/usr/bin/env python
# coding: utf-8

# # Create / update a page view table
#
# * Course
# * Base Course
# * chapter
# * subchapter
# * timestamp
# * sid
# * useinfo id
#
# --
# * chapter name?
# * subchapter name?
# * chapter number?
# * subchapter number?
#

# In[104]:


import pandas as pd
from sqlalchemy import create_engine
import datetime
import os

eng = create_engine(os.environ["DBURL"])


# In[105]:


TIMEFRAME = "2022-08-01"
TF = datetime.datetime(2022, 8, 1)
LY = TF - datetime.timedelta(days=365)


# In[106]:


tmp = pd.read_sql_query("select max(timestamp) as last_ts from page_views", eng)


# In[107]:


print(tmp.last_ts[0])


# In[108]:


get_ipython().run_cell_magic(
    "time",
    "",
    "pages = pd.read_sql_query(f\"\"\"select * from useinfo\n   join courses on useinfo.course_id = courses.course_name\n   where useinfo.timestamp > %(last_ts)s\n   and courses.term_start_date >= %(start)s\n   and event = 'page'\n   \"\"\", params={'last_ts': tmp.last_ts[0], 'start': TF},\n   con=eng, parse_dates=['term_start_date','timestamp'])\n",
)


# In[109]:


len(pages)


# In[110]:


def get_chapter(divid):
    parts = divid.split("/")
    if len(parts) >= 2:
        return parts[-2]


def get_subchapter(divid):
    parts = divid.split("/")
    if len(parts) >= 2:
        return parts[-1].replace(".html", "")


# In[111]:


pages["chapter"] = pages.div_id.map(get_chapter)
pages["subchapter"] = pages.div_id.map(get_subchapter)
pages["time_from_start"] = pages.timestamp - pages.term_start_date
pages["week"] = pages.time_from_start.dt.days // 7
pages = pages[pages.week >= 0]


# In[112]:


print(len(pages))


# In[ ]:


# In[113]:


titles = pd.read_sql_query(
    """select * from chapters join sub_chapters on chapters.id = sub_chapters.chapter_id """,
    eng,
)


# The next step needs to be different for PTX books and Runestone books...
# 1. For Runestone books I can deduce the chapter and subchapter from the URL in div_id
# 2. For ptx books I can deduce the sub_chapter id from the URL and would want to merge with the basecourse+subchap

# In[114]:


mp = pages.merge(
    titles,
    left_on=["base_course", "chapter", "subchapter"],
    right_on=["course_id", "chapter_label", "sub_chapter_label"],
)


# In[115]:


mp = mp[
    [
        "timestamp",
        "term_start_date",
        "week",
        "course_name",
        "base_course",
        "chapter",
        "subchapter",
        "courselevel",
        "chapter_name",
        "sub_chapter_name",
    ]
]


# In[116]:


mp.to_sql(
    "page_views", eng, if_exists="append", index=False, method="multi", chunksize=10000
)


# In[117]:


# mp.to_csv("page_views.csv", index=False)


# In[118]:


# mp.sort_values('timestamp')


# ```sql
# create index chapter_id on page_views using btree(chapter);
# create index sub_chapter_id on page_views using btree(subchapter);
# create index base_course_idx on page_views using btree(base_course);
# ```
#
