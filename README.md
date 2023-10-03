*⭐**Star this repo if it was useful to you**⭐*
⚠️**Please report Not found | Low quality | Wrong covers**⚠️

- [PS2 Covers](https://github.com/xlenore/ps2-covers#ps2-covers  "PS2 Covers")
- [PCSX2 Setup](https://github.com/xlenore/ps2-covers#pcsx2-setup  "PCSX2 Setup")
- [PS2CoverDL App](https://github.com/xlenore/ps2-covers#PS2CoverDL)

| Serial | Available/Total | Percentage |
| ------ | --------------- | ---------- |
| ALCH | 16/16 | 100.00% |
| CPCS | 2/2 | 100.00% |
| GUST | 1/1 | 100.00% |
| PAPX | 12/13 | 92.31% |
| PBGP | 3/3 | 100.00% |
| PBPX | 29/35 | 82.86% |
| PCPX | 6/12 | 50.00% |
| PDPX | 1/1 | 100.00% |
| PKP2 | 1/1 | 100.00% |
| SCAJ | 160/213 | 75.12% |
| SCCS | 12/18 | 66.67% |
| SCED | 8/304 | 2.63% |
| SCES | 380/455 | 83.52% |
| SCKA | 65/92 | 70.65% |
| SCPM | 2/2 | 100.00% |
| SCPN | 7/7 | 100.00% |
| SCPS | 238/291 | 81.79% |
| SCUS | 207/397 | 52.14% |
| SLAJ | 43/63 | 68.25% |
| SLED | 3/52 | 5.77% |
| SLES | 2911/3069 | 94.85% |
| SLKA | 168/261 | 64.37% |
| SLPM | 2456/2728 | 90.03% |
| SLPS | 1136/1288 | 88.20% |
| SLUS | 1737/1944 | 89.35% |
| TCES | 2/12 | 16.67% |
| TCPS | 19/36 | 52.78% |
| TLES | 2/8 | 25.00% |
| VW067 | 2/2 | 100.00% |

## PCSX2 setup
PCSX2 has its own cover downloader, upgrade to version **v1.7.3329** or higher.
- Open PCSX2
- Tools -> Cover Downloader...
- Use this url `https://raw.githubusercontent.com/xlenore/ps2-covers/main/covers/${serial}.jpg`
- Check "Use Serial Files Name"
- Click Start
- Enjoy :)

[![](https://i.imgur.com/jTGL0HH.gif)](https://i.imgur.com/jTGL0HH.gif)

## PS2CoverDL
PS2CoverDL is a command-line tool that automatically downloads PlayStation 2 (PS2) game covers for the PCSX2 emulator.

**.Exe instructions:**
- Download [PS2CoverDL.exe](https://github.com/xlenore/ps2-covers/raw/main/ps2coverdl/ps2coverdl.exe) | ([Source Code](https://raw.githubusercontent.com/xlenore/ps2-covers/main/ps2coverdl/ps2coverdl.py))
- Run **PS2CoverDL.exe**
- Search and select **pcsx2-qtx64-avx2.exe**
- Select whether you want to use SSL or not.

The configurations will be saved in **ps2coverdl.ini** file, which will be located in the same directory as the .exe file.

**.Py (CLI) instructions:**
- Download [PS2CoverDL.py](https://github.com/xlenore/ps2-covers/raw/main/ps2coverdl/ps2coverdl.py)
```console
python ps2coverdl.py -dir /path/ -use_ssl true

#-dir: Specifies the directory where the `pcsx2-qtx64-avx2.exe` file is located. This argument allows you to provide a custom directory path instead of using the default directory.
#-use_ssl (optional): Specifies whether to use SSL (https)or not. By default, the value is set to `True` . If you want to disable SSL, you can set this argument to `false` .
```

[![](https://i.imgur.com/C8obFzK.png)](https://i.imgur.com/C8obFzK.png)

## Credits
* pcsx2.net
* psxdatacenter.com
* gvcover.top
* imkira3
* waifu2x