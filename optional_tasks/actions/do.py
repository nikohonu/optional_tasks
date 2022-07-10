from optional_tasks.actions.action import Action
from optional_tasks.models import Skill, Task, TaskCompletion, TaskSkill


class Do(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['do', 'd'], 'complete a task')
        task_ids = [task.id for task in Task.select()]
        self.parser.add_argument(
            "id", type=int, choices=task_ids, help='id of task')
        self.parser.add_argument(
            '-s', '--skills', type=int, nargs='*',
            help='skills of task')

    def do(self, args):
        task = Task.get_by_id(args.id)
        skills = None
        if args.skills:
            skills = [Skill.get_by_id(skill_id) for skill_id in args.skills]
        else:
            skills = task.skills
        skills += [None]
        date = datetime.now().date()
        for skill in skills:
            print(task, skill, date)
            task.add_skill(skill)
            Task.inherit_skills()
            TaskCompletion.get_or_create(task=task, skill=skill, date=date)
        print(args)
