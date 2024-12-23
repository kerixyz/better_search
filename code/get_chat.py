import pandas as pd
import datetime
import os
from dotenv import load_dotenv
import socket
import logging
from emoji import demojize

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')
token = os.getenv('TWITCH_ACCESS_TOKEN')

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'kehree'
channel = '#kehree'

sock = socket.socket()

sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

from emoji import demojize

while True:
    resp = sock.recv(2048).decode('utf-8')
    print(resp)

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    
    elif len(resp) > 0:
        logging.info(demojize(resp))


# resp = sock.recv(2048).decode('utf-8')

# print(resp)

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s — %(message)s',
#                     datefmt='%Y-%m-%d_%H:%M:%S',
#                     handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

# logging.info(resp)