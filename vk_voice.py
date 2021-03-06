""" Vk API for send voices

For work on mobile devices, the audio file format must be monaural.
"""

import vk_requests # Only >= 1.2.0, see https://github.com/prawn-cake/vk-requests/issues/37
import json
import requests
import random

_CLIENT_ID = "2274003"                  # VK for Android app client_id
_CLIENT_SECRET = "hHbZxrka2uZ6jB1inYsH" # VK for Android app client_secret
#_CLIENT_ID = "3697615"                  # VK for Windows app client_id
#_CLIENT_SECRET = "AlVXZFMUqyrnABp8ncuU" # VK for Windows app client_secret
#_CLIENT_ID = "3140623"                  # VK for iPhone app client_id
#_CLIENT_SECRET = "VeWdmVclDCtn6ihuP1nt" # VK for iPhone app client_secret

_MAX_INT = 2**31-1

def _make_peer_id(user_id, is_chat):
    return 2000000000 + int(user_id) if is_chat else user_id

def _make_random_id():
    return random.randint(0, _MAX_INT)

def send(login, password, voice_input, user_id, is_chat=False):
    api = vk_requests.create_api(app_id=_CLIENT_ID,
                                 client_secret=_CLIENT_SECRET,
                                 login=login, password=password,
                                 scope=['messages' 'docs'])
    upload_url = api.docs.getMessagesUploadServer(type='audio_message', peer_id=_make_peer_id(user_id, is_chat))['upload_url']

    response = requests.post(upload_url, files=dict(file=voice_input))
    response.raise_for_status()

    response_file = json.loads(response.text)['file']
    doc_response = api.docs.save(file=response_file)

    message = {'attachment': 'doc{0}_{1}'.format(doc_response['audio_message']['owner_id'], doc_response['audio_message']['id']),
	       'random_id': _make_random_id()}
    if is_chat:
        message['chat_id'] = user_id
    else:
        message['user_id'] = user_id
    api.messages.send(**message)
