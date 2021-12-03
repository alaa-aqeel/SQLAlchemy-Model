from database import SQLAlchemy, model
from database.validation import Validate, required



db = SQLAlchemy(
    url="sqlite:///./sqlite.db",
    connect_args={
        "check_same_thread": False
    }
)

def handler_errors(error, method, **kw):

    raise ValueError(str(error)) 

db.Model.handler_errors = handler_errors

class TestModel(db.Model):

    name = model.Column(model.types.String, unique=True)


db.create_all()

model_valid = Validate(
    {
        "name": [required]
    },
    {
        "name": ""
    }, 
    TestModel
)

test = model.create()
print(test)
