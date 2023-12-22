import os
from dotenv import dotenv_values
config = dotenv_values('.env')
SERVER = config['SERVER']
DATABASE = config['DATABASE']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']

SOURCE_FOLDER = os.getcwd()+'\source'

SENDER = config["SENDER"] 
RECIEVER = config["RECIEVER"]
E_PASSWORD = config["E_PASSWORD"]