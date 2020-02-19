#!/usr/bin/env python3
from playhouse.db_url import connect
import os
import argparse
import getpass
from app import config
from app.models import User
import bcrypt
database = connect(config.DATABASE)

parser = argparse.ArgumentParser(description='Creates a new user.')
parser.add_argument('-u', '--user', metavar='NAME', help='Username', required=True)
parser.add_argument('-e', '--email', metavar='NAME', help='Email', required=True)

args = parser.parse_args()
password = getpass.getpass('Contaseña: ')
password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
User.create(username=args.user, email=args.email, password=password)