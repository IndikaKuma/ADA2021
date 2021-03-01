import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Saving model in a given location (provided as an env. variable
if "DB_URL" is os.environ:
    db_url = os.environ['DB_URL']
else:
    db_url = 'sqlite:///delivery.db'

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()
