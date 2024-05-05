import os
import sys
import threading
from requests import get
import traceback


def get_prompt(prompt, color_num) -> str:
    return f"\033[{color_num}m" + prompt + "\033[0m"


def get_command(minimum, maximum, aikar, gui, serverfilename) -> str:
    aikarFlag = "-XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled -XX:+PerfDisableSharedMem -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1HeapWastePercent=5 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1NewSizePercent=30 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 -XX:MaxGCPauseMillis=200 -XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true"
    noGui = "nogui"

    startCommand = f"""
@echo off
java -Xms{minimum} -Xmx{maximum} """

    if aikar:
        startCommand += aikarFlag + " "

    if not gui:
        startCommand += noGui

    startCommand += f" -jar {serverfilename}\npause"

    return startCommand


minMem = input(get_prompt("[?] Minimum memory usage? (4096M, 4G etc...) : ", 37))
maxMem = input(get_prompt("[?] Maximum memory usage? (6144M, 6G etc...) : ", 37))
useAikar = input(get_prompt("[?] Use Aikar's flag? (y/n) : ", 37))
useGui = input(get_prompt("[?] use gui? (y/n) : ", 37))
forderName = input(get_prompt("[?] server folder name : ", 37))
serverFileVer = input(
    get_prompt(
        "[?] input server version and build number (ex. 1.20.4 | 496) (Separated by ' | '): ",
        37,
    )
).split(" | ")
serverFileURL = f"https://api.papermc.io/v2/projects/paper/versions/{serverFileVer[0]}/builds/496/downloads/paper-{serverFileVer[0]}-{serverFileVer[1]}.jar"
serverFileName = f"paper-{serverFileVer[0]}-{serverFileVer[1]}.jar"

Command = get_command(minMem, maxMem, useAikar, useGui, serverFileName)


def download(serverfileurl, file_name):
    try:
        with open(file_name, "wb") as file:
            response = get(serverfileurl)
            file.write(response.content)
    except Exception as ex:
        print(get_prompt(f"[-] ERROR : \n", 31))
        print(get_prompt(traceback.format_exc(), 31))
        sys.exit(1)


os.mkdir(forderName)
currentPath = os.getcwd()
serverFilePath = currentPath + "\\" + forderName + "\\" + serverFileName
serverForderPath = currentPath + "\\" + forderName
print(get_prompt(f"[+] Downloading server file : {serverFileName}...", 37))
download(serverFileURL, serverFilePath)
print(get_prompt(f"[+] Successfully downloaded.", 37))


def set_env():
    os.chdir(serverForderPath)
    os.system(f"{serverFilePath}")


envSetThread = threading.Thread(target=set_env, daemon=True)
envSetThread.start()

noprint = 0
while not os.path.exists("eula.txt"):
    if noprint == 0:
        print(get_prompt("[+] setting basic server settings...", 37))
        noprint = 1

agreeEULA = input(get_prompt("[?] Are you agree to mojang EULA? (y/n) : ", 37))

if agreeEULA == "y":
    agreeEULA = "true"
elif agreeEULA == "n":
    agreeEULA = "false"
    print(
        get_prompt("[-] Program is stopping because you did not accept the EULA.", 93)
    )
    sys.exit(0)

with open(serverForderPath + "\\eula.txt", "r+") as file:
    newfile = file.read().replace("false", "true")
    file.seek(0)
    file.truncate(0)
    file.write(newfile)

print(get_prompt("[+] saved eula.txt.", 37))

with open(serverForderPath + "\\start.bat", "w") as file:
    file.write(Command)

print(get_prompt("[+] saved start.bat.", 37))

nowRun = input(get_prompt("[?] Are you run your server right now? (y/n) : ", 37))

if nowRun == "y":
    print(get_prompt("[+] starting server...", 37))
    os.system(serverForderPath + "\\start.bat")
    print(get_prompt("[+] server ended.", 37))
    sys.exit(0)
elif nowRun == "n":
    print(get_prompt("[+] exiting...", 37))
    sys.exit(0)
