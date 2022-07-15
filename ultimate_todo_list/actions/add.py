from datetime import date, datetime

from ultimate_todo_list.actions.action import Action
from ultimate_todo_list.models import (Category, Project, Task, TaskCategory,
                                       TaskProject)


class Add(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['add'], 'add a task')
        self.parser.add_argument('name', help='name of task')
        self.parser.add_argument('-p', '--priority', type=int,
                                 choices=Task.priorities, default=0,
                                 help='1 is high, 8 is low, 0 = no priority')
        self.parser.add_argument('-i', '--interval', type=str, default=None,
                                 help='interval of recurence.\
                                 For example: 1d, 1m, 1y, ..., optional.')
        self.parser.add_argument('-d', '--due', type=str, default=None)
        self.parser.add_argument('-o', '--option', type=str,
                                 choices=Task.options, default=None)
        self.parser.add_argument('-r', '--projects', type=str, default=[],
                                 nargs='*')
        self.parser.add_argument('-c', '--categories', type=str, default=[],
                                 nargs='*')

    def fix_iterval(self, interval):
        return interval

    def fix_due(self, due, interval):
        if not due and interval and interval != 'optional':
            due = datetime.now().date()
        return due

    def do(self, args):
        interval = self.fix_iterval(args.interval)
        due = self.fix_due(args.due, interval)
        task = Task.create(priority=args.priority, name=args.name,
                           interval=interval, due=due, option=args.option)
        for project_name in args.projects:
            project, _ = Project.get_or_create(name=project_name)
            TaskProject.create(task=task, project=project)
        for category_name in args.categories:
            category, _ = Category.get_or_create(name=category_name)
            TaskCategory.create(task=task, category=category)
        Task.fix_indexes()
        print(args)
