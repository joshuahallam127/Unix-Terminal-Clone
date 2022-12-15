import User

# Inheritance class is the parent class for Directory and File classes.
class Inheritance:
    def __init__(self, owner: User.User, ancestors: list, name: str, parent, isdir: bool):
        self.owner = owner
        self.ancestors = ancestors
        self.name = name
        self.parent = parent
        self.isdir = isdir

    def get_ancestors(self):
        ancestors = []
        is_root = self.is_root
        while not is_root:
            ancestors = [cwd] + ancestors
            cwd = cwd.parent
            is_root = cwd.is_root
        return ancestors
    
    # Gets the path of the file or directory in /first/second/etc format as a string.
    def get_path(self):
        path_names = []
        for ancestor in self.ancestors:
            if ancestor == None:
                continue
            if ancestor.name == None:
                continue
            path_names.append(ancestor.name)
        if self.parent != None:
            if self.parent.name != None:
                path_names.append(self.parent.name)
        if self.name != None:
            path_names.append(self.name)
        if len(path_names) == 0:
            return '/'
        path = '/' + '/'.join(path_names)
        return path
