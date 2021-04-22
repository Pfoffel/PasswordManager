import os
import secrets
import sqlite3
import string
from getpass import getpass
from tabulate import tabulate

CASES = string.ascii_letters + string.digits + string.punctuation

def clear(): #clear screen function
    os.system('cls')

# create dir for db
def makeDir(name):
    try:
        os.mkdir('db')
        print("Created successfully")
    except:
        print("Already created")

# crate connection to db and cursor
def connectDB(dir):
    global con
    global cur
    con = sqlite3.connect(dir)
    cur = con.cursor()

# returns true if there are already passwords, false if not
def checkForPasswords(l):
    try:
        cur.execute(f'SELECT * FROM {l}')
        if len(cur.fetchall()) == 0:
            return False
        return True
    except:
        return False

def checkMPExist():
    try:
        #tries to create a new master password table, if it exists already goes to 'except'
        cur.execute(
            '''CREATE TABLE pass_manager(
                masterPassword text
            )'''
        )
        print("Create a new Master Password\n\n")
        create_MP()
    except:
        #password already existing, asking for it
        password = getpass("Introduce your Master Password: ")
        clear()
        check_masterPass(password)

def createPasswords():
    try:
        #tries to create passwords table, if existing goes to 'except'
        cur.execute('''CREATE TABLE passwords
        (service text, password text)''')
        print("Welcome to your Password Manager.\n")
    except:
        #already existing
        print("Welcome back.\n")

def printList(tuple_list):#string generator
    if len(tuple_list)!=0:
        passList = []
        for service, passwd in tuple_list:
            passList.append([service, passwd])
        print(tabulate(passList, headers=["Service", "Password"], tablefmt="orgtbl"))
    else:
        print("\nThis service is not stored yet.")

def checkChars(password): # checks the chars in the password
    for i in range(len(password)):
        if password[i] not in CASES:
            return False, i
    return True, i
    

def generate(service = 0):
    print("Do you want a custom password or a generated one?\n\n")
    print("*"*15)
    print("COMMANDS:\n")
    print("1 = custom password")
    print("2 = generated password")
    print("*"*15)
    custom = int(input(": "))
    clear()
    if custom == 1:
        new_password = input("\nIntroduce the password: ")
        valid, i = checkChars(new_password)
        while not valid or len(new_password)<8:
            if not valid:
                if new_password[i] == ' ':
                    print("The password can not contain spaces.")
                else:
                    print(f"The password can not contain '{new_password[i]}'") 
            if len(new_password)<8:
                print("The password should be at least 8 characters long...")
            new_password = input("\nIntroduce a valid password: ")
            valid, i = checkChars(new_password)    
            clear()
    elif custom == 2:
        length = int(input("\nHow long do you want the password to be: "))
        clear()
        while length<8:
            print("The password should be at least 8 characters long...")
            length = int(input("\nHow long do you want the password to be: "))
            clear()
        new_password = ''.join(secrets.choice(CASES) for i in range(length))
    if service != 0:
        insert((service, new_password))
    else:
        return new_password

def update_pass(password, service=0): #updates passwords if service = 0 master password else specific one
    q1 = "UPDATE pass_manager SET masterPassword = ?"
    q2 = "UPDATE passwords SET password = ? WHERE service = '{}'".format(service)
    if service == 0:
        cur.execute(q1, (password,))    
    else:
        cur.execute(q2, (password,))
    con.commit()

def create_MP(change = 0): #loop for new master password
    while True:
        while True:
            pwd = getpass("New password: ")
            if len(pwd) >= 8:
                break
            clear()
            print("The password should be 8 characters long...\n")

        pwdC = getpass("Confirm new password: ")
        if pwd == pwdC:
            break
        clear()
        print("Passwords do not match...")
    if change == 0:
        cur.execute("INSERT INTO pass_manager VALUES (?)", (pwd,)) #inserts master password into table
        con.commit()
    else:
        update_pass(pwd) #updates existing one with the new one
    clear()
    print("\nYour master password has been successfully created.")

def check_masterPass(passwd): #compares whether valid or not
    cur.execute("SELECT masterPassword FROM pass_manager")
    while cur.fetchone()[0] != passwd: #as long as the right password is not introduced, repeats
        passwd = getpass('That was not correct.\nInput the correct Master Password: ')
        cur.execute("SELECT masterPassword FROM pass_manager")
        clear()

def change_Password(): #changes masterpassword
    password = getpass("Introduce your current Master Password: ")
    check_masterPass(password)
    print("Now introduce your new password\n\n")
    create_MP(1)

def read(request = 0):#print elements of tables if there is a request it prints just that one
    if request == 0:
        print("\nYour list is currently: \n\n")
        cur.execute("SELECT * FROM passwords ORDER BY service")
        printList(cur.fetchall())
    else:
        cur.execute('SELECT * FROM passwords WHERE service=?',(request,))
        printList(cur.fetchall())
        
    input("\nPress any key... ")

def insert(to_add): #inserts the values into the tables
    q1 = "INSERT INTO passwords VALUES {}".format(to_add) 
    cur.execute(q1)
    con.commit()

def delete(delete_service): #deletes cirtain values
    cur.execute("DELETE FROM passwords WHERE service=?", (delete_service,))
    con.commit()

def existing(to_add):# checks for existing services
    cur.execute("SELECT service FROM passwords ORDER BY service")
    site_list = cur.fetchall()
    for service in site_list:
        if to_add in service:
            return True # exists
    return False #not existing

def add_password(new_service): #adds password to database 
    if not existing(new_service):
        generate(new_service)
    else:
        clear()
        print("You already have a password for this service.")
        print("Do you prefere to update the password of", new_service, "? (y/n)")
        if input() == 'y':
            new_password = generate()
            update_pass(new_password, new_service)

def closePass():
    con.close()
    print("The manager has been closed correctly.")