from sys import platform

if platform == 'linux':
  import asyncio

  import uvloop
  asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from os import environ

from dotenv import load_dotenv
load_dotenv('.env')
from pyrogram import Client
from db import database


app = Client(
  name = 'torjoman-telegram',
  api_id = int(environ.get('API_ID')),
  api_hash = environ.get('API_HASH'),
  bot_token = environ.get('BOT_TOKEN'),
  plugins = {
    "root": "plugins"
  },
)
app.torjoman = environ.get("TORJOMAN_BASE_URL")
app.run(database.connect())
app.run()
app.run(database.disconnect())
