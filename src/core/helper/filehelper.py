import os
import traceback
import zipfile

from requests import get

from core.helper.prompt import promptType
from main import wait_and_exit, main_logger


class fileHelper:
    def __init__(self):
        pass

    def get_cwd(self):
        return os.getcwd()

    def ch_dir(self, path):
        os.chdir(path)

    def download_file(self, url, filename, path):
        try:
            response = get(url)
            with open(path + "\\" + filename, "wb") as file:
                file.write(response.content)
            return 0
        except Exception as ex:
            main_logger.log(
                f"ERROR downloading file: \n{traceback.format_exc()}", promptType.ERROR
            )
            wait_and_exit(3)

    def read_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            file.read()

    def make_file(self, filename, path, data):
        with open(f"{path}/{filename}", "w") as file:
            file.write(data)
        return 0

    def make_dir(self, dirname, path):
        os.mkdir(path + "\\" + dirname)
        return 0

    def read_dir(self, dirname):
        return os.listdir(dirname)
    
    def unzip_to_folder(zip_path, server_folder):
        # 현재 디렉토리에 'java22' 폴더 생성
        target_folder = os.path.join(server_folder, 'java22')
        os.mkdir(target_folder)
        
        # zip 파일 열기
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 압축 해제
            zip_ref.extractall(target_folder)

