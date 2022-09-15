import datetime
import os

from sqlalchemy import (
    Column,
    Table,
    ForeignKey,
    Index,
    Integer,
    String,
    Date,
    DateTime,
    Text,
    create_engine,
    types,
    Float,
    inspect,
    MetaData,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.orm import declarative_base

# Local application imports
# -------------------------
# This creates the base class we will use to create models

Base = declarative_base()

# authors will have a role defined for their user_id in auth_group and auth_membership
engine = create_engine(os.environ["DBURL"])
Session = sessionmaker(expire_on_commit=False)
engine.connect()
Session.configure(bind=engine)
meta = MetaData()


class UserActivity(Base):
    __tablename__ = "user_activity"
    timestamp = Column(DateTime, primary_key=True)
    num_users = Column(Integer)


Base.metadata.create_all(bind=engine)


def create_activity_entry(num_active: int) -> None:
    new_row = UserActivity(num_users=num_active, timestamp=datetime.datetime.utcnow())
    with Session.begin() as session:
        session.add(new_row)


last_five = engine.execute(
    """
    select count(distinct sid) from useinfo where timestamp > now() - interval '5 minutes'
    """
).first()

num_active = last_five[0]

create_activity_entry(num_active)
