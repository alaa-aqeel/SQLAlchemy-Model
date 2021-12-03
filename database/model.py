from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, types
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import clear_mappers


def raise_errors(errors, *args, **kw):

    raise str(errors)

class CustomProperty(property):

    def __get__(self, cls):
        return self.fget(cls)


class BaseModel:

    session = None

    handler_errors = raise_errors

    id = Column(types.BigInteger, primary_key=True, index=True, autoincrement=True)
    

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @CustomProperty
    def query(cls):
        return cls.session.query(cls)

    @classmethod
    def find(cls, id) -> object:
        obj = cls.query.get(id)
        if not obj:
            cls.handler_errors(f"Not found {cls.__name__} {id}", "find", id)

        return obj
    
    @classmethod
    def filter(cls, **kw):
        return cls.query.filter(**kw)

    @classmethod
    def create(cls, **kw):
        try:
            obj = cls(**kw)
            cls.session.add(obj)
            cls.session.commit()
        except SQLAlchemyError as err :
            cls.session.rollback()
            cls.handler_errors(err.__dict__.get("orig", "Opps errors"), 'create', **kw)


    def save(self):
        try:
            self.session.add(self)
            self.session.commit()
        except SQLAlchemyError as err :
            self.session.rollback()
            self.handler_errors(err.__dict__.get("orig", "Opps errors"), "save")


    def update(self, **kw):
        try:
            obj = self.filter(id=self.id)
            self.update(kw)
            return obj.first()
        except SQLAlchemyError as err :
            self.session.rollback()
            self.handler_errors(err.__dict__.get("orig", "Opps errors"), "update",  **kw)

    def delete(self, id):
        try:
            self.session.delete(self)
            self.session.commit()
            return True
        except SQLAlchemyError as err:
            self.session.rollback()
            self.handler_errors(err.__dict__.get("orig", "Opps errors"), "delete", id)


    def __repr__(self) -> str:
        return f"<{self.__name__} (id={self.id})>"



