from pathlib import Path

from appdirs import user_data_dir
from peewee import (AutoField, CompositeKey, DateField, ForeignKeyField,
                    IntegerField, Model, SqliteDatabase, TextField)

data_dir = Path(user_data_dir('optional_tasks', '封獣ぬえ'))
data_dir.mkdir(parents=True, exist_ok=True)
db = SqliteDatabase(data_dir / 'data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    name = TextField()
    priority = IntegerField(null=True)
    parent = ForeignKeyField('self', null=True, backref='children')

    @property
    def priority_str(self):
        match self.priority:
            case 3:
                return 'H'
            case 2:
                return 'M'
            case 1:
                return 'L'
            case _:
                return None

    @property
    def skills(self):
        return [task_skill.skill for task_skill in self.task_skills]

    @property
    def skills_str(self):
        string = ''
        for skill in self.skills:
            string += f' +{skill.name}({skill.id})'
        return string

    def add_skill(self, skill):
        if skill not in self.skills and skill:
            TaskSkill.create(task=self, skill=skill)

    def add_skills(self, skills):
        if skills:
            [self.add_skill(skill) for skill in skills]

    def get_children(self, root_task=None):
        tasks = [self]
        for task in Task.select().where(Task.parent == root_task):
            tasks += task.get_children(task)
        return tasks

    @property
    def completion(self):
        dates = set([tc.date for tc in TaskCompletion.select()])
        completion_tree = {}
        tasks = self.get_children(self)
        for task in tasks:
            for tc in TaskCompletion.select().where(TaskCompletion.task == task, TaskCompletion.skill == None):
                if tc.date not in completion_tree:
                    completion_tree[tc.date] = set([tc])
                else:
                    completion_tree[tc.date].add(tc)
        return len(completion_tree)

    @property
    def score(self):
        priority = self.priority if self.priority else 1
        return self.completion / priority

    def inherit_skills(root_task=None):
        for task in Task.select().where(Task.parent == root_task):
            if task.parent:
                task.add_skills(task.parent.skills)
            Task.inherit_skills(task)

    def __str__(self):
        string = f'|{self.id}|'
        if self.priority:
            string += f' ({self.priority_str})'
        string += f' {self.name}'
        string += self.skills_str
        string += f' c:{self.completion}'
        string += f' s:{self.score}'
        return string


class Skill(BaseModel):
    name = TextField()
    parent = ForeignKeyField('self', null=True, backref='children')


class TaskSkill(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE', backref='task_skills')
    skill = ForeignKeyField(Skill, on_delete='CASCADE')

    class Meta:
        primary_key = CompositeKey('task', 'skill')


class TaskCompletion(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE')
    skill = ForeignKeyField(Skill, null=True, on_delete='CASCADE')
    date = DateField()

    class Meta:
        primary_key = CompositeKey('task', 'skill', 'date')


models = BaseModel.__subclasses__()
db.create_tables(models)
