#!/usr/bin/python

import time
import requests
import sys

if (len(sys.argv) < 2):
    print("Usage:")
    print("  slap.py <bot_token>")
    exit(1)

botapi_url = 'https://api.telegram.org/bot'
token = sys.argv[1]
endpoint = botapi_url + token
offset = 0
print(time.ctime(), ': bot started')
while(True):
    try:
        method = 'getUpdates'
        request = endpoint + '/' + method
        query = {'offset': offset}
        response = requests.get(request, params=query)
        json = response.json()
        if (json['result']):
            result = json['result']
            for update in result:
                if 'message' in update:
                    message = update['message']
                    if 'text' in message:
                        text = message['text']
                        spl = text.split(' ')
                        chat_id = message['chat']['id']
                        command = spl[0]
                        msg_text = ''
                        if (command[:6] == '/start'):
                            msg_text = 'Slap someone with a wet trout using /slap username'
                        elif (command[:5] == '/slap'):
                            user_from = ''
                            if 'username' in message['from']:
                                user_from = '@' + message['from']['username']
                            else:
                                user_from = message['from']['first_name']
                            msg_text += user_from + ' slaps '
                            if (len(spl) == 1):
                                msg_text += 'himself'
                            else:
                                user_slap = spl[1]
                                if user_slap[0] != '@':
                                    msg_text += '@'
                                msg_text += user_slap
                            msg_text += ' around a bit with a large trout'
                        else:
                            continue
                        method_resp = 'sendMessage'
                        query_resp = {'chat_id': chat_id, 'text': msg_text}
                        requests.get(endpoint + '/' + method_resp, params=query_resp)
                # move offset
                offset = int(update['update_id']) + 1
        # print json
        time.sleep(1)
    except ValueError:
        print(time.ctime(), ": Broken response: ", response)
        time.sleep(60)
    except KeyboardInterrupt:
        print(time.ctime(), ": Ctrl-C pressed - exiting")
        exit(1)
    except:
        print(time.ctime(), ": Unexpected error", sys.exc_info()[0])
        time.sleep(300)
