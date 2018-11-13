from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME, FLOAT
import datetime

Base = declarative_base()

#baby_model
class Baby(Base):
    __tablename__ = 'baby'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    birthday = Column(VARCHAR(255))
    weight = Column(FLOAT(5, 2))
    height = Column(FLOAT(5, 2))
    create_time = Column(DATETIME, default=datetime.datetime.now())

    def keys(self):
        return [c.name for c in self.__table__.columns]
