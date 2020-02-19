#!/usr/bin/env python3
from peewee_migrate import Router
from playhouse.db_url import connect
import os
import argparse
from app import config
database = connect(config.DATABASE)
router = Router(database, migrate_dir='migrations', ignore=['basemodel'])

parser = argparse.ArgumentParser(description='Apply or manage database migrations.')
parser.add_argument('-c', '--create', metavar='NAME', help='Creates a new migration')
parser.add_argument('-a', '--auto', metavar='NAME', help='Creates a new migration (automatic)')

args = parser.parse_args()

if args.create:
    router.create(args.create)
elif args.auto:
    router.create(args.auto, 'app')
else:
    router.run()
