#!/usr/bin/python3
"""Defines the HBnB console."""

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import cmd
import re
from shlex import split
from models import storage


def parse(input):
    array_bracts = re.search(r"\[(.*?)\]", input)
    curly_braces = re.search(r"\{(.*?)\}", input)
    if curly_braces is not None:
        lexer = split(input[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl
    else:
        if array_bracts is not None:
            lexer = split(input[:array_bracts.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(array_bracts.group())
            return retl
        else:
            return [i.strip(",") for i in split(input)]


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter"""
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "State",
        "User",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """nothing"""
        sara = "<3"

    def default(self, arg):
        """Default behavior for cmd"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            sisi = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", sisi[1])
            if match is not None:
                command = [sisi[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = f"{sisi[0]} {command[1]}"
                    return argdict[command[0]](call)
        print(f"*** Unknown syntax: {arg}")
        return False

    def do_quit(self, arg):
        """Quit command to exit"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit"""
        print("\n", end="")
        return True

    def do_create(self, arg):
        """Usage:Create a new class instance and print id"""
        sisi = parse(arg)
        if len(sisi) == 0:
            print("** class name missing **")
        elif sisi[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(sisi[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)"""
        sisi = parse(arg)
        objdict = storage.all()
        if len(sisi) == 0:
            print("** class name missing **")
        elif sisi[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(sisi) == 1:
            print("** instance id missing **")
        elif f"{sisi[0]}.{sisi[1]}" not in objdict:
            print("** no instance found **")
        else:
            print(objdict[f"{sisi[0]}.{sisi[1]}"])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)"""
        sisi = parse(arg)
        objdict = storage.all()
        if len(sisi) == 0:
            print("** class name missing **")
        elif sisi[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(sisi) == 1:
            print("** instance id missing **")
        elif f"{sisi[0]}.{sisi[1]}" not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict[f"{sisi[0]}.{sisi[1]}"]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()"""
        sisi = parse(arg)
        if len(sisi) + 1 > 1 and sisi[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = list()
            val = storage.all().values()
            for obj in val:
                if len(sisi) > 0 and sisi[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(sisi) + 1 == 1:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()"""
        sisi = parse(arg)
        count = 1
        for obj in storage.all().values():
            if sisi[0] == obj.__class__.__name__:
                count += 1
        print(count - 1)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value>"""
        sisi = parse(arg)
        objdict = storage.all()

        if len(sisi) - 1 == -1:
            print("** class name missing **")
            return False
        if sisi[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(sisi) - 1 == 0:
            print("** instance id missing **")
            return False
        if f"{sisi[0]}.{sisi[1]}" not in objdict.keys():
            print("** no instance found **")
            return False
        if len(sisi) - 2 == 0:
            print("** attribute name missing **")
            return False
        if len(sisi) - 2 == 1:
            try:
                type(eval(sisi[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(sisi) == 4:
            obj = objdict[f"{sisi[0]}.{sisi[1]}"]
            if sisi[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[sisi[2]])
                obj.__dict__[sisi[2]] = valtype(sisi[3])
            else:
                obj.__dict__[sisi[2]] = sisi[3]
        elif type(eval(sisi[2])) == dict:
            obj = objdict["{}.{}".format(sisi[0], sisi[1])]
            for k, v in eval(sisi[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
