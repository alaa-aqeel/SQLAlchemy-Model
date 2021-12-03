# SQLAlchemy Model+Validate 


#### create app  
```py
from database import SQLAlchemy, model


db = SQLAlchemy(
    url="sqlite:///./sqlite.db",
    connect_args={
        "check_same_thread": False
    }
) # or db.init_app()
```

## Model 

```py
class TestModel(db.Model):

    name = model.Column(model.types.String, unique=True)

# migrate tables 
db.create_all()
print(db.tables) # return list tables name
```

## Create, Delete & Update 
```py
# create 
test = TestModel.create(name="test name")
print(test) # <TestModel (id=1)>

# update 
test.update(name="test new name")
print(test.name) # test new name

# delete 
test.delete()
```

## Query 
```py 
# find by id 
TestModel.find(1)

# finde by field 
TestModel.find_by(name="tets new name").first()
```

## Custom fetch errors 
```py 
def handler_errors(error, *args, **kw):

    raise ValueError(str(error)) 

db.Model.handler_errors = handler_errors
```

## With validate 
```py 
from database.validation import Validate, required

valid = Validate(
    { # rules 
        "name": [required]
    },
    { # values 
        "name": "test name 01"
    }
)

valid.is_valid()

pritn( valid.errors ) 

# output 
"""
{
    fieldname:[
        rules_message
    ]
}
"""
```


## With validate and model 
```py 
from database.validation import Validate, required

valid_model = Validate(
    { # rules 
        "name": [required]
    },
    { # values 
        "name": "test name 01"
    },
    TestModel # model 
)


# create with valid 
valid_model.create() # raise errors 

# update 
valid_model.update() # raise errors 
```

## creae rule 
```py 

# Required rule 
def required(field, value):
    if not len(value.strip()):
        return f"Field {field} is required"

valid_model = Validate(
    { # rules 
        "field": [required]
    },
    { # values },
)
```