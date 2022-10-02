import sys
import random
import time
from graphics import *

alphaLower = 'a'
alphaUpper = 'A'
number = '0'
special = '!@#$%^&*()'

def genRandomChar():
    typeOfChar = random.randint(1, 100000) % 4
    
    if typeOfChar == 0:
        return chr(ord(alphaLower) + random.randint(1, 100000) % 24)
    elif typeOfChar == 1:
        return chr(ord(alphaUpper) + random.randint(1, 100000) % 24)
    elif typeOfChar == 2:
        return chr(ord(number) + random.randint(1, 100000) % 10)
    elif typeOfChar == 3:
        return special[random.randint(1, 100000) % 10]

def findType(c):
    if (ord(c) <= ord(alphaLower)+24 and ord(c) >= ord(alphaLower)):
        return 0
    elif (ord(c) <= ord(alphaUpper)+24 and ord(c) >= ord(alphaUpper)):
        return 1
    elif (ord(c) <= ord(number)+10 and ord(c) >= ord(number)):
        return 2
    elif (c in special):
        return 3


def checkPass(password):
    if (len(password) < 4):
        return False

    flags = [False, False, False, False,]
    for j, c in enumerate(password):
        t = findType(c)
        for i, flag in enumerate(flags):
            if flag:
                continue
            if (t == i):
               flags[i] = True 
               continue
            if (j == len(password)-1 and not flag):
                return False 
    return True 

def genPass(length):

    password = ''
    while (not checkPass(password)):
        password = ''
        for i in range(length):
            password += genRandomChar()

    return password

def genSeed():
    seed = ''
    urandom = open('/dev/urandom', 'rb')
    return repr(urandom.read(1048576))

if __name__=='__main__':
    try:
        length = int(sys.argv[1])
        if (length < 4):
            print("Too short length!")
            exit(1)
    except IndexError:
        length = 16

    random.seed(genSeed())
    ui = UI()
    ui.displayUI()
    ui.displayFancyString(genPass(length))
