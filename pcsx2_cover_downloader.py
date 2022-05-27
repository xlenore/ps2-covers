from logging import exception
import re
from time import sleep
from urllib.error import HTTPError
from termcolor import colored
from colorama import init
import urllib.request
import json
import os, sys

COVERS_URL = "https://github.com/LouiseSulyvahn/PCSX2_Cover_Downloader/raw/main/covers/"

def serial_list(): #Get game serial
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(os.path.realpath(sys.executable))
    elif __file__:
        path = os.path.dirname(__file__)
    with open(f'{path}\cache\gamelist.cache', encoding='ansi') as file:
        regex = re.compile('(\w{4}-\d{5})').findall(file.read())
        serial_list = list(dict.fromkeys(regex))
        print('[LOG]:',colored(f'Found {len(serial_list)} games','green'))
        if len(serial_list) == 0:
            print('[ERROR]:',colored(f'You have 0 games installed','yellow'))
            input()
            quit()
        return serial_list

def serial_to_name(serial:str): #Get game name using serial
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(os.path.realpath(sys.executable))
    elif __file__:
        path = os.path.dirname(__file__)    
    with open(f'{path}\GameIndex.json', encoding='utf-8-sig') as file:
        try:
            json_data = json.loads(file.read())
            name = json_data[serial]["name"]
            return name
        except KeyError:
            print('[ERROR]:',colored(f'{serial} Not found. Skipping...','yellow'))
            return None
             
def download_covers(serial_list): #Download Covers
        for i in range(len(serial_list)):
            game_serial = serial_list[i]
            game_name = serial_to_name(serial_list[i])
            if game_name != None:
                print('[LOG]:',colored(f'Downloading {game_serial} | {game_name} cover...','green'))
                try:
                    urllib.request.urlretrieve(f'{COVERS_URL}{game_serial}.jpg', f'covers/{game_name}.jpg')
                    sleep(3)
                except HTTPError:
                    print('[ERROR]:',colored(f'{game_serial} | {game_name} Not found. Report it in GitHub please...','yellow'))
                    
                      
def run():
        download_covers(serial_list())
        print('[LOG]:',colored(f'Done!','green'))
        input()

init()    
run()