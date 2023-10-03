import argparse
import configparser
import os
import re
import sys
import urllib.request
from time import sleep
from tkinter import filedialog, messagebox
from urllib.error import HTTPError

import yaml
from termcolor import colored
from tqdm import tqdm

COVERS_URL = "https://raw.githubusercontent.com/xlenore/ps2-covers/main/covers/"
VERSION = "2.0"


def set_console_title():
    if os.name == "nt":  # Windows
        os.system(f"title PS2CoverDL {VERSION}")
    else:  # Linux
        os.system(f"echo -ne '\\033]0;PS2CoverDL {VERSION}\\007'")


def get_config():
    config = configparser.ConfigParser()
    if os.path.exists("ps2coverdl.ini"):
        config.read("ps2coverdl.ini")
    return config


def save_config(config):
    with open("ps2coverdl.ini", "w") as configfile:
        config.write(configfile)
    messagebox.showinfo(
        "PS2CoverDL",
        "The configuration was completed.\n\nIn case you want to change the configuration, delete the ps2coverdl.ini file.",
    )


def get_pcsx2_file(config):
    pcsx2_file = config.get("Settings", "pcsx2_file", fallback=None)
    if pcsx2_file is None:
        pcsx2_file = filedialog.askopenfilename(
            title="Select the pcsx2-qtx64-avx2.exe file",
            filetypes=(
                ("Executable files", "pcsx2-qtx64-avx2.exe"),
                ("All files", "*.*"),
            ),
        )
        if pcsx2_file == "" or pcsx2_file is None:
            sys.exit(0)
        if not config.has_section("Settings"):
            config.add_section("Settings")
        config.set("Settings", "pcsx2_file", pcsx2_file)
    return pcsx2_file


def serial_list(games_file):
    gamelist_cache = os.path.join(
        os.path.dirname(games_file), "cache", "gamelist.cache"
    )
    if not os.path.exists(gamelist_cache):
        print(colored("[ERROR]: gamelist.cache file not found", "red"))
        input()
        sys.exit(1)
    with open(gamelist_cache, errors="ignore") as file:
        regex = re.findall(r"(\w{4}-\d{5})", file.read())
        serial_list = list(set(regex))
        print(colored(f"[LOG]: {len(serial_list)} games found", "green"))
        if not serial_list:
            print(colored("[ERROR]: No games found", "red"))
            input()
            sys.exit(1)
        return serial_list


def name_list(games_file):
    name_list = {}
    gameindex_file = os.path.join(
        os.path.dirname(games_file), "resources", "GameIndex.yaml"
    )
    if not os.path.exists(gameindex_file):
        print(colored("[ERROR]: GameIndex.yaml file not found", "red"))
        input()
        sys.exit(1)
    with open(gameindex_file, encoding="utf-8-sig") as file:
        name_list = {
            key: value["name"]
            for key, value in yaml.load(file, Loader=yaml.CBaseLoader).items()
        }
    return name_list


def existing_covers(covers_dir):
    covers = [
        w.replace(".jpg", "") for w in os.listdir(covers_dir) if w.endswith(".jpg")
    ]
    return covers


def serial_to_name(name_list, serial):
    return name_list.get(serial, None)


def download_covers(serial_list, name_list, covers_dir, use_ssl):
    if not os.path.exists(covers_dir):
        os.makedirs(covers_dir)
    existing_cover = existing_covers(covers_dir)
    for game_serial in tqdm(
        serial_list,
        desc="Downloading covers",
        unit="cover",
        ncols=50,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    ):
        game_name = serial_to_name(name_list, game_serial)
        if game_name is not None:
            if game_serial not in existing_cover:
                tqdm.write(colored(f"{game_serial} | {game_name}", "green"))
                try:
                    url = f"{COVERS_URL}{game_serial}.jpg"
                    if not use_ssl:
                        url = url.replace("https://", "http://")
                        urllib.request.ssl._create_default_https_context = (
                            urllib.request.ssl._create_unverified_context
                        )
                    urllib.request.urlretrieve(
                        url, os.path.join(covers_dir, f"{game_serial}.jpg")
                    )
                    sleep(0.1)
                except HTTPError:
                    tqdm.write(
                        colored(
                            f"[{game_serial} | {game_name}] not found. Skipping...",
                            "yellow",
                        )
                    )
            else:
                tqdm.write(
                    colored(
                        f"[{game_serial} | {game_name}] already exists. Skipping...",
                        "yellow",
                    )
                )


def run(games_file, covers_dir, use_ssl):
    download_covers(serial_list(games_file), name_list(games_file), covers_dir, use_ssl)
    print(
        colored(
            f"[LOG]: Done! Please report Not found | Low quality | Wrong covers on GitHub.",
            "green",
        )
    )
    input()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PS2CoverDL CLI")
    parser.add_argument(
        "-dir",
        help="Specify the directory where the pcsx2-qtx64-avx2.exe file is located",
    )
    parser.add_argument(
        "-use_ssl", action="store", default=None, help="Use SSL (https)"
    )
    args = parser.parse_args()
    if args.dir:
        games_file_dir = args.dir
        games_file = os.path.join(games_file_dir, "pcsx2-qtx64-avx2.exe")
        covers_dir = os.path.join(games_file_dir, "covers")
    else:
        set_console_title()
        config = get_config()
        games_file = get_pcsx2_file(config)
        covers_dir = os.path.join(os.path.dirname(games_file), "covers")
        use_ssl = config.getboolean("Settings", "use_ssl", fallback=False)
        if not config.has_option("Settings", "use_ssl"):
            result = messagebox.askyesno(
                "Use SSL",
                "Do you want to use SSL (https)?\n\nRecommended: Yes\n\nIn case you have problems with SSL, select No.",
            )
            use_ssl = result
            config.set("Settings", "use_ssl", str(use_ssl))
            save_config(config)
        
    use_ssl = args.use_ssl
    if use_ssl is None:
        use_ssl = True
    elif use_ssl.lower() == "false":
        use_ssl = False

    run(games_file, covers_dir, use_ssl)
