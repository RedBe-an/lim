import os
from core.errors.error import notExistError


def set_props() :
    exist_bat = os.path.exists("server.properties")
    if not exist_bat :
        raise notExistError
    
    with open("server.properties", "r", encoding="utf-8") as file :
        data = file.read()
    