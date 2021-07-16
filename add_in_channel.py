from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import os
cwd = os.getcwd()
api_id = 2429786
api_hash = '992cd4665a7b141dc5c9a340b58b9b4d'
print(f"[*] Automation Add Member Channel Telegram!\n[*] Author: RJD")
session_name = ''
channel_username = input(f"[*] Input Channel Username (example: @channeluser): ")
try:
    client = TelegramClient(str(session_name), api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        phone = input(f"[*] Input Number (example: +6213232323232): ")
        client.send_code_request(phone)
        
        client.sign_in(phone, input('[*] Enter the code: '))
        target = input("[*] File Name CSV Target: ")
        delay = input("[*] Delay Add per User: ")
        delay = int(delay)
    try:
        input_file = f'{cwd}/{target}'
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['srno'] = row[0]
                user['username'] = row[1]
                user['id'] = int(row[2])
                #user['access_hash'] = int(row[2])
                user['name'] = row[4]
                users.append(user)

        startfrom = int(input("[*] Start From = "))
        endto = int(input("[*] End To = "))

        n = 0

        for user in users:
            if (int(startfrom) <= int(user['srno'])) and (int(user['srno']) <= int(endto)):
                n += 1
                if n % 50 == 0:
                    time.sleep(900)
                    quit()
                try:
                    print("[*] Adding {}".format(user['id']))

                    if user['username'] == "":
                        print("[*] No username, moving to next")
                        continue
                    
                    client(InviteToChannelRequest(
                        channel_username,
                        [user['username']]
                    ))
                    
                    print(f"[*] Waiting for {delay} Seconds...")
                    time.sleep(delay)
                except PeerFloodError:
                    print("[*] Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                    quit()
                except UserPrivacyRestrictedError:
                    print("[*] The user's privacy settings do not allow you to do this. Skipping.")
                except:
                    traceback.print_exc()
                    print("[*] Unexpected Error")
                    continue
            elif int(user['srno']) > int(endto):
                print("[*] Members added successfully")
                break
    except Exception as e:
        print(f'[*] Eror Second: {e}')
except Exception as e:
    print(f'[*] Eror First: {e}')
