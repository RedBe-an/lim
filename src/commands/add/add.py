import os
from core.helper.file_helper import fileHelper
from core.helper.prompt_helper import promptHelper
from core.signature.sign import lim


def add(arg) :
    lim()

    filehelper = fileHelper()

    main_logger = promptHelper("D:\\Proj\\AutoPaper\\AutoPaper\\src\\config\\log_format.json")
    main_logger.load_config()

    main_logger.log(f"adding plugin : {arg} -> {filehelper.get_cwd()}\\{os.path.basename(arg)}")
    filehelper.move_file(arg, filehelper.get_cwd() + "\\" + "plugins", os.path.basename(arg))
    main_logger.log("succeed.")