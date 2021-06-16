#!/usr/bin/env python3
import os
import imaplib
import discord
from dotenv import load_dotenv

class Emaillogin:
    def __init__(self):
        pass

client = discord.Client()

@client.event
async def on_ready():
    print("Bot has been initialised")

async def post_email_data(ctx, member: discord.Member, *, content):
    channel = member.create_dm()
    await channel.send(content)

load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
