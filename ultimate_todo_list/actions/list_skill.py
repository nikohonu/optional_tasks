from optional_tasks.actions.action import Action
from optional_tasks.models.skills import Skills
from optional_tasks.models.tasks import Tasks


class ListSkill(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['list-skill', 'ls'], 'list of skills')

    def do(self, args):
        Skills.print()
        print(args)
