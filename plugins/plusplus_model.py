from pathlib import Path

from peewee import CharField, IntegerField, Model, SqliteDatabase

db = SqliteDatabase(Path(__file__).resolve().parent / "plusplus.db")


class Plusplus(Model):
    """
    Model for plusplus count
    """

    name = CharField(primary_key=True)
    counter = IntegerField(default=0)

    class Meta:
        database = db


db.connect()
db.create_tables([Plusplus], safe=True)
