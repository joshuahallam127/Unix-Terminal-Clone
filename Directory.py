import Inheritance
import User
import File


class Directory(Inheritance.Inheritance):

    def __init__(self, owner: User.User, ancestors: list, name: str, parent, contents: list, is_root: bool):
        super(Directory, self).__init__(owner, ancestors, name, parent, True)
        self.contents = contents
        self.is_root = is_root
        self.perms = 'drwxr-x'
