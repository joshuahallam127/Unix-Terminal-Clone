from Directory import *
from File import *
from User import *

def main():
    # Setting up default directory and user and initialising lists of them etc. 
    root_user = User('root', True)
    root_dir = Directory(root_user, [None], None, None, [], False)
    cu = root_user
    cwd = root_dir
    contents = []
    contents.append(root_dir)
    users = [root_user]

    # Loop that continuously takes user input and then performs correct function.
    while True:
        user_input = input(f'{cu.name}:{cwd.get_path()}$ ')
        input_parts = get_input_parts(user_input) # Splits up user input into certain parts. 
        if not valid_syntax(input_parts): # Checks that input parts are of valid type. 
            continue

        main_command = input_parts[0]
        '''
        For this block of if statements, the "if len(inputs_parts) == x"
        is determining whether a flag has been entered.  This can be done
        as it is already known that the input is of "valid syntax".  E.g.
        for mkdir, if len(input_parts) == 2, then the input parts are known
        to be "mkdir" and the path.  If len(input_parts) == 3, then the 
        input parts are known to be "mkdir", the path, and the flag "-p" 
        (as -p is the only valid flag). 

        Also for this block, most functions return a tuple starting with
        True/False. If False, it means there was an error, and nothing
        should be done. If True, it means there were no errors, and any
        values needed for performing commands outside of the function are
        given as the other valuues in the tuple. This is what the "if results[0]"
        is testing for.
        '''
        if main_command == 'exit':
            exit_program(cu)
        elif main_command == 'pwd':
            pwd(cwd)
        elif main_command == 'cd':
            results = cd(cwd, cu, input_parts[1])
            if results[0]:
                if results[1] == 'root_dir':
                    cwd = root_dir
                else:
                    cwd = results[1]
        elif main_command == 'mkdir':
            if len(input_parts) == 2:
                results = mkdir(cwd, cu, input_parts[1], False)  # Runs mkdir function with no flag.
                if results[0]:
                    contents.append(results[1])  # Adds directory to all contents. 
                    results[1].parent.contents.append(results[1])  # Adds directory to parent conents.
            else:
                results = mkdir(cwd, cu, input_parts[2], True)  # Runs mkdir function with flag.
                if results[0]:
                    contents.append(results[1])  # Adds directory to all contents.
                    contents += results[2]  # Adds all ancestors created to contents.
                    results[1].parent.contents.append(results[1])  # Adds directory to parent contents.
        elif main_command == 'touch':
            results = touch(cwd, cu, input_parts[1]) 
            if results[0]:
                contents.append(results[1])  # Adds file to all contents.
                results[1].parent.contents.append(results[1])  # Adds file to parent contents.
        elif main_command == 'cp':
            results = cp(cwd, cu, input_parts[1], input_parts[2])
            if results[0]:
                contents.append(results[1])  # Adds file to all contents
        elif main_command == 'mv':
            mv(cwd, cu, input_parts[1], input_parts[2])
        elif main_command == 'rm':
            results = rm(cwd, cu, input_parts[1])
            if results[0]:
                contents.remove(results[1])  # Removes file from all contents.
        elif main_command == 'rmdir':
            results = rmdir(cwd, cu, input_parts[1]) 
            if results[0]:
                contents.remove(results[1])  # Removes directory from all contents.
        elif main_command == 'chmod':
            if len(input_parts) == 4:
                chmod(cwd, cu, input_parts[2], input_parts[3], True)  # Runs chmod function with flag
            else:
                chmod(cwd, cu, input_parts[1], input_parts[2], False)  # Runs chmod function without flag
        elif main_command == 'chown':
            user = None
            user_exists = False
            if cu.is_super_user:  # Tests for being root user. 
                if len(input_parts) == 4:
                    for u in users:  # Finds correct User object.
                        if u.name == input_parts[2]:
                            user = u
                            break
                    if user != None:
                        chown(cwd, user, input_parts[3], True)  # Runs chown function with flag
                    else:
                        print('chown: Invalid user')
                else:
                    for u in users:  # Finds correct User object.
                        if u.name == input_parts[1]:
                            user = u
                            break
                    if user != None:
                        chown(cwd, user, input_parts[2], False)  # Runs chown functino without flag
                    else:
                        print('chown: Invalid user')
            else:
                print('chown: Operation not permitted')  # Prints if not root user. 
        elif main_command == 'adduser':
            if cu.is_super_user:
                results = adduser(users, input_parts[1])
                if results[0]:
                    users.append(results[1])  # Adds user to all users. 
            else:
                print('adduser: Operation not permitted')
        elif main_command == 'deluser':
            if cu.is_super_user:
                results = deluser(users, input_parts[1])
                if results[0]:
                    users.remove(results[1])  # Removes user from all users. 
            else:
                print('deluser: Operation not permitted')
        elif main_command == 'su':
            if len(input_parts) == 1:
                cu = root_user
            else:
                results = su(users, input_parts[1])
                if results[0]:
                    cu = results[1]
        elif main_command == 'ls':
            if len(input_parts) == 1:
                ls(cwd, cu)
            elif len(input_parts) == 2:
                ls(cwd, cu, input_parts[1])
            elif len(input_parts) == 3:
                ls(cwd, cu, input_parts[1], input_parts[2])
            elif len(input_parts) == 4:
                ls(cwd, cu, input_parts[1], input_parts[2], input_parts[3])
            else:
                ls(cwd, cu, input_parts[1], input_parts[2], 
                   input_parts[3], input_parts[4])

def exit_program(cu):
    print('bye, ' + cu.name)
    exit()

def pwd(cwd):
    print(cwd.get_path())        

def cd(cwd, cu, path):
    if path == '/':
        return (True, 'root_dir')
    if path[0] == '/':
        while cwd.parent != None:
            cwd = cwd.parent
        path = path[1:]
    path = path.split('/')
    for i in range(len(path)):
        ancestor_exists = False
        if path[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(path) - 1:
                return (True, cwd)
            continue
        if path[i] == '.' or path[i] == '/':
            if i == len(path) - 1:
                return (True, cwd) 
            continue
        for directory in cwd.contents:
            if path[i] == directory.name:
                if i == len(path) - 1:
                    if directory.isdir:
                        if directory.owner == cu or directory.perms[6] == 'x':
                            return (True, directory)
                        print('cd: Permission denied')
                        return (False, 0)
                    print('cd: Destination is a file')
                    return (False, 0)
                ancestor_exists = True
                cwd = directory
                break
        if not ancestor_exists:
            print('cd: No such file or directory')
            return (False, 0)
    print('cd: No such file or directory')
    return (False, 0)

def mkdir(cwd, cu, path, flag):
    if path[0] == '/':
        path = path[1:]
    # Setting known ancestors and parent for testing perms later. 
    ancestors = cwd.ancestors.copy()
    ancestors.append(cwd.parent)
    ancestors.append(cwd)
    pwd = cwd
    parent = cwd
    path = path.split('/')
    new_contents = []  # List for new ancestor directories created if flag is used. 
    name = path[len(path) - 1]
    for i in range(len(path) - 1):
        ancestor_exists = False
        # Checking for special path cases. 
        if path[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(path) - 1:
                return (True, cwd)
            continue
        if path[i] == '.' or path[i] == '/':
            if i == len(path) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor directory exists. 
        for directory in cwd.contents:
            if path[i] == directory.name:
                ancestors.append(directory)
                ancestor_exists = True
                if i == len(path) - 2:
                    parent = directory
                    ancestors.remove(directory)
                cwd = directory
                break
        if not ancestor_exists and not flag:
            print(f'mkdir: Ancestor directory does not exist')
            return (False, 0)
        if not ancestor_exists and flag:  # Creates ancestor directory if flag is True. 
            new_ancestor = Directory(cu, cwd.ancestors + [cwd.parent], 
                                     path[i], cwd, [], False)
            cwd.contents.append(new_ancestor)
            new_contents.append(new_ancestor)
            ancestors.append(new_ancestor)
            cwd = ancestors[len(ancestors) - 1]
            if i == len(path) - 2:
                parent = cwd
                ancestors.remove(cwd)
    if parent == pwd:
        ancestors.remove(pwd)
    # Testing file and ancestor and parent permissions. 
    for ancestor in ancestors + [parent]:
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('mkdir: Permission denied')
            return (False, 0)
    if parent != None:
        if parent.owner != cu and parent.perms[5] != 'w':
            print('mkdir: Permission denied')
            return (False, 0)
    for dr in parent.contents:
        if dr.name == name and not flag:
            print('mkdir: File exists')
            return (False, 0)
    if flag:
        return (True, Directory(cu, ancestors, name, parent, [], False), 
                new_contents)
    return (True, Directory(cu, ancestors, name, parent, [], False))
    
def touch(cwd, cu, path):
    if path[0] == '/':
        path = path[1:]
    ancestors = cwd.ancestors.copy() 
    parent = cwd
    path = path.split('/')
    name = path[len(path) - 1]
    for i in range(len(path) - 1):
        # Checking for special path cases. 
        ancestor_exists = False
        if path[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(path) - 1:
                return (True, cwd)
            continue
        if path[i] == '.' or path[i] == '/':
            if i == len(path) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor directory exists. 
        for directory in cwd.contents:
            if path[i] == directory.name:
                if directory.isdir:  
                    ancestors.append(directory)
                    ancestor_exists = True
                    if i == len(path) - 2:
                        parent = directory
                        ancestors.remove(directory)
                    cwd = directory
                    break
        # Printing error and returning false if ancestor directory doesn't exist. 
        if not ancestor_exists:
            print(f'touch: Ancestor directory does not exist')
            return (False, 2)
    # Testing for correct ancestor and parent permissions. 
    for ancestor in ancestors + [parent]:
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('touch: Permission denied')
            return (False, 3)
    if parent.owner != cu and parent.perms[5] != 'w':
        print('touch: Permission denied')
        return (False, 4)
    return (True, File(cu, ancestors, name, parent))

def cp(cwd, cu, src, dst):
    if src[0] == '/':
        src = src[1:]
    if dst[0] == '/':
        dst = dst[1:]
    dst_ancestors = cwd.ancestors.copy()
    temp_src_cwd = cwd
    temp_dst_cwd = cwd
    src = src.split('/')
    dst = dst.split('/')
    src_parent = cwd
    dst_parent = cwd
    f = None

    for i in range(len(dst)):
        ancestor_exists = False
        # Checking for special path cases. 
        if dst[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(dst) - 1:
                return (True, cwd)
            continue
        if dst[i] == '.' or dst[i] == '/':
            if i == len(dst) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor exists. 
        for directory in temp_dst_cwd.contents:
            if dst[i] == directory.name:
                ancestor_exists = True
                temp_dst_cwd = directory
                if i == len(dst) - 1:
                    if directory.isdir:
                        print('cp: Destination is a directory')
                        return (False, 0)
                    print('cp: File exists')
                    return (False, 0)
                else:
                    if not directory.isdir:
                        print('cp: No such file or directory')
                        return (False, 0)
                    if i == len(dst) - 2:
                        dst_parent = directory
                    else:
                        dst_ancestors.append(directory)
                break
        if i == len(dst) - 1:
            d_name = dst[len(dst) - 1]
            break
        if not ancestor_exists:
            print('cp: No such file or directory')
            return (False, 0)

    for i in range(len(src)):
        ancestor_exists = False
        # Checking for special path cases. 
        if src[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(src) - 1:
                return (True, cwd)
            continue
        if src[i] == '.' or src[i] == '/':
            if i == len(src) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor exists. 
        for directory in temp_src_cwd.contents:
            if src[i] == directory.name:
                ancestor_exists = True
                temp_src_cwd = directory
                if i == len(src) - 1:
                    if directory.isdir:
                        print('cp: Source is a directory');
                        return (False, 0)
                    f = directory
                else:
                    if not directory.isdir:
                        print('cp: No such file or directory')
                        return (False, 0)
                break
        if i == len(src) - 1 and f == None:
            print('cp: No such file')
            return (False, 0)
        if not ancestor_exists:
            print(f'cp: No such file or directory')
            return (False, 0)
    # Testing ancestors and parent and file permissions. 
    for ancestor in (f.ancestors + dst_ancestors + [f.parent] + [dst_parent]):
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('cp: Permission denied')
            return (False, 0)
    if f.owner != cu and f.perms[4] != 'r':
        print('cp: Permission denied')
        return (False, 0)
    if dst_parent.owner != cu and dst_parent.perms[5] != 'w':
        print('cp: Permission denied')
        return (False, 0)
    copied_file = File(f.owner, dst_ancestors, d_name, dst_parent)
    dst_parent.contents.append(copied_file)  # Adding copied file to destination parent contents. 
    return (True, copied_file)

def mv(cwd, cu, src, dst):
    if src[0] == '/':
        src = src[1:]
    if dst[0] == '/':
        dst = dst[1:]
    dst_ancestors = cwd.ancestors.copy()
    temp_src_cwd = cwd
    temp_dst_cwd = cwd
    src = src.split('/')
    dst = dst.split('/')
    dst_parent = cwd
    f = None

    for i in range(len(dst)):
        ancestor_exists = False
        # Checking for special path cases. 
        if dst[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(dst) - 1:
                return (True, cwd)
            continue
        if dst[i] == '.' or dst[i] == '/':
            if i == len(dst) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor exists. 
        for directory in temp_dst_cwd.contents:
            if dst[i] == directory.name:
                ancestor_exists = True
                temp_dst_cwd = directory
                if i == len(dst) - 1:
                    if directory.isdir:
                        print('mv: Destination is a directory')
                        return (False, 0, 0)
                    print('mv: File exists')
                    return (False, 0, 0)
                else:
                    if not directory.isdir:
                        print('mv: No such file or directory')
                        return (False, 0, 0)
                    if i == len(dst) - 2:
                        dst_parent = directory
                    else:
                        dst_ancestors.append(directory)
                break
        if i == len(dst) - 1:
            break
        if not ancestor_exists:
            print('mv: No such file or directory')
            return (False, 0, 0)

    for i in range(len(src)):
        ancestor_exists = False
        # Checking for special path cases. 
        if src[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(src) - 1:
                return (True, cwd)
            continue
        if src[i] == '.' or src[i] == '/':
            if i == len(src) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor exists. 
        for directory in temp_src_cwd.contents:
            if src[i] == directory.name:
                ancestor_exists = True
                temp_src_cwd = directory
                if i == len(src) - 1:
                    if directory.isdir:
                        print('mv: Source is a directory');
                        return (False, 0, 0)
                    f = directory
                else:
                    if not directory.isdir:
                        print('mc: No such file or directory')
                        return (False, 0, 0)
                break
        if i == len(src) - 1 and f == None:
            print('mv: No such file')
            return (False, 0, 0)
        if not ancestor_exists:
            print(f'mv: No such file or directory')
            return (False, 0, 0)
    # Testing permissions for ancestors and parents and files.
    for ancestor in (f.ancestors + dst_ancestors + [f.parent] + [dst_parent]):
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('mv: Permission denied')
            return (False, 3)
    if dst_parent.owner != cu and dst_parent.perms[5] != 'w':
        print('mv: Permission denied')
        return (False, 0)
    if f.parent.owner != cu and f.parent.perms[5] != 'w':
        print('mv: Permission denied')
        return (False, 0)
    f.parent.contents.remove(f)  # Removing file from its parents contents. 
    f.ancestors = dst_ancestors  # Changing files ancestors to new ancestors. 
    f.parent = dst_parent  # Changing files parent to new parent. 
    dst_parent.contents.append(f)  # Adding file to new parents contents. 
    return

def rm(cwd, cu, path):
    if path[0] == '/':
        path = path[1:]
    path = path.split('/')
    f = None

    for i in range(len(path)):
        ancestor_exists = False
        # Checking for special path cases. 
        if path[i] == '..':
            if cwd.parent != None:
                cwd = cwd.parent
            if i == len(path) - 1:
                return (True, cwd)
            continue
        if path[i] == '.' or path[i] == '/':
            if i == len(path) - 1:
                return (True, cwd) 
            continue
        # Finding if ancestor exists. 
        for directory in cwd.contents:
            if path[i] == directory.name:
                ancestor_exists = True
                cwd = directory
                if i == len(path) - 1:
                    if directory.isdir:
                        print('rm: Is a directory');
                        return (False, 0, 0)
                    f = directory
                break
        if i == len(path) - 1 and f == None:
            print('rm: No such file')
            return (False, 0, 0)
        if not ancestor_exists:
            print('rm: Ancestor directory does not exist')
            return (False, 0, 0)
    # Testing permissions for ancestors and parent and file. 
    for ancestor in f.ancestors + [f.parent]:
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('rm: Permission denied')
            return (False, 3)
    if f.owner != cu and f.perms[5] != 'w':
        print('rm: Permission denied')
        return (False, 0)
    if f.parent.owner != cu and f.parent.perms[5] != 'w':
        print('rm: Permission denied')
        return (False, 0)
    f.parent.contents.remove(f)  # Removes file form parents contents. 
    return (True, f)

def rmdir(cwd, cu, path):
    count = 0
    # Testing special path cases.
    if path == '..':
        if cwd.parent != None:
            f = cwd.parent
        if cwd.parent == None:
            print('rmdir: Cannot remove pwd')
            return (False, 0)
    if path == '.':
        print('rmdir: Cannot remove pwd')
        return (False, 0)
    if path == '/':
        while cwd.parent != None:
            cwd = cwd.parent
        if len(cwd.contents) > 0:
            print('rmdir: Directory not empty')
            return (False, 0)
        print('rmdir: Cannot remove pwd')
        return (False, 0)
    if path[0] == '/':
        while cwd.parent != None:
            cwd = cwd.parent
            count -= 1
        path = path[1:]
    path = path.split('/')
    d = None
    for i in range(len(path)):
        ancestor_exists = False
        # Checking for special path cases. 
        if path[i] == '..':
            count -= 1
            if cwd.parent != None:
                cwd = cwd.parent
        if i == len(path) - 1:
            if path[i] == '..':
                print('rmdir: Directory not empty')
                return (False, 0)
            if path[i] == '.' and len(cwd.contents) > 0:
                print('rmdir: Directory not empty')
                return (False, 0)
        # Finding if ancestor directory exists. 
        for directory in cwd.contents:
            if path[i] == directory.name:
                ancestor_exists = True
                cwd = directory
                if i == len(path) - 1:
                    if not directory.isdir:
                        print('rmdir: Not a directory');
                        return (False, 0)
                    if len(directory.contents) > 0:
                        print('rmdir: Directory not empty')
                        return (False, 0)
                    if directory == pwd:
                        print('rmdir: Cannot remove pwd')
                        return (False, 0)
                    d = directory
                count += 1
                break
        
        if i == len(path) - 1 and d == None:
            print('rmdir: No such file or directory')
            return (False, 0)
        if not ancestor_exists:
            print('rm: No such file or directory')
            return (False, 0)
        if count <= 0:
            print('rmdir: Cannot remove pwd')
            return (False, 0)
    # Testing permissions if user isn't root user. 
    if not cu.is_super_user:
        for ancestor in d.ancestors + [d.parent]:
            if ancestor == None:
                continue
            if ancestor.owner != cu and ancestor.perms[6] != 'x':
                print('rmdir: Permission denied')
                return (False, 0)
        if d.parent.owner != cu and d.parent.perms[5] != 'w':
            print('rmdir: Permission denied')
            return (False, 0)
    d.parent.contents.remove(d)  # Removing directory from parents contents. 
    return (True, d)

def chmod(cwd, cu, s, path, flag):
    files = []  # List of files in which permissions will be altered. 
    # Checking for special path cases. 
    if path == '/':
        while cwd.parent != None:
            cwd = cwd.parent
        files.append(cwd)
    if path[0] == '/':
        path = path[1:]
    path = path.split('/')
    for i in range(len(path)):
        if flag:  # If flag was inputted, adds contents of current directory to files list. 
            for f in cwd.contents:
                files.append(f)
        ancestor_exists = False
        if path[i] == '':
            continue
        # Finding if ancestor exists. 
        for directory in cwd.contents:
            if path[i] == directory.name:
                ancestor_exists = True
                cwd = directory
                if flag or i == len(path) - 1:
                    files.append(directory)
                break
        if i == len(path) - 1 and files == []:
            print('chmod: No such file or directory')
            return
        if not ancestor_exists:
            print('chmod: No such file or directory')
            return
    for ancestor in files[len(files) - 1].ancestors:
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('chmod: Permission denied')
            return
    # Testing permissions for files. 
    for f in files:
        if f.owner != cu and not cu.is_super_user: 
            print('chmod: Operation not permitted')
            return
        if f.parent != None and f.parent.owner != cu:
            if f.parent.perms[6] != 'x':
                print('chmod: Permission denied')
                return
    # Finding which operator is used. 
    operator = ''
    if '-' in s:
        s = s.split('-')
        operator = '-'
    elif '+' in s:
        s = s.split('+')
        operator = '+'
    else:
        s = s.split('=')
        operator = '='
    # Making dictionaries to convert between octal form and string form.
    octal_to_perms = {
        0 : '---',
        1 : '--x',
        2 : '-w-',
        3 : '-wx',
        4 : 'r--',
        5 : 'r-x',
        6 : 'rw-',
        7 : 'rwx',
    }
    perms_to_octal = {
        '---' : 0,
        '--x' : 1, 
        '-w-' : 2, 
        '-wx' : 3,  
        'r--' : 4,
        'r-x' : 5, 
        'rw-' : 6, 
        'rwx' : 7, 
    }
    # Getting current user perms for all files in files list. 
    current_perms_octal = []
    for i in range(len(files)):
        current_user_perms = files[i].perms[1:4]
        current_other_perms = files[i].perms[4:]
        current_perms_octal.append([
                                    perms_to_octal[current_user_perms], 
                                    perms_to_octal[current_other_perms]
                                    ])
    # Finding the modification in string format depending on the input from user. 
    if len(s[1]) == 0:
        modification = '---'
    elif len(s[1]) == 1:
        if s[1] == 'r':
            modification = 'r--'
        elif s[1] == 'w':
            modification = '-w-'
        elif s[1] == 'x':
            modification = '--x'
    elif len(s[1]) == 2:
        if 'x' not in s[1]:
            modification = 'rw-'
        if 'w' not in s[1]:
            modification = 'r-x'
        if 'r' not in s[1]:
            modification = '-wx'
    else:
        modification = 'rwx'
    final_perms = []
    # If operator is equals, this simply sets all perms of files to the modification. 
    if operator == '=':
        if s[0] == 'a':
            for i in range(len(files)):
                final_perms.append([modification, modification])
        else:
            for i in range(len(files)):
                final_perms.append(modification)
    # Otherwise see whether operator is + or -. 
    else:
        mod_octal = perms_to_octal[modification]
        if operator == '+':
            # Tests if modifiction should be applied to user perms. 
            if s[0] == 'u':
                no_dash_mod = ''.join(modification.strip('-').split('-'))  # Removes dashes from string modification
                for i in range(len(files)):
                    no_dash_perms = ''.join(octal_to_perms[current_perms_octal[i][0]]
                                            .strip('-')
                                            .split('-'))  # Removes dashes from current perms.
                    # Add octal form of both and append to final perms if they they don't exist in each other. 
                    if no_dash_mod not in no_dash_perms and no_dash_perms not in no_dash_mod:
                        final_perms_octal = current_perms_octal[i][0] + mod_octal
                        if final_perms_octal > 7:
                            final_perms_octal = 7
                        final_perms.append(octal_to_perms[final_perms_octal])
                    # Else append to final perms the whichever in octal form is smaller.
                    else:
                        if current_perms_octal[i][0] > mod_octal:
                            final_perms.append(octal_to_perms[current_perms_octal[i][0]])
                        else:
                            final_perms.append(modification) 
            # Repeats above but just for "other" section of perms instead of user section. 
            elif s[0] == 'o':
                no_dash_mod = ''.join(modification.strip('-').split('-'))
                for i in range(len(files)):
                    no_dash_perms = ''.join(octal_to_perms[current_perms_octal[i][1]]
                                            .strip('-')
                                            .split('-'))
                    if no_dash_mod not in no_dash_perms and no_dash_perms not in no_dash_mod:
                        final_perms_octal = current_perms_octal[i][1] + mod_octal
                        if final_perms_octal > 7:
                            final_perms_octal = 7
                        final_perms.append(octal_to_perms[final_perms_octal])
                    else:
                        if current_perms_octal[i][1] > mod_octal:
                            final_perms.append(octal_to_perms[current_perms_octal[i][1]])
                        else:
                            final_perms.append(modification)
            else:
                for i in range(len(files)):
                    final_perms_octal = [
                                         current_perms_octal[i][0] + mod_octal, 
                                         current_perms_octal[i][1] + mod_octal
                                        ]
                    for i in range(2):
                        if final_perms_octal[i] > 7:
                            final_perms_octal[i] = 7
                    final_perms.append([
                                        octal_to_perms[final_perms_octal[0]], 
                                        octal_to_perms[final_perms_octal[1]]
                                       ])
        elif operator == '-':
            # Test for if modification should be done to user perms. 
            if s[0] == 'u':
                no_dash_mod = ''.join(modification.strip('-').split('-'))  # Removes dashes from string modification
                for i in range(len(files)):
                    no_dash_perms = ''.join(octal_to_perms[current_perms_octal[i][0]]
                                            .strip('-')
                                            .split('-'))  # Removes dashes from current perms. 
                    # Minus octal form of modification and current perms if either exist in the other. 
                    if no_dash_mod in no_dash_perms or no_dash_perms in no_dash_mod:
                        final_perms_octal = current_perms_octal[i][0] - mod_octal
                        if final_perms_octal < 0:
                            final_perms_octal = 0
                        final_perms.append(octal_to_perms[final_perms_octal])
                    # Else just append to final perms whichever is larger in octal format. 
                    else:
                        if current_perms_octal[i][0] < mod_octal:
                            final_perms.append(modification)
                        else:
                            final_perms.append(octal_to_perms[current_perms_octal[i][0]])
            # Same as for user but just applied to other perms instead. 
            elif s[0] == 'o':
                no_dash_mod = ''.join(modification.strip('-').split('-'))
                for i in range(len(files)):
                    no_dash_perms = ''.join(octal_to_perms[current_perms_octal[i][1]]
                                            .strip('-')
                                            .split('-'))
                    if no_dash_mod in no_dash_perms or no_dash_perms in no_dash_mod:
                        final_perms_octal = current_perms_octal[i][1] - mod_octal
                        if final_perms_octal < 0:
                            final_perms_octal = 0
                        final_perms.append(octal_to_perms[final_perms_octal])
                    else:
                        if current_perms_octal[i][1] < mod_octal:
                            final_perms.append(modification)
                        else:
                            final_perms.append(octal_to_perms[current_perms_octal[i][1]])
            else:
                for i in range(len(files)):
                    final_perms_octal = [
                                         current_perms_octal[i][0] - mod_octal, 
                                         current_perms_octal[i][1] - mod_octal
                                        ]
                    for i in range(2):
                        if final_perms_octal[i] < 0:
                            final_perms_octal[i] = 0
                    final_perms.append([
                                        octal_to_perms[final_perms_octal[0]], 
                                        octal_to_perms[final_perms_octal[1]]
                                       ])
    # Sets perms for all files according to which was modified. 
    if s[0] == 'u':
        for i in range(len(files)):
            files[i].perms = files[i].perms[0] + final_perms[i] + files[i].perms[4:]
    elif s[0] == 'o':
        for i in range(len(files)):
            files[i].perms = files[i].perms[0:4] + final_perms[i]
    else:
        for i in range(len(files)):
            files[i].perms = files[i].perms[0] + final_perms[i][0] + final_perms[i][1]
    return

def chown(cwd, user, path, flag):
    files = []  # List of files that will need their owner changed. 
    if path == '/':
        while cwd.parent != None:
            for f in cwd.contents:
                files.append(f)
            cwd = cwd.parent
    if path[0] == '/':
        path = path[1:]
    path = path.split('/')
    for i in range(len(path)):
        ancestor_exists = False
        if path[i] == '.':
            ancestor_exists = True
        if flag:
            for f in cwd.contents:
                files.append(f)
        # Finds if ancestor exists. 
        for directory in cwd.contents:
            if path[i] == directory.name:
                ancestor_exists = True
                cwd = directory
                if flag or i == len(path) - 1:
                    files.append(directory)
                break
        if i == len(path) - 1 and files == []:
            print('chown: No such file or directory')
            return
        if not ancestor_exists:
            print('chown: No such file or directory')
            return
    # Changes owner to entered user for all files in files. 
    for f in files:
        f.owner = user
    return
    
def adduser(users, user):
    # Checks if user already exists. 
    for u in users:
        if u.name == user:
            print('adduser: The user already exists')
            return (False, 0)
    return (True, User(user, False))  # Creates and returns new user. 

def deluser(users, user):
    # Finds user and checks if it is the root user. 
    for u in users:
        if u.name == user:
            if u.is_super_user:
                print('''WARNING: You are just about to delete the root account
Usually this is never required as it may render the whole system unusable
If you really want this, call deluser with parameter --force
(but this `deluser` does not allow `--force`, haha)
Stopping now without having performed any action''')
                return (False, 0)
            return (True, u)
    print('deluser: The user does not exist')
    return (False, 0)

def su(users, user):
    for u in users:
        if u.name == user:
            return (True, u)
    print('su: Invalid user')
    return (False, 0)

def ls(cwd, cu, *flags_and_path):       
    a_flag = False
    d_flag = False
    l_flag = False
    path = None
    # Finds which flags were entered and if a path was entered. 
    for thing in flags_and_path:
        if thing == '-a':
            a_flag = True
        elif thing == '-d':
            d_flag = True
        elif thing == '-l':
            l_flag = True
        else:
            path = thing
    if path == None:
        f = cwd
    else: 
        if path == '/':
            while cwd.parent != None:
                cwd = cwd.parent
            f = cwd
        if path[0] == '/':
            path = path[1:]
        path = path.split('/')
        f = None

        for i in range(len(path)):
            ancestor_exists = False
            # Tests for special path cases. 
            if path[i] == '..':
                if cwd.parent != None:
                    cwd = cwd.parent
                if i == len(path) - 1:
                    return (True, cwd)
                continue
            if path[i] == '.' or path[i] == '/':
                if i == len(path) - 1:
                    return (True, cwd) 
                continue
            # Finds if ancestor exists. 
            for directory in cwd.contents:
                if path[i] == directory.name:
                    ancestor_exists = True
                    cwd = directory
                    if i == len(path) - 1:
                        f = directory
                    break
            if (i == len(path) - 1 and f == None) or not ancestor_exists:
                print('ls: No such file or directory')
                return
    # Tests permissions for ancestors and parent and file. 
    for ancestor in f.ancestors:
        if ancestor == None:
            continue
        if ancestor.owner != cu and ancestor.perms[6] != 'x':
            print('ls: Permission denied')
            return
    if not f.isdir or d_flag:
        if f.parent.perms[4] != 'r' or f.owner != cu:
            print('ls: Permission denied')
            return
    if f.isdir and f.perms[4] != 'r':
        print('ls: Permission denied')
        return
    # Depending on which flags were entered, prints the appropriate output.
    if f.isdir:
        if d_flag:
            if f.name == None:
                print(f'{f.perms} {f.owner.name} /')
            elif f.name[0] == '.' and not a_flag:
                pass
            elif l_flag:
                print(f'{f.perms} {f.owner.name} {f.name}')
            else:
                print(f.name)
        else:
            things = []
            if a_flag:
                for content in f.contents:
                    if content.name[0] != '.':
                        things.append(content)
            else:
                for content in f.contents:
                    things.append(content)
            if l_flag:
                for content in things:
                    print(f'{content.perms} {content.owner.name} {content.name}')
            else:
                for content in things:
                    print(content.name)
    else:
        print(f.name)
        
def get_input_parts(string):
    string = string.strip()  # Removes any whitespace from the sides. 
    input_parts = []

    # Tests for if quotations are in the input. 
    if '"' in string: 
        i = 0
        current_arg_start = 0
        middle_of_quotation = False
        while i < len(string):
            if string[i] == ' ' and not middle_of_quotation:
                arg = string[current_arg_start:i]
                arg = arg.split('"')
                arg = ''.join(arg)
                input_parts.append(arg)
                if i == len(string) - 1:
                    break
                k = 1
                while string[i + k] == ' ':
                    k += 1
                i += k
                current_arg_start = i
            elif string[i] == '"':
                if middle_of_quotation:
                    middle_of_quotation = False
                else:
                    middle_of_quotation = True
                i += 1
            else: 
                i += 1
        arg = string[current_arg_start:i]
        if not middle_of_quotation and '"' in arg:
            arg = arg.split('"')
            arg = ''.join(arg)
            input_parts.append(arg)
        else:
            input_parts.append(arg)
    # If quotations are not in the input, can simply split the input by spaces.
    else:
        input_parts = string.split()
    return input_parts

def valid_syntax(input_parts):
    # Creates a dictionary associating the command with the possible flags, 
    # and the number of arguments allowed for that command
    cmd_flags_numargs = {
        'exit' : [['p'], 0],
        'pwd' : [[], 0],
        'cd' : [[], 1],
        'mkdir' : [['-p'], 1],
        'touch' : [[], 1],
        'cp' : [[], 2],
        'mv' : [[], 2],
        'rm' : [[], 1],
        'rmdir' : [[], 1],
        'chmod' : [['-r'], 2],
        'chown' : [['-r'], 2],
        'adduser' : [[], 1],
        'deluser' : [[], 1],
        'su' : [[], 1],
        'ls' : [['-a', '-d', '-l'], 1],
    }
    # Tests for if nothing was entered, and if the command entered doesn't exist.
    if len(input_parts) == 0:
        return False
    cmd = input_parts[0]
    if not cmd in cmd_flags_numargs:
        print(f'{cmd}: Command not found')
        return False
    # Sets allowed flags and args for the command that was entered. 
    allowed_flags = cmd_flags_numargs[cmd][0]
    num_args = cmd_flags_numargs[cmd][1]
    entered_flags = []
    entered_args = []
    no_more_flags = False
    for s in input_parts[1:]:
        if s[0] == '-':
            if no_more_flags:
                print(f'{cmd}: Invalid syntax')
                return False
            entered_flags.append(s)
        else:
            no_more_flags = True
            entered_args.append(s)
    if len(entered_flags) > len(allowed_flags):
        print(f'{cmd}: Invalid syntax')
        return False
    if len(entered_args) != num_args:
        # ls and su commands can have variable number of args, so must account for this
        if cmd != 'ls' and cmd != 'su':  
            print(f'{cmd}: Invalid syntax')
            return False
    for flag in entered_flags:
        acceptable_flag = False
        for f in allowed_flags:
            if f == flag:
                acceptable_flag = True
                break
        if not acceptable_flag:
            print(f'{cmd}: Invalid syntax')
            return False
    accepted_characters = 'abcdefghijklmnopqrstuvwxyz0123456789 "-._/'
    # Chmod syntax is very different from everything else. So checks specifically.
    if cmd == 'chmod':
        mode = ['uoa', '-+=', 'rwx']  # List of allowed characters for each argument.
        splitter = ''
        # Finds operator entered, returns False if there is more than one.
        for char in entered_args[0]:
            if char == '-':
                if not splitter == '':
                    print(f'{cmd}: Invalid syntax')
                    return False
                splitter = '-'
            elif char == '+':
                if not splitter == '':
                    print(f'{cmd}: Invalid syntax')
                    return False
                splitter = '+'
            elif char == '=':
                if not splitter == '':
                    print(f'{cmd}: Invalid syntax')
                    return False
                splitter = '='
        # Returns false if no operator was found.
        if splitter == '':
            print(f'{cmd}: Invalid syntax')
            return False
        s_list = entered_args[0].split(splitter)
        # Checks each character before and after operator are valid
        for char in s_list[0]:
            if char not in mode[0]:
                print(f'{cmd}: Invalid syntax')
                return False
        for char in s_list[1]:
            if char not in mode[2]:
                print(f'{cmd}: Invalid syntax')
                return False
        entered_args.pop(0)
        return True
    # Checks for all other commands that each character is a valid character.
    for arg in entered_args:
        for char in arg:
            if char.lower() not in accepted_characters:
                print(f'{cmd}: Invalid syntax')
                return False
    return True

if __name__ == '__main__':
    main()
