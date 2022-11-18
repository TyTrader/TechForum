from peewee import *
from os import path

db_connection_path = path.dirname(path.realpath(__file__))

db = SqliteDatabase(path.join(db_connection_path, "TechForum.db"))


class User(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


class Question(Model):
    question = CharField()
    answer = CharField()

    class Meta:
        database = db


User.create_table(fail_silently=True)
Question.create_table(fail_silently=True)
