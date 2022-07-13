from peewee import (AutoField, BooleanField, CompositeKey, DateField,
                    FloatField, ForeignKeyField, IntegerField, TextField)

from optional_tasks.models.base_model import BaseModel


class Skill(BaseModel):
    index = IntegerField(null=True)
    name = TextField()
    priority = FloatField(null=True)
    parent = ForeignKeyField('self', null=True)

    def __str__(self):
        return f'{self.index}. {self.name}'


Skill.create_table()
