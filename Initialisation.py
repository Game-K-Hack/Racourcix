import os

NAME_OF_DIR = "Liens Internet"
PROGRAM_DIR = fr"C:\Users\{os.environ['username']}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
BASE_DIR = PROGRAM_DIR + "\\" + NAME_OF_DIR

if NAME_OF_DIR not in os.listdir(PROGRAM_DIR):
    os.mkdir(BASE_DIR)

if ".icon" not in os.listdir(BASE_DIR):
    os.mkdir(BASE_DIR + "\\" + ".icon")

if ".script" not in os.listdir(BASE_DIR):
    os.mkdir(BASE_DIR + "\\" + ".script")
