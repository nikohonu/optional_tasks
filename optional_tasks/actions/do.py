from optional_tasks.actions.action import Action
from optional_tasks.models.skills import Skills
from optional_tasks.models.tasks import Tasks


class Do(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['do', 'd'], 'complete a task')
        self.parser.add_argument(
            "id", type=int, choices=Tasks.get_indexes(), help='id of task')

    def do(self, args):
        Tasks.complete(args.id)
        print(args)
