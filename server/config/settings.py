import os

HOST = '127.0.0.1'
PORT = 8080


file = os.path.dirname(os.path.dirname(__file__))
DB_FILE_PATH = os.path.join(file,'db','user.xlsx')
USER_FOLDER_DIR = os.path.join(file,'Fiels')