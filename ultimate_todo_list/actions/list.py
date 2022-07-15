from datetime import date, datetime

from ultimate_todo_list.actions.action import Action
from ultimate_todo_list.models import (Category, Project, Task, TaskCategory,
                                       TaskProject)


class List(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['ls'], 'list of tasks')

    def do(self, args):
        tasks = Task.select()
        dates = sorted(set([task.due for task in tasks if task.due != None]))
        for date in dates:
            print(date)
            local_tasks = [task for task in tasks if task.due == date]
            local_tasks = sorted(local_tasks, key=lambda x: x.priority)
            for task in local_tasks:
                if task.option != 'deleted':
                    print(task)
        print(None)
        local_tasks = [task for task in tasks if task.due == None]
        local_tasks = sorted(local_tasks, key=lambda x: x.priority)
        for task in local_tasks:
            if task.option != 'deleted':
                print(task)

        print(args)
