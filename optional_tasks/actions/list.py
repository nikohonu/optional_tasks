from optional_tasks.actions.action import Action
from optional_tasks.models import Task


class List(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['list', 'ls'], 'show a list of tasks')
        self.parser.add_argument('-t', '--type', choices=['all', 'now'],
                                 default='all', help='type of list')

    def get_children(self, root_task=None):
        tasks = []
        for task in Task.select().where(Task.parent == root_task):
            tasks.append(task)
        return tasks

    def print_all_tasks(self, tab=0, root_task=None):
        for task in Task.select().where(Task.parent == root_task):
            print(' '*tab + str(task))
            self.print_all_tasks(tab+1, task)

    def test(self, root_task=None):
        tasks = []
        for task in self.get_children(root_task):
            if task.priority:
                tasks.append(task)
            else:
                tasks += self.test(task)
        return tasks

    def print_now_tasks(self, tab=0, root_task=None,
                        ignore_without_priority=True):
        tasks = []
        if root_task:
            tasks = self.get_children(root_task)
        else:
            tasks = self.test()
        tasks = sorted(tasks, key=lambda x: x.score)
        for task in tasks:
            print(' '*tab + str(task))
            self.print_now_tasks(tab+1, task)

    def do(self, args):
        if 'type' in args:
            match args.type:
                case 'all':
                    self.print_all_tasks()
                case 'now':
                    self.print_now_tasks()
        else:
            self.print_all_tasks()
        print(args)
