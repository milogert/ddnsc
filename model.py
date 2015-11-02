import sqlalchemy

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Record(Base):
  """Class for keeping track of DNS names."""
  __tablename__ = "Record"

  id = Column(Integer, primary_key=True)

  # Domain name stuff.
  subdomain = Column(String(255))
  domain = Column(String(255), nullable=False)

  # Username/password.
  username = Column(String(32), nullable=False)
  password = Column(String(32), nullable=False)

  ip = Column(String(15))

  # Provider and api things.
  provider = Column(String(255), nullable=False)
  api = Column(String(1024))
  extras = Column(String(1024))

  response = Column(String(1024))


# Lets create the database.
engine = create_engine("sqlite:///ddnsc.db")
Base.metadata.create_all(engine)

