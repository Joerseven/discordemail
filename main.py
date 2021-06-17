#!/usr/bin/env python3
import os
import imaplib
import discord
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

class Emaillogin:
    def __init__(self):
        pass

def gmailAuthentication():
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
	results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
	

gmailAuthentication()
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
