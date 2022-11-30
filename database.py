from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql+pymysql://root:9RKksx6jxJ[E/EDH@34.128.91.205/gatesystem")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine)
