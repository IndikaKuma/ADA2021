import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL is provided as an env. variable
if "DB_URL" is os.environ:
    db_url = os.environ['DB_URL']
else:
    db_url = 'sqlite:///place.db'

engine = create_engine(db_url)
# https://docs.sqlalchemy.org/en/13/orm/session.html
Session = sessionmaker(bind=engine)
# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html
Base = declarative_base()
