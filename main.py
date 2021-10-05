import control.db as db
import sys

username = str(input('Enter username: '))
password = str(input('Enter password: '))

access, accessType = db.isThereAUserOrNot(username, password)
if access == db.accessed:
    # Continue if accessed
    print("\nAccessed as " + accessType + "\n")
else:
    print(access)
    # Close program if access denied
    sys.exit(0)

while True:
    if accessType == db.admin:
        text = """Action list:\nEnter 1 to check file\nEnter 2 to create new user\nEnter 3 to
         hash file\nEnter 0 to exit\nAction : """
    elif accessType == db.user:
        text = 'Action list:\nEnter 1 to check file\nEnter 0 to exit\nAction : '
    
    action = str(input(text))

    if action == '1':
        path = str(input('Enter file path: '))
        checked = db.checkFile(path)
        if checked[0] == True:
            print('\nLast changes were at: ' + checked[1] + '\n')
        else:
            print('\n' + checked[1] + '\n')

    if action == '2' and accessType == db.admin:
        username = str(input('Enter username: '))
        password = str(input('Enter password: '))
        accessType = str(input('Enter access type. 1 is admin. 2 is user : '))
        db.insertUser(username, password, db.admin if accessType == 1 else db.user)

    if action == '3' and accessType == db.admin:
        path = str(input('Enter file path: '))
        db.insertFile(path)

    if action == '0':
        break