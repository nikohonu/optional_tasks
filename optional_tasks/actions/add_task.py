from optional_tasks.actions.action import Action
from optional_tasks.models.skills import Skills
from optional_tasks.models.tasks import Tasks


class AddTask(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['add-task', 'at'], 'add a new task')
        self.parser.add_argument("name", help='name of task')
        self.parser.add_argument('-p', '--priority', type=float,
                                 help='priority of task')
        self.parser.add_argument('-P', '--parent', type=int,
                                 choices=Tasks.get_indexes(),
                                 help='parents of task')
        self.parser.add_argument('-s', '--skills', type=int, nargs='*',
                                 choices=Skills.get_indexes(),
                                 help='skills of task')

    def do(self, args):
        Tasks.add(args.name, args.priority, args.parent, args.skills)
        print(args)
