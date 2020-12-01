import json
import re

class ModelHelper:
    def serialize(self):
        return json.dumps(self.__dict__)

    def fetchFromDictionary(self, dictionary):
        p = re.compile('\.')
        for property, value in vars(self).items():
            if (isinstance(dictionary[property], str)):
                if (dictionary[property].isdigit() and p.match(dictionary[property])):
                    dictionary[property] = float(dictionary[property])
                else:
                    if (dictionary[property].isnumeric()):
                        dictionary[property] = int(dictionary[property])
            setattr(self, property, dictionary[property])
