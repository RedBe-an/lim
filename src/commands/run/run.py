import os

from core.errors.error import notExistError


def run() :
    a = os.path.exists("server-start.bat")
    if a == True :
        os.system("server-start.bat")
    elif a == False :
        raise notExistError