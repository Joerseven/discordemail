#!/usr/bin/env python3
import time
import imaplib
import discord
import traceback

def requestEmailData():
    email_creds = {}
    email_creds["email_string"] = "j.d.hydon@gmail.com"
    email_creds["password_string"] = input("Please enter in your password: ")
    email_creds["server"] = "imap.google.com"
    email_creds["port"] = 993
    return email_creds

