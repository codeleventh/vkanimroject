import vk
import time
import json
import sys

LOGIN = 'durov@vk.com'
PASSWORD = 'qwerty'
APP_ID = '1234567'

SHORTPAUSE = 2
LONGPAUSE = 4
MINSPEED = 0.35  # при меньших значениях ловишь бан мгновенно

# args: py vk.py id speed file
# example: py vk.py 1 0.75 skinhands.json

v = '5.38'  # ¯\_(ツ)_/¯
session = vk.AuthSession(APP_ID, LOGIN, PASSWORD, scope='messages')
vk_api = vk.API(session)

try:
    arg_id = sys.argv[1]
    arg_framedelay = float(sys.argv[2])
    arg_file = sys.argv[3]
    arg_framedelay = max(arg_framedelay, MINSPEED)
    print("Args parsed.")
except (IndexError, TypeError, FileNotFoundError, ValueError) as e:
    print("Error. Wrong args: {}.".format(e.args[-1]))
    exit()
try:
    data = open(arg_file, encoding="utf8").read()
    data = json.loads(data)
    print("Reading {} is done.".format(arg_file))
except (FileExistsError, FileNotFoundError, ValueError) as e:
    print("Error. bad JSON file: {}.".format(e.args[-1]))
    exit()
try:
    data['frames']
except (KeyError) as e:
    print("Error. There is no frames in JSON file.")
    exit()

data_def = {
    "before": "",
    "after": "",
    "cycles": 1,
    "ping_pong_animation": False,
    "delete_after_end": False,
}
data_def.update(data)
data = data_def

print("Data: {}.".format(data))

if data['before'] == "":
    fstmsg = data['frames'][0]
else:
    fstmsg = data['before']

try:
    message_id = vk_api.messages.send(peer_id=arg_id, message=fstmsg, v=v)
    print("MSG SEND is OK, the message id is {}".format(message_id))
    time.sleep(SHORTPAUSE)

    while True:
        message = vk_api.messages.getById(
            message_id=message_id, preview_length=0, v=v)
    #     # обработка на баны и ошибки здесь
        is_read = message['items'][0]['read_state']
        if(is_read == 1):
            print("User has read the MSG")
            break
        time.sleep(LONGPAUSE)

    while (data['cycles'] > 0):
        for i in range(len(data['frames'])):
            time.sleep(arg_framedelay)
            response = vk_api.messages.edit(
                peer_id=arg_id, message=data['frames'][i], message_id=message_id, v=v)
            print("frame №{}".format(i))
            # check_response()

        if data['ping_pong_animation'] == True:
            print("vice versa: ")
            for i in range(len(data['frames'])-2, 0, -1):
                time.sleep(arg_framedelay)
                response = vk_api.messages.edit(
                    peer_id=arg_id, message=data['frames'][i], message_id=message_id, v=v)
                print("frame №{}".format(i))
                # check_response()
        data['cycles'] -= 1

    if data["after"] != "":
        time.sleep(arg_framedelay)
        response = vk_api.messages.edit(
            peer_id=arg_id, message=data["after"], message_id=message_id, v=v)

    if data["delete_after_end"] == True:
        time.sleep(SHORTPAUSE)
        response = vk_api.messages.delete(
            message_ids=[message_id], spam=0, delete_for_all=1, v=v)
        if response == 1:
            print("MSG deleted.")
except(vk.exceptions.VkAPIError) as e:
    print("💀  VkAPIError: {}.".format(e))
    exit()

print("Done.")
