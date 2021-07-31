from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import os
from telethon.tl.types import UserStatusLastWeek
api_id = 2429786

api_hash = '992cd4665a7b141dc5c9a340b58b9b4d'

session_name = 'Testsaja'
print(f"[*] Automation Scraping Member Group Telegram!\n[*] Author: RJD")
target = input(f"[*] Input Link/@ Group (example: @defiandmore): ")

try:
    client = TelegramClient(str(session_name), api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        phone = input(f"[*] Input Number (example: +6213232323232): ")
        client.send_code_request(phone)
        client.sign_in(phone, input('[*] Enter the code: '))

    print('[*] Fetching Members...')
    all_participants = []
    cwd = os.getcwd()
    try:

        all_participants = client.get_participants(target, aggressive=True)

        print('[*] Saving In file...')
        with open(f"{cwd}/{target}.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['sr. no.','username', 'user id', 'name', 'group', 'group id'])
            i = 0
            for user in all_participants:
                accept = True
                if not user.status == UserStatusRecently():
                    accept = False
                if accept:
                    i += 1
                    if user.username:
                        username = user.username
                    else:
                        username = ""
                    if user.first_name:
                        first_name = user.first_name
                    else:
                        first_name = ""
                    if user.last_name:
                        last_name = user.last_name
                    else:
                        last_name = ""
                    name = (first_name + ' ' + last_name).strip()
                    writer.writerow([i,username, user.id, name, 'group name', 'groupid'])
        print(f'[*] Members scraped successfully.\n[*] Saved to {target}.csv')
    except Exception as e:
        print(f"[*] Eror Second: {e}")
except Exception as e:
    print(f"[*] Eror First: {e}")
