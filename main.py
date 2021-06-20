#!/usr/bin/env python3
import os
import imaplib
import discord
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from time import sleep

client = discord.Client()
load_dotenv()
TOKEN = os.getenv("TOKEN")

async def gmail_authentication():
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
    print("Connection with GmailAPI established")
    return service

async def post_email(contents):
    user = await client.fetch_user('778676909311393794')
    email_post = discord.Embed(title=contents['title'], description=contents['description'], color=0xff0000)
    email_post.add_field(name="Author", value=contents['sender'])
    channel = await user.create_dm()
    await channel.send(embed=email_post)

async def fetch_email(service, date):
    results = service.users().messages().list(userId='me',labelIds=['IMPORTANT','UNREAD']).execute()
    messages = results.get('messages', [])
    new_date = date
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        if int(msg['internalDate']) > date:
            header_list = msg['payload']['headers'] 
            email_author = next(header for header in header_list if header["name"] == "From")['value']
            await post_email({
                'title': "New Email",
                'sender': email_author,
                'description': msg['snippet']
            })
            newdate = int(msg['internalDate'])
    return newdate

@client.event
async def on_ready():
    print("Bot has been initialised")
    gmailapi = await gmail_authentication() 
    new_date = await fetch_email(gmailapi, 1623785486)

if __name__ == "__main__":
    client.run(TOKEN)
