#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """Represents the BaseModel"""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""
        dateform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.updated_at = self.created_at = datetime.today()
        if len(kwargs) != 0:
            for i, j in kwargs.items():
                if i == "created_at" or i == "updated_at":
                    self.__dict__[i] = datetime.strptime(j, dateform)
                else:
                    self.__dict__[i] = j
        else:
            models.storage.new(self)

    def to_dict(self):
        """Return the dictionary of the BaseModel instance"""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict["created_at"] = self.created_at.isoformat()
        return my_dict

    def save(self):
        """Update updated_at with new datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def __str__(self):
        """Return the str represent of the BaseModel instance."""
        classname = self.__class__.__name__
        return "[{}] ({}) {}".format(classname, self.id, self.__dict__)
