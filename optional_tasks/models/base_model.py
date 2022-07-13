from pathlib import Path

from appdirs import user_data_dir
from peewee import Model, SqliteDatabase

data_dir = Path(user_data_dir('optional_tasks', 'nikohonu'))
data_dir.mkdir(parents=True, exist_ok=True)
db = SqliteDatabase(data_dir / 'optional_tasks.db')


class BaseModel(Model):
    '''Base model for table in database'''
    class Meta:
        database = db
