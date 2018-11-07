from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, DATETIME
from datetime import datetime

Base = declarative_base()

#user_model
class User(Base):
    __tablename__ = 'user'
    user_id = Column(INTEGER, primary_key=True, autoincrement=True)
    openid = Column(INTEGER, unique=True)
    nick_name = Column(VARCHAR(255))
    image_url = Column(VARCHAR(255))
    gender = Column(VARCHAR(255))
    province = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    create_time = Column(DATETIME, default=datetime.now())

    def keys(self):
        return [c.name for c in self.__table__.columns]

