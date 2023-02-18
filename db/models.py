import datetime
import databases
import sqlalchemy

import ormar
from os import environ
host = environ.get('DATABASE_HOST')
port = environ.get('DATABASE_PORT', 5432)
user = environ.get('DATABASE_USER')
password = environ.get('DATABASE_PASSWORD')
name = environ.get('DATABASE_NAME')

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class User(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    user_id: int = ormar.BigInteger(primary_key=True)
    send_time: str = ormar.Time(default=datetime.datetime.utcnow)
    number_of_words: int = ormar.Integer()
    sent_words: int = ormar.Integer(default=0)
    data: dict = ormar.JSON(default={"step": "main"})
    access_token: str = ormar.String(max_length=400, nullable=True)
    refresh_token: str = ormar.String(max_length=400, nullable=True)
    

# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.drop_all(engine)
# metadata.create_all(engine)