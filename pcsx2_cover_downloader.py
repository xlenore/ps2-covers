"""
⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀

     NO COVERS?
"""


from msilib.schema import Directory
import re
from time import sleep
from urllib.error import HTTPError
from termcolor import colored
from colorama import init
import urllib.request
import yaml
import os, sys


COVERS_URL = 'https://github.com/LouiseSulyvahn/PCSX2_Cover_Downloader/raw/main/covers/'
VERSION_URL = 'https://raw.githubusercontent.com/LouiseSulyvahn/PCSX2_Cover_Downloader/main/version'
VERSION = 1.4


def path():
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(os.path.realpath(sys.executable))
    elif __file__:
        path = os.path.dirname(__file__)
    return path


def check_version():
    try:
        version = urllib.request.urlopen(VERSION_URL)
        if float(version.read().decode('utf-8').replace('\n','')) != VERSION:
            print('[LOG]:', colored(f'New update available!\n', 'green'))
    except:
        pass


def serial_list():  # Get game serial
    with open(f'{path()}\cache\gamelist.cache', errors='ignore') as file:
        regex = re.compile('(\w{4}-\d{5})').findall(file.read())
        serial_list = list(dict.fromkeys(regex))
        print('[LOG]:', colored(f'Found {len(serial_list)} games', 'green'))
        if len(serial_list) == 0:
            print('[ERROR]:', colored(f'You have 0 games installed', 'red'))
            input()
            quit()
        return serial_list


def name_list():  # Get game name
    name_list = {}
    with open(f'{path()}\/resources\GameIndex.yaml', encoding='utf-8-sig') as file:
        for key, value in yaml.load(file, Loader=yaml.CBaseLoader).items():
            name_list[key] = value["name"]
    return name_list


def existing_covers():
    covers = [w.replace('.jpg', '') for w in os.listdir(f'{path()}\covers')]
    return covers


def serial_to_name(name_list, serial:str):  # Get game name using serial
    try:
        return name_list[serial]
    except KeyError:
        print('[WARNING]:', colored(f'{serial} Not found. Skipping...', 'yellow'))
        return None


def download_covers(serial_list:list, name_list):  # Download Covers
    if os.path.exists(f'{path()}\covers') == False:
        os.makedirs(f'{path()}\covers')
    existing_cover = existing_covers()
    for i in range(len(serial_list)):
        game_serial = serial_list[i]
        game_name = serial_to_name(name_list, game_serial)
        if game_name != None:
            if game_serial not in existing_cover:
                print('[LOG]:', colored(f'Downloading {game_serial} | {game_name} cover...', 'green'))
                try:
                    urllib.request.urlretrieve(f'{COVERS_URL}{game_serial}.jpg', f'covers/{game_serial}.jpg')
                    sleep(1)
                except HTTPError:
                    print('[WARNING]:', colored(f'{game_serial} | {game_name} Not found. Skipping...', 'yellow'))
            else:
                print('[WARNING]:', colored(f'{game_serial} | {game_name} already exist in /covers. Skipping...', 'yellow'))


def run():
    check_version()
    download_covers(serial_list(), name_list())
    print('[LOG]:', colored(f'Done!, please report Not found | Low quality | Wrong covers in GitHub.', 'green'))
    input()


os.system(f'title PCSX2 Cover Downloader {VERSION}')
init()
run()