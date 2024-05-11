import os
import traceback
from typing import NoReturn, TypeAlias
from requests import get
import sys
import time
import json
from enum import IntEnum, auto

from error import unexpectedInputError

class promptType(IntEnum) :
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    QUESTION = auto()

class promptHelper() :
    def __init__(self, filename : str, /) :
        self.filename = filename
    
    def load_config(self) :
        with open(self.filename, "r") as f:
            data = json.load(f)
        self.config = data
        self.log_format  =  self.config["log_format"]

    def log(self, prompt : str, type : promptType = promptType.INFO, /) :
        if type == 1 :
            print(self.log_format["info"] + prompt)
        elif type == 2 :
            print(self.log_format["warn"] + prompt)
        elif type == 3 :
            print(self.log_format["error"] + prompt)
        elif type == 4 :
            return input(self.log_format["question"] + prompt + " : ")
        else :
            raise unexpectedInputError(
                "The type parameter is not an integer or a messageType class constant."
                )
            
_ExitStatus: TypeAlias = str | int | None
_MemoryValue: TypeAlias = str | int

def wait_and_exit(sleep_sec: int = 0, status: _ExitStatus = 0, /) -> NoReturn :
    time.sleep(sleep_sec) # wait for sleep_sec second.
    sys.exit(status)  # process exit with status

def get_command(min_memory: _MemoryValue,
                max_memory: _MemoryValue,
                use_aikar: bool,
                use_gui: bool,
                file_name: str) :
    
    # define flags
    aikar_flags = " ".join(
        [
            "-XX:+AlwaysPreTouch",
            "-XX:+DisableExplicitGC",
            "-XX:+ParallelRefProcEnabled",
            "-XX:+PerfDisableSharedMem",
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:+UseG1GC",
            "-XX:G1HeapRegionSize=8M",
            "-XX:G1HeapWastePercent=5",
            "-XX:G1MaxNewSizePercent=40",
            "-XX:G1MixedGCCountTarget=4",
            "-XX:G1MixedGCLiveThresholdPercent=90",
            "-XX:G1NewSizePercent=30",
            "-XX:G1RSetUpdatingPauseTimePercent=5",
            "-XX:G1ReservePercent=20",
            "-XX:InitiatingHeapOccupancyPercent=15",
            "-XX:MaxGCPauseMillis=200",
            "-XX:MaxTenuringThreshold=1",
            "-XX:SurvivorRatio=32",
            "-Dusing.aikars.flags=https://mcflags.emc.gs",
            "-Daikars.new.flags=true",
        ]
    )
    nogui_flag = " --nogui"

    command: str = f"@echo off\njava -Xms{min_memory} -Xmx{max_memory}"
    
    # Apply user selection 
    if use_aikar:
        command += aikar_flags

    if not use_gui:
        command += nogui_flag

    command += f" -jar {file_name}\npause" # -jar option and pause set 
    return command

class fileHelper() :
    def __init__(self) :
        pass

    def get_cwd() :
        return os.getcwd()

    def download_file(self, url, filename):
        try:
            response = get(url)
            with open(filename, "wb") as file:
                file.write(response.content)
        except Exception as ex:
            main_logger.log(
                f"ERROR downloading file: \n{traceback.format_exc()}", promptType.ERROR
            )
            wait_and_exit(3)
    
    def read_file(self, filename) :
        pass

    def make_file(self, filename, data) :
        pass

    def make_dir(self, dirname, path) :
        os.mkdir(path + "/" + dirname)

    def read_dir(self, dirname) :
        check_list = os.listdir(dirname)
        for checkfile in check_list :
            checkfile = f"{dirname}/{checkfile}"
            isitfile = os.path.isfile(checkfile)
            if not isitfile :
                self.read_dir(checkfile)


if __name__ == "__main__" :
    main_logger = promptHelper()
    main_logger.load_config("src\config.json")
    main_logger.log("Log Message")
