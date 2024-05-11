from typing import NoReturn, TypeAlias
from requests import get
import sys
import time
import json
from enum import Enum, auto

class messageType(Enum) :
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    QUESTION = auto()
class logger() :
    def __init__(self) :
        self
    
    def load_config(self, file_name : str, /) :
        with open (file_name, "r") as f:
            data = json.load(f)
        self.config = data
        self.log_format  =  self.config["log_format"]

    def log(self, message : str, type : messageType = "info") :
        pass

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

