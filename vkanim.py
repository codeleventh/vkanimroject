import vk
import time
import json
import sys

LOGIN = 'durov@vk.com'
PASSWORD = 'qwerty'
APP_ID = '1234567'

SHORTPAUSE = 2
LONGPAUSE = 4
MINSPEED = 0.35  # сразу же ловишь бан при меньших значениях

# args: py vk.py id1 [speed] hands.json

v = '5.23'  # ¯\_(ツ)_/¯
session = vk.AuthSession(APP_ID, LOGIN, PASSWORD, scope='messages')
vk_api = vk.API(session)

arg_id = sys.argv[1]
arg_framedelay = float(sys.argv[2])
arg_file = sys.argv[3]

print(sys.argv)

data = open(arg_file, encoding="utf8").read()
data = json.loads(data)
print("Reading {} is done".format(arg_file))

arg_framedelay = max(arg_framedelay, MINSPEED)

# - - -

message_id = vk_api.messages.send(
    user_id=arg_id, message='смотри внимательно', v=v)
print("MSG SEND is OK, the message id is {}".format(message_id))
time.sleep(SHORTPAUSE)
while True:
    message = vk_api.messages.getById(
        message_id=message_id, preview_length=0, v=v)
#     # обработка на баны и ошибки здесь
    is_read = message['items'][0]['read_state']
    print("Read state: {0:b}".format(is_read))
    if(is_read == 1):
        break
    time.sleep(LONGPAUSE)

while (data['cycles'] > 0):
    for i in range(len(data['frames'])):
        time.sleep(arg_framedelay)
        response = vk_api.messages.edit(
            peer_id=arg_id, message=data['frames'][i], message_id=message_id, v=v)
        print(i)
        # check_response()

    if data['ping_pong_animation'] == True:
        for i in range(len(data['frames'])-2, 0, -1):
            time.sleep(arg_framedelay)
            response = vk_api.messages.edit(
                peer_id=arg_id, message=data['frames'][i], message_id=message_id, v=v)
            print(i)
            # check_response()
    data['cycles'] -= 1
print("Done.")
