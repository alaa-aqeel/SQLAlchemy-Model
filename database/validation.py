

required = lambda field, value: f"Field {field} is required" if not len(value.strip()) else None

class Validate:

    __rules = {}
    __values = {}
    __errors = {}

    def __init__(self, rules:dict, values:dict, model: object =None) -> None:
        self.__rules = rules 
        self.__values = values
        self.__model = model


    def __get_value(self, field):
        if isinstance(self.__values, dict):
            return self.__values.get(field)
        return getattr(self.__values, field) 

    def values_to_dict(self):
        if isinstance(self.__values, dict):
            return self.__values
        return self.__values.dict()


    def is_valid(self):

        for field, rules in self.__rules.items():

            errors = []
            for rule in rules:

                err = rule(field, self.__get_value(field))
                if err:
                    errors.append(err)

            if len(errors):
                self.__errors.update({field: errors})


    def create(self):

        if not self.__model: 
            raise Exception("pass model to save")
        self.is_valid()

        if not self.__errors:
            self.__model.create(**self.values_to_dict())
            return self.__model

        raise Exception(self.__errors)

    
    def update(self):

        if not self.__model: 
            raise Exception("pass model to save")
            
        self.is_valid()
        if not self.__errors:
            self.__model.update(**self.values_to_dict())
            return self.__model

        raise Exception(self.__errors)
            

    @property
    def errors(self):
        self.__errors


