
from getpass import getpass
from passMan import *

folder = 'db'
dbFile = 'test.db'
dbList = 'passwords'

# makes directory for db file
makeDir(folder)

# connect to db
connectDB(f"{folder}/{dbFile}")

# clears window
clear()

# returns boolean whether there are already passwords
listExist = checkForPasswords(dbList)
checkMPExist()
createPasswords()

while True:
    # try:
        #repeats until 'q'
    print("*"*15)
    print("COMMANDS:\n")
    if listExist: # if there are no passwords don't show those options
        print("l = list your passwords")
        print("r = request password")
    print("a = add password")
    if listExist:
        print("d = delete password")
        print("c = change service password")
    print("m = change master pasword")
    print("q = quit")
    print("*"*15)
    
    op = input(": ")
    clear()

    if op.lower() == 'l':
        read() #reads list of passwords
    if op.lower() == 'r':
        #prints specific row of table
        request = input("From which service: ")
        read(request)
    if op.lower() == 'a':
        #adds new password
        service = input("What is the name of the service: ")
        add_password(service)
        read()
        if not(listExist):
            listExist = True
    if op.lower() == 'd':
        #deletes existing passwords
        delete_service = input("Which service do you want to delete: ")
        clear()
        if existing(delete_service):
            print("Are you sure you want to delete", delete_service, "? (y/n)")
            if input() == 'y':
                delete(delete_service)
                read()
        else:
            print(f"'{delete_service}' is not in your list yet - can not be deleted.")
            read()
    
    if op.lower() == 'c':
        #changes service passwords
        service = input("Which services password do you want to change: ")
        if existing(service):
            update_pass(generate(), service)
            read()
        else:
            clear()
            if input("This service does not exist yet, do you want to add it? (y/n)") == 'y':
                add_password(service)
                read()

    if op.lower() == 'm':
        #changes master password
        change_Password()
        input("\nPress any key... ")
    if op.lower() == 'q':
        break
    
    clear()
    # except Exception as e:
    #     print("An error has ocurred.\n" + str(e))
    #     input("\nPress any key...")

closePass()
