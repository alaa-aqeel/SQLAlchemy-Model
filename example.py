from database import SQLAlchemy, model
from database.validation import Validate, required



db = SQLAlchemy(
    url="sqlite:///./sqlite.db",
    connect_args={
        "check_same_thread": False
    }
)

def handler_errors(error, *args, **kw):

    raise ValueError(str(error)) 

db.Model.handler_errors = handler_errors

class TestModel(db.Model):

    name = model.Column(model.types.String, unique=True)


# db.drop_all()
db.create_all()

# TestModel.create(name="tet name")

# test.update(name="test new name")
# print(TestModel.find(1).name) # test new name

# model_valid = Validate(
#     {
#         "name": [required]
#     },
#     {
#         "name": ""
#     }, 
#     TestModel
# )

# test = model_valid.create()
# print(test)
