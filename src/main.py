"""
  #####    ###    #######  #### ### 
 ##   #    ###     ##  ##   ##   #  
 ###       # ##    ##   #    ## #   
  ####    #  ##    ####       ##    
    ###  #######   ##         ##    
 #   ##  #    ##   ##         ##    
 #####   ##   ### ####       ####   

- SAFY - Server Agent For only You -

LICENSE - 2024, be-noi
Generally permitted activities such as 
quoting, executing, and checking the code 
are not prohibited, but the rights to copy the code, 
leave the author unknown, and distribute commercially 
belong only to be-noi, the copyright holder of this program. 
If this is not followed, the copyright holder or agent may take legal action.
"""

from typing import NoReturn, TypeAlias
from requests import get
import os
import threading
import sys
import time
import zipfile

from core.errors.error import unexpectedInputError
from core.helper.filehelper import fileHelper
from core.helper.prompt import promptHelper, promptType
from core.variables.typevar import _ExitStatus, _MemoryValue

def wait_and_exit(sleep_sec: int = 0, status: _ExitStatus = 0, /) -> NoReturn:
    time.sleep(sleep_sec)  # wait for sleep_sec second.
    sys.exit(status)  # process exit with status


def get_command(
    min_memory: _MemoryValue,
    max_memory: _MemoryValue,
    use_aikar: bool,
    use_gui: bool,
    file_name: str,
):

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

    command += f" -jar {file_name}\npause"  # -jar option and pause set
    return command


def str_to_bool(y_or_n : str):
    s = y_or_n.lower()
    if s in ['y', 'yes', 'true', 't', '1']:
        return True
    elif s in ['n', 'no', 'false', 'f', '0']:
        return False
    else:
        raise unexpectedInputError


def run_server(server_folder, scriptfile) :
    filehelper.ch_dir(server_folder)
    os.system(f"{scriptfile}")


if __name__ == "__main__":
    filehelper = fileHelper()

    main_logger = promptHelper("src\\program\\config\\log_format.json")
    main_logger.load_config()

    safy_signature = """
  #####    ###    #######  #### ### 
 ##   #    ###     ##  ##   ##   #  
 ###       # ##    ##   #    ## #   
  ####    #  ##    ####       ##    
    ###  #######   ##         ##    
 #   ##  #    ##   ##         ##    
 #####   ##   ### ####       ####   

- SAFY - Server Agent For only You -
"""
    print(safy_signature)

    min_mem = main_logger.log(
        "Minimum memory usage (ex. 4G, 4096M)", promptType.QUESTION
    )
    max_mem = main_logger.log(
        "Maximum memory usage (ex. 6G, 6144M)", promptType.QUESTION
    )
    use_aikar = str_to_bool(
        main_logger.log(
        "Use Aikar flags? (recommended) (y/n)", promptType.QUESTION
        )
    )
    use_gui = str_to_bool(
        main_logger.log(
        "Use Paper's Server Gui? (non-recommended) (y/n)", promptType.QUESTION
        )
    )
    server_name = main_logger.log(
        "Server name (ONLY english character)", promptType.QUESTION
    )
    version_info = main_logger.log(
        "Server version info (ex. 1.20.4 496) (seperated by ' ')", promptType.QUESTION
    )

    cwd = filehelper.get_cwd()
    main_logger.log("Making server directory...")
    filehelper.make_dir(server_name, cwd)
    main_logger.log(f"{server_name} forder created in {cwd}.")

    server_folder = f"{cwd}\\{server_name}"

    server_version, build_number = version_info.split(" ")
    server_file_url = f"https://api.papermc.io/v2/projects/paper/versions/{server_version}/builds/{build_number}/downloads/paper-{server_version}-{build_number}.jar"
    server_file_name = f"paper-{server_version}-{build_number}.jar"

    main_logger.log("Downloading server file...")
    filehelper.download_file(server_file_url, server_file_name, server_folder)
    main_logger.log("Downloaded server file.")

    main_logger.log("making script file for server starting...")
    command = get_command(min_mem, max_mem, use_aikar, use_gui, server_file_name)
    filehelper.make_file("server-start.bat", server_folder, command)
    main_logger.log("saved server-start.bat.")

    server_file_path = f"{server_folder}\\{server_file_name}"
    threading.Thread(
        target=run_server, args=(server_folder, "server-start.bat"), daemon=True
    ).start()  # TODO : to function

    _ = 0
    while not os.path.exists("eula.txt"):
        if _ == 0:
            main_logger.log("Setup your server, wait...")
            _ = 1

    main_logger.log("successfully setuped.")

    agree_EULA = main_logger.log(
        "[?] Are you agree to mojang EULA? (y/n) : ", promptType.QUESTION
    )

    if agree_EULA == "y":
        agree_EULA = True
    elif agree_EULA == "n":
        agree_EULA = False
        main_logger.log(
            "Program being terminated due to non-compliance with EULA...",
            promptType.ERROR,
        )
        wait_and_exit(3, 1)

    main_logger.log("Specifying compliance with EULA...")
    with open(server_folder + "\\eula.txt", "r+") as file:
        true_eula = file.read().replace("false", "true")
        file.seek(0)
        file.truncate(0)
        file.write(true_eula)
    main_logger.log("Specified.")

    now_run = str_to_bool(
        main_logger.log(
        "Now run your server? (y/n)", promptType.QUESTION
        )
    )

    if now_run :
        run_server(server_folder, "start-server.bat")
    else :
        main_logger.log("To run it, run safy run from the server folder.")
        main_logger.log("Exit...")
        wait_and_exit(3, 0)