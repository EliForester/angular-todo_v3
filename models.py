import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config

DATABASE = SqliteDatabase('todos.sqlite')


class Todo(Model):
    name = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    completed = BooleanField(default=False, null=True)

    class Meta:
        database = DATABASE


class User(Model):
    username = CharField(max_length=255, unique=True)
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = DATABASE


def initialize():
    try:
        DATABASE.connect()
        DATABASE.create_tables([User, Todo], safe=True)
        DATABASE.close()
    except FileExistsError:
        pass
