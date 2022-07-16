from pathlib import Path

from appdirs import user_data_dir
from peewee import (BooleanField, CompositeKey, DateField, FloatField,
                    ForeignKeyField, IntegerField, Model, SqliteDatabase,
                    TextField)

data_dir = Path(user_data_dir('ultimate_todo_list', 'nikohonu'))
data_dir.mkdir(parents=True, exist_ok=True)
db = SqliteDatabase(data_dir / 'ultimate_todo_list.db')

def cyan_str(string):
    return f'\033[36m{string}\033[00m'

def red_str(string):
    return f'\033[91m{string}\033[00m'

class BaseModel(Model):
    '''Base model for table in database'''
    class Meta:
        database = db


class Task(BaseModel):
    index = IntegerField(null=True)
    priority = IntegerField(default=0)
    name = TextField()
    interval = TextField(null=True)
    due = DateField(null=True)
    option = TextField(null=True)  # autoFail, autoComplete, hidden, deleted

    priorities = list(range(1, 9)) + [0]
    options = {'autoFail', 'autoComplete', 'hidden', None}

    @property
    def projects(self):
        return [task_project.project for task_project in self.task_projects]

    @property
    def categories(self):
        return [task_category.category for task_category in self.task_categories]

    @staticmethod
    def fix_indexes():
        i = 1
        for task in Task.select():
            if task.option == 'deleted':
                task.index = None
            else:
                task.index = i
                i += 1
            task.save()

    @staticmethod
    def get_indexes():
        return [task.index for task in Task.select().where(Task.index != None)]

    @ staticmethod
    def by_index(index: int):
        return Task.get(index=index)

    def __str__(self):
        max_index = len(str(max(Task.get_indexes())))
        projects = ''
        categories = ''
        for project in self.projects:
            projects += f' +{project.name}'
        for category in self.categories:
            categories += f' @{category.name}'
        priority = f' ({self.priority})' if self.priority else ''
        rec = ''
        if self.interval:
            rec = f' rec:{self.interval}'
        due = ''
        if self.due:
            due = f' due:{self.due}'
        option = ''
        completion = f' completions:{len(self.completions)}'\
            if self.completions else ''
        if self.option:
            option = f' option:{self.option}'
        return f'|{self.index:{max_index}}|{priority} {self.name}{projects}{categories}{rec}{due}{option}{completion}'


class Project(BaseModel):
    coefficient = FloatField(default=1)
    name = TextField(unique=True)
    option = TextField(null=True)  # hidden, deleted

    def __str__(self):
        coefficient = f'({self.coefficient}) ' if self.coefficient else ''
        return f'{coefficient}{self.name}'


class Category(BaseModel):
    coefficient = FloatField(default=1)
    name = TextField(unique=True)
    option = TextField(null=True)  # hidden, deleted

    @property
    def completions(self):
        tasks = Task.select()
        result = []
        for task in tasks:
            if self in task.categories:
                result += list(task.completions)
        return result

    @property
    def score(self):
        return len(self.completions) / self.coefficient


    def __str__(self):
        coefficient = f'({self.coefficient}) ' if self.coefficient else ''
        completions = f' completions:{len(self.completions)}' if self.completions else ''
        score = f' {cyan_str("score")}:{red_str(self.score)}' if self.score else ''
        return f'{coefficient}{self.name}{completions}{score}'


class TaskProject(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE', backref='task_projects')
    project = ForeignKeyField(Project, on_delete='CASCADE',
                              backref='project_tasks')

    class Meta:
        primary_key = CompositeKey('task', 'project')


class TaskCategory(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE',
                           backref='task_categories')
    category = ForeignKeyField(Category, on_delete='CASCADE',
                               backref='category_tasks')

    class Meta:
        primary_key = CompositeKey('task', 'category')


class Completion(BaseModel):
    task = ForeignKeyField(Task, on_delete='CASCADE', backref='completions')
    date = DateField()

    class Meta:
        primary_key = CompositeKey('task', 'date')


models = BaseModel.__subclasses__()
db.create_tables(models)
