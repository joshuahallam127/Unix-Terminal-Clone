import Inheritance
import User

class File(Inheritance.Inheritance):
    def __init__(self, owner: User.User, ancestors: list, name: str, parent):
        super(File, self).__init__(owner, ancestors, name, parent, False)
        self.perms = '-rw-r--'
    
    def copy(self):
        return File(self.owner, self.ancestors, self.name, self.parent)
