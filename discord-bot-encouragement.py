import os
import discord
import requests
import json
import random
from replit import db

from keep_alive import keep_alive


client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']
starter_encouragements = ["Cheer up!", "Hang in there.", "You are a great person / bot"]

if "res" not in db.keys():
  db["res"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '", - ' + json_data[0]['a']
  return quote

def update_encouragements(new_enc_message):
  if "enc" in db.keys():
    enc = db["enc"]
    enc.append(new_enc_message)
    db["enc"] = enc
  else:
    db["enc"] = [new_enc_message]


def delete_encouragement(index_num):
  enc = db["enc"]
  if len(enc) > index_num:
    del enc[index_num]
    db["enc"] = enc

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
  
    msg = message.content
  
    if msg.startswith('$hello'):
        await message.channel.send('Hello!')

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["res"]:
        enc_options = starter_encouragements
        if "enc" in db.keys():
            enc_options = enc_options + list(db["enc"])

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(enc_options))

    if msg.startswith("$new"):
        enc_msg = msg.split("$new ", 1)[1]
        update_encouragements(enc_msg)
        await message.channel.send("New encouragement message added.")

    if msg.startswith("$del"):
        enc = []
        if "enc" in db.keys():
            index_num = int(msg.split("$del", 1)[1])
            delete_encouragement(index_num)
            enc = db["enc"]
        
        await message.channel.send(list(enc))

    if msg.startswith("$list"):
        enc = []
        if "enc" in db.keys():
            enc = list(db["enc"])
        
        await message.channel.send(enc)

    if msg.startswith("$res"):
        value = msg.split("$res ", 1)[1]

        if value.lower() == "true":
            db["res"] = True
            await message.channel.send("Responding is ON.")
        else:
            db["res"] = False
            await message.channel.send("Responding is OFF.")

token = os.environ['TOKEN']

keep_alive()
client.run(token)
