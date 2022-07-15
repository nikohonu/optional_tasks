from optional_tasks.actions.action import Action
from optional_tasks.models.skills import Skills
from optional_tasks.models.tasks import Tasks


class AddSkill(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['add-skill', 'as'], 'add a new skill')
        self.parser.add_argument("name", help='name of a skill')
        self.parser.add_argument('-p', '--priority', type=float,
                                 help='priority of a skill')
        self.parser.add_argument('-P', '--parent', type=int,
                                 choices=Skills.get_indexes(),
                                 help='parent of a skill')

    def do(self, args):
        Skills.add(args.name, args.priority, args.parent)
        print(args)
