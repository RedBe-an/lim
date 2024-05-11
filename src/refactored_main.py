from requests import get
import os
import sys
import threading
import time
import traceback


def exit_program(code: int = 0):
    time.sleep(3)
    sys.exit(code)


def get_colored_prompt(prompt, color_code):
    return f"{prompt}"


def get_server_start_command(
    min_memory, max_memory, use_aikar_flags, use_gui, server_filename
):
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
    no_gui_flag = " --nogui"
    start_command = f"java -Xms{min_memory} -Xmx{max_memory} "
    if use_aikar_flags == "y":
        start_command += aikar_flags + " "
    if use_gui == "n":
        start_command += no_gui_flag
    start_command += f" -jar {server_filename}"
    return start_command


def prompt_user_for_configuration():
    min_memory = input(
        get_colored_prompt("[?] Minimum memory usage? (4096M, 4G etc.): ", 37)
    )
    max_memory = input(
        get_colored_prompt("[?] Maximum memory usage? (6144M, 6G etc.): ", 37)
    )
    use_aikar_flags = input(get_colored_prompt("[?] Use Aikar's flags? (y/n): ", 37))
    use_gui = input(get_colored_prompt("[?] Use GUI? (y/n): ", 37))
    server_folder_name = input(get_colored_prompt("[?] Server folder name: ", 37))
    version_info = input(
        get_colored_prompt(
            "[?] Input server version and build number (ex. 1.20.4 496) (Separated by ' '): ",
            37,
        )
    ).split(" ")
    return (
        min_memory,
        max_memory,
        use_aikar_flags,
        use_gui,
        server_folder_name,
        version_info,
    )


def download_file(url, filename):
    try:
        response = get(url)
        with open(filename, "wb") as file:
            file.write(response.content)
    except Exception as ex:
        print(
            get_colored_prompt(
                f"[-] ERROR downloading file: \n{traceback.format_exc()}", 31
            )
        )
        exit_program(1)


def setup_server_environment(server_folder_path, server_file_path):
    os.chdir(server_folder_path)
    os.system(f"{server_file_path}")


min_memory, max_memory, use_aikar_flags, use_gui, server_folder_name, version_info = (
    prompt_user_for_configuration()
)
server_version, build_number = version_info
server_file_url = f"https://api.papermc.io/v2/projects/paper/versions/{server_version}/builds/{build_number}/downloads/paper-{server_version}-{build_number}.jar"
server_file_name = f"paper-{server_version}-{build_number}.jar"

os.mkdir(server_folder_name)
current_path = os.getcwd()
server_file_path = os.path.join(current_path, server_folder_name, server_file_name)
server_folder_path = os.path.join(current_path, server_folder_name)

print(get_colored_prompt(f"[+] Downloading server file: {server_file_name}...", 37))
download_file(server_file_url, server_file_path)
print(get_colored_prompt("[+] Successfully downloaded.", 37))

threading.Thread(
    target=setup_server_environment,
    args=(server_folder_path, server_file_path),
    daemon=True,
).start()

no_print = 0
while not os.path.exists("eula.txt"):
    if no_print == 0:
        print(get_colored_prompt("[+] setting basic server settings...", 37))
        no_print = 1

print(get_colored_prompt("[+] Successfully setted.", 37))
agree_EULA = input(get_colored_prompt("[?] Are you agree to mojang EULA? (y/n) : ", 37))

if agree_EULA == "y":
    agree_EULA = "true"
elif agree_EULA == "n":
    agree_EULA = "false"
    print(
        get_colored_prompt(
            "[-] Program is stopping because you did not accept the EULA.", 93
        )
    )
    exit_program(0)

with open(server_folder_path + "\\eula.txt", "r+") as file:
    true_eula = file.read().replace("false", "true")
    file.seek(0)
    file.truncate(0)
    file.write(true_eula)

print(get_colored_prompt("[+] saved eula.txt.", 37))

start_command = get_server_start_command(
    min_memory, max_memory, use_aikar_flags, use_gui, server_file_name
)
with open(server_folder_path + "\\start.bat", "w") as file:
    file.write(start_command)

print(get_colored_prompt("[+] saved start.bat.", 37))

run = input(get_colored_prompt("[?] Are you run your server right now? (y/n) : ", 37))

if run == "y":
    print(get_colored_prompt("[+] starting server...", 37))
    os.system(server_folder_path + "\\start.bat")
    print(get_colored_prompt("[+] server ended.", 37))
    exit_program(0)
elif run == "n":
    print(get_colored_prompt("[+] exiting...", 37))
    exit_program(0)
