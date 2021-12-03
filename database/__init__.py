from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from database.model import BaseModel
class SQLAlchemy:

    def __init__(self, **kw):

        if kw:
            self.init__app(**kw)

    def init__app(self, **kw):

        self.engine = create_engine(**kw)
        self.session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        ))

        BaseModel.session = self.session()

        self.__model = declarative_base(name="Model", bind=self.engine, cls=BaseModel)


    def create_all(self):

        self.__model.metadata.create_all(bind=self.engine)

    def drop_all(self):

        self.__model.metadata.drop_all(bind=self.engine)

    @property
    def tables(self):
        return self.engine.table_names()

    @property
    def Model(self):
        return self.__model