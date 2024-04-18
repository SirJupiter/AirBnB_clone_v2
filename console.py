#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    the_classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in self.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        # if not args:
        #     print("** class name missing **")
        #     return
        # elif args not in HBNBCommand.the_classes:
        #     print("** class doesn't exist **")
        #     return
        # if not self.checker(args, ["n", 'ec']):
        #     return
        # cls, var, val = self.parse_command(args)
        # new_instance = HBNBCommand.the_classes[cls](**{var: val})
        # storage.save()
        # print(new_instance.id)
        # storage.save()

        cmd_input = args.split(' ')

        if not cmd_input[0]:
            print("** class name missing **")
            return

        class_name = cmd_input[0]
        if class_name in self.the_classes:
            o_dict = {}
            for element in cmd_input[1:]:
                key, value = element.split('=')
                key = key.strip()
                value = value.strip('"')

                if '_' in value:
                    value = value.replace('_', ' ')
                o_dict[key] = value
            created_obj = self.the_classes[class_name](**o_dict)
            print(created_obj.id)
            created_obj.save()
        else:
            print("** class does not exist **")

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method shows a desired object """
        new = args.partition(" ")
        parsed_name = new[0]
        parsed_id = new[2]

        # guard against trailing args
        if parsed_id and ' ' in parsed_id:
            parsed_id = parsed_id.partition(' ')[0]

        if not parsed_name:
            print("** class name missing **")
            return

        if parsed_name not in self.the_classes:
            print("** class doesn't exist **")
            return

        if not parsed_id:
            print("** instance id missing **")
            return

        key = parsed_name + "." + parsed_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        parsed_name = new[0]
        parsed_id = new[2]
        if parsed_id and ' ' in parsed_id:
            parsed_id = parsed_id.partition(' ')[0]

        if not parsed_name:
            print("** class name missing **")
            return

        if parsed_name not in HBNBCommand.the_classes:
            print("** class doesn't exist **")
            return

        if not parsed_id:
            print("** instance id missing **")
            return

        key = parsed_name + "." + parsed_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in self.the_classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all(self.the_classes[args]).items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        parsed_name = parsed_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            parsed_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if parsed_name not in HBNBCommand.the_classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            parsed_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = parsed_name + "." + parsed_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] != '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in self.types:
                    att_val = self.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    # @staticmethod
    # def parse_command(line):
    #     """parse the command entered by the user"""

    #     parts = line.split('.')
    #     equal_parts = line.split()
    #     if len(parts) == 2 and parts[1].endswith(')'):
    #         cls = parts[0]
    #         parts = parts[1].split("(")
    #         if len(parts) == 2:
    #             method = parts[0]
    #             parts = parts[1].rstrip(")")
    #             if not parts:
    #                 return cls, method
    #             if "{" not in parts:
    #                 args = [literal_eval(
    # i.strip()) for i in parts.split(",")]
    #             else:
    #                 args = [literal_eval(
    # i.strip()) for i in parts.split(",", 1)]
    #             return cls, method, args
    #         return cls, parts[0]
    #     if len(equal_parts) == 2:
    #         var, val = equal_parts[1].split("=")
    #         return equal_parts[0]. var, val
    #     else:
    #         return None

    # @staticmethod
    # def checker(model, keys):
    #     """checks if the model string contains any of the specified keys"""

    #     part = model.split()
    #     if "n" in keys and not model:
    #         print("** class name missing **")
    #         return False
    #     if "l" in keys and len(model.split()) < 2:
    #         print("** instance id missing **")
    #         return False
    #     if "ec" in keys and part[0] not in HBNBCommand.the_classes:
    #         print("** class doesn't exist **")
    #         return False
    #     if "es" in keys and ".".join(part[0:2]) not in storage.all():
    #         print("** no instance found **")
    #         return False
    #     if "a" in keys and len(model.split()) < 3:
    #         print("** attribute name missing **")
    #         return
    #     if "v" in keys and len(model.split()) < 4:
    #         print("** value missing **")
    #         return
    #     return True

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
