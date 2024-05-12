import os
from core.errors.error import notExistError
from core.helper.file_helper import fileHelper
from core.helper.prompt_helper import promptHelper, promptType
from core.signature.sign import lim
from core.utils.utils import str_to_bool


def set_props() :
    exist_bat = os.path.exists("server.properties")
    if not exist_bat :
        raise notExistError
    
    with open("server.properties", "r", encoding="utf-8") as file :
        data = file.read()
    
    filehelper = fileHelper()

    main_logger = promptHelper("log_format.json")
    main_logger.load_config()

    lim()

    used_setting = str_to_bool(main_logger.log("Do you want to change only frequently used settings? (y/n)", promptType.QUESTION))
    if used_setting :
        difficulty = main_logger.log("Difficulty (peaceful | easy | normal | hard)", promptType.QUESTION)
        enable_command_block = str_to_bool(main_logger.log("Enable command block? (y/n)", promptType.QUESTION))
        gamemode = main_logger.log("gamemode (survival | creative | adventure | spector)", promptType.QUESTION)
        enable_hardcore = str_to_bool(main_logger.log("Enable hardcore? (WARN : difficulty will be fixed to hard!) (y/n)", promptType.QUESTION))
        max_players = main_logger.log("max players (integer)", promptType.QUESTION)
        motd = main_logger.log("motd", promptType.QUESTION)
        pvp = str_to_bool(main_logger.log("Enable pvp? (y/n)", promptType.QUESTION))

        data = data.replace("difficulty=easy", f"difficulty={difficulty}")
        data = data.replace("enable-command-block=false", f"enable-command-block={str(enable_command_block).lower()}")
        data = data.replace("gamemode=survival", f"gamemode={gamemode}")
        data = data.replace("hardcore=false", f"hardcore={str(enable_hardcore).lower()}")
        data = data.replace("max-players=20", f"max-players={max_players}")
        data = data.replace("motd=A Minecraft Server", f"motd={motd}")
        data = data.replace("pvp=true", f"pvp={str(pvp).lower()}")

        with open("server.properties", "w+") as file :
            file.write(data)
        
        main_logger.log("Successfully setted.")
        