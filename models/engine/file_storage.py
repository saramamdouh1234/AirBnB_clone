#!/usr/bin/python3
"""Defines the FileStorage class"""
import json
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.base_model import BaseModel
from models.user import User
from models.city import City


class FileStorage:
    """Represent an abstracted storage engine"""
    __file_path = "storage.json"
    __objects = {}

    def all(self):
        """Return the dictionary all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Make a new obj"""
        classname = obj.__class__.__name__
        FileStorage.__objects[f"{classname}.{obj.id}"] = obj

    def save(self):
        """Serialize the objects to the JSON file """
        myobjcts = FileStorage.__objects
        jsonobj = {i: myobjcts[i].to_dict() for i in myobjcts.keys()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(jsonobj, file)

    def reload(self):
        """Deserializing the JSON file"""
        try:
            with open(FileStorage.__file_path) as file:
                jsonobj = json.load(file)
                for i in jsonobj.values():
                    cls_name = i["__class__"]
                    del i["__class__"]
                    self.new(eval(cls_name)(**i))
        except FileNotFoundError:
            print("an error")
            return
