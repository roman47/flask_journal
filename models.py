import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(unique=True)
    date = DateField(default=datetime.datetime.now)
    time_spent = IntegerField()
    what_you_learned = TextField()
    resources_to_remember = TextField()

    @classmethod
    def create_entry(cls, title, date, time_spent,
                     what_you_learned, resources_to_remember):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    date=date,
                    time_spent=time_spent,
                    what_you_learned=what_you_learned,
                    resources_to_remember=resources_to_remember)
        except IntegrityError:
            raise ValueError("Entry already exists")

    class Meta:
        database = DATABASE
        order_by = ('-date',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
