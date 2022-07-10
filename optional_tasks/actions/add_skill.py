from optional_tasks.actions.action import Action
from optional_tasks.models import Skill


class AddSkill(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['add-skill', 'as'], 'add a new skill')
        self.parser.add_argument('name', type=str.lower, help='name of skill')
        ids = [skill.id for skill in Skill.select()]
        self.parser.add_argument(
            '-p', '--parent', type=int, choices=ids,
            help='parents of skill')

    def do(self, args):
        skill = Skill.create(name=args.name, parent= args.parent)
        print(args)
