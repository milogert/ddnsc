from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from config import DOMAIN, PROVIDER, API

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

    def __init__(
            self,
            subdomain,
            username,
            password,
            extras,
            domain=DOMAIN,
            provider=PROVIDER,
            api=API
    ):
        self.subdomain = subdomain
        self.domain = domain
        self.username = username
        self.password = password
        self.provider = provider
        self.api = api
        self.extras = extras


# Lets create the database.
engine = create_engine("sqlite:///rec.db")
Base.metadata.create_all(engine)
