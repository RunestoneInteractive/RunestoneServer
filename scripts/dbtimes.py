from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

engine = create_engine(
    #    "postgresql://runestone:al3xandria@localhost/logtimes",
    # echo=True
    "postgresql://bmiller:autocubanlobbyduck@localhost/bmiller",
    echo=True,
)
meta = MetaData()
Session = sessionmaker(bind=engine)


class LogEntry(Base):
    __tablename__ = "api_times"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Date)
    endpoint = Column(String)
    calls = Column(Integer)
    response_average = Column(Float)
    max_response = Column(Integer)


Base.metadata.create_all(engine)
# meta.create_all(engine)
db = Session()

e = LogEntry(
    timestamp=datetime.datetime.now().date(),
    endpoint="foo",
    calls=10,
    response_average=1.55,
    max_response=10,
)

db.add(e)

db.commit()
