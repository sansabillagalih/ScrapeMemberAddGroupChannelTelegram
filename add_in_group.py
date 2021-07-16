from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
from time import sleep
import random
import os
cwd = os.getcwd()
api_id = 2429786
api_hash = '992cd4665a7b141dc5c9a340b58b9b4d'
 

session_name = ''


try:
    client = TelegramClient(str(session_name), api_id, api_hash)
    print(f"[*] Automation Adding Member Group Telegram!\n[*] Author: RJD")
    client.connect()
    if not client.is_user_authorized():
        phone = input("[*] Phone Number (example: +6281364445559):")
        client.send_code_request(phone)
        client.sign_in(phone, input('[*] Enter the code: '))
        target = input("[*] File Name CSV Target: ")
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

            chats = []
            last_date = None
            chunk_size = 200
            groups = []

            result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash=0
            ))
            chats.extend(result.chats)

            for chat in chats:
                try:
                    if chat.megagroup == True:
                        groups.append(chat)
                except:
                    continue
            delay = input('[*] Input Delay Add User: ')
            print('[*] Choose a group to add members:')
            
            delay = int(delay)
            i = 0
            for group in groups:
                print('[*] ' + str(i) + '. ' + group.title)
                i += 1

            g_index = input("[*] Enter a Number: ")
            target_group = groups[int(g_index)]

            target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

            mode = int(input("[*] Enter 1 to add by username or 2 to add by ID: "))

            startfrom = int(input("[*] Start From = "))
            endto = int(input("[*] End To = "))

            n = 0

            for user in users:
                
                if (int(startfrom) <= int(user['srno'])) and (int(user['srno']) <= int(endto)):
                    n += 1
                    if n % 50 == 0:
                        sleep(900)
                        quit()
                    try:
                        print("[*] Adding {}".format(user['id']))
                        if mode == 1:
                            if user['username'] == "":
                                continue
                            user_to_add = client.get_input_entity(user['username'])
                        elif mode == 2:
                            user_to_add = InputPeerUser(user['id'], user['access_hash'])
                        else:
                            sys.exit("Invalid Mode Selected. Please Try Again.")
                        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                        print(f"[*] Waiting for {delay} Seconds...")
                        sleep(delay)
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
            print(f"[*] Eror Second: {e}")

except Exception as e:
    print(f"[*] Eror First: {e}")
