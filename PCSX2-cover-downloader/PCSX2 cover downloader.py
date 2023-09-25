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


import os
import re
import sys
import urllib.request
from time import sleep
from urllib.error import HTTPError
from pathlib import Path

import yaml
from colorama import init
from termcolor import colored

COVERS_URL = 'https://raw.githubusercontent.com/xlenore/ps2-covers/main/covers/'
VERSION_URL = 'https://raw.githubusercontent.com/LouiseSulyvahn/PCSX2_Cover_Downloader/main/version'
VERSION = 1.5


def path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    if __file__:
        return Path(__file__).parent


def check_version():
    try:
        version = urllib.request.urlopen(VERSION_URL)
        if float(version.read().decode('utf-8').replace('\n','')) != VERSION:
            print('[LOG]:', colored('New update available!\n', 'green'))
    except:
        pass


def serial_list():  # Get game serial
    with open(path() / 'cache' / 'gamelist.cache', errors='ignore') as file:
        regex = re.compile('(\w{4}-\d{5})').findall(file.read())
        serial_list = list(dict.fromkeys(regex))
        print('[LOG]:', colored(f'Found {len(serial_list)} games', 'green'))
        if len(serial_list) == 0:
            print('[ERROR]:', colored('You have 0 games installed', 'red'))
            input()
            quit()
        return serial_list


def name_list():  # Get game name
    name_list = {}
    with open(path() / 'resources' / 'GameIndex.yaml', encoding='utf-8-sig') as file:
        for key, value in yaml.load(file, Loader=yaml.CBaseLoader).items():
            name_list[key] = value["name"]
    return name_list


def serial_to_name(name_list, serial: str):  # Get game name using serial
    try:
        return name_list[serial]
    except KeyError:
        print('[WARNING]:', colored(f'{serial} Not found. Skipping...', 'yellow'))
        return None


def download_covers(serial_list: list, name_list):  # Download Covers
    cover_folder = path() / 'covers'
    if not cover_folder.exists():
        cover_folder.mkdir()
    existing_cover = [w.stem for w in cover_folder.iterdir()]
    for i in range(len(serial_list)):
        game_serial = serial_list[i]
        game_name = serial_to_name(name_list, game_serial)
        if game_name is not None:
            if game_serial not in existing_cover:
                print('[LOG]:', colored(
                    f'Downloading {game_serial} | {game_name} cover...',
                    'green'))
                try:
                    urllib.request.urlretrieve(
                        f'{COVERS_URL}{game_serial}.jpg',
                        cover_folder / f'{game_serial}.jpg')
                    sleep(0.1)
                except HTTPError:
                    print('[WARNING]:', colored(
                        f'{game_serial} | {game_name} Not found. Skipping...',
                        'yellow'))
            else:
                print('[WARNING]:', colored(
                    f'{game_serial} | {game_name} already exist in /covers. Skipping...',
                    'yellow'))


def run():
    #check_version()
    download_covers(serial_list(), name_list())
    print('[LOG]:', colored(
        'Done!, please report Not found | Low quality | Wrong covers in GitHub.',
        'green'))
    input()


os.system(f'title PCSX2 Cover Downloader {VERSION}')
init()
run()
