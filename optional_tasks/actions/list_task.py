from optional_tasks.actions.action import Action
from optional_tasks.models.skills import Skills
from optional_tasks.models.tasks import Tasks


class ListTask(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['list-task', 'lt'], 'list of tasks')
        self.parser.add_argument('-t', '--type', choices=['all', 'now'],
                                 default='all', help='type of list')

    def do(self, args):
        if 'type' in args:
            match args.type:
                case 'all':
                    Tasks.print()
                case 'now':
                    Tasks.print_now()
        else:
            Tasks.print()
        print(args)
