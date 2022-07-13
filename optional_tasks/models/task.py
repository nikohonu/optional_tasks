from peewee import (AutoField, BooleanField, CompositeKey, DateField,
                    FloatField, ForeignKeyField, IntegerField, TextField)

from optional_tasks.models.base_model import BaseModel
from optional_tasks.models.skill import Skill


class Task(BaseModel):
    index = IntegerField(null=True)
    name = TextField()
    priority = FloatField(null=True)
    parent = ForeignKeyField('self', null=True)

    @staticmethod
    def _get_children(parent):
        return Task.select()\
            .where(Task.parent == parent)\
            .order_by(Task.id.desc())

    def add_skill(self, skill):
        TaskSkill.create(task=self, skill=skill)

    def add_skills(self, skills):
        for skill in skills:
            self.add_skill(skill)

    @property
    def skills(self):
        task_skills = TaskSkill.select().where(TaskSkill.task == self)
        if task_skills:
            return [task_skill.skill for task_skill in task_skills]

    def get_completion(self):
        dates = set()
        queue = [self]
        while queue:
            current = queue.pop()
            queue += list(self._get_children(current))
            completions = TaskCompletion.select()\
                .where(TaskCompletion.task == current,
                       TaskCompletion.skill == None)
            for completion in completions:
                dates.add(completion.date)
        return len(dates)

    @property
    def score(self):
        if self.priority:
            return round(self.get_completion() / self.priority * 100)/100
        else:
            return self.get_completion()


    def __str__(self):
        if self.priority:
            priority = f'({self.priority}) '
        else:
            priority = ''
        if self.skills:
            skills = ' skills:' +\
                ','.join([skill.name for skill in self.skills])
        else:
            skills = ''
        return f'{self.index:2}. {priority}{self.name}{skills} completions:{self.get_completion()} score:{self.score}'


class TaskSkill(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE')
    skill = ForeignKeyField(Skill, on_delete='CASCADE')

    class Meta:
        primary_key = CompositeKey('task', 'skill')


class TaskCompletion(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE')
    skill = ForeignKeyField(Skill, null=True, on_delete='CASCADE')
    date = DateField()

    class Meta:
        primary_key = CompositeKey('task', 'skill', 'date')


TaskCompletion.create_table()
Task.create_table()
TaskSkill.create_table()
