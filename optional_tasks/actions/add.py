from optional_tasks.actions.action import Action
from optional_tasks.models import Skill, Task, TaskSkill


class Add(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['add-task', 'at'], 'add a new task')
        self.parser.add_argument("name", help='name of task')
        self.parser.add_argument(
            '-r', '--priority', choices=['h', 'm', 'l'],
            type=str.lower, help='priority of task')
        task_ids = [task.id for task in Task.select()]
        self.parser.add_argument(
            '-p', '--parent', type=int, choices=task_ids,
            help='parents of task')
        skill_ids = [skill.id for skill in Skill.select()]
        self.parser.add_argument(
            '-s', '--skills', type=int, nargs='*', choices=skill_ids,
            help='skills of task')

    def do(self, args):
        priority = None
        match args.priority:
            case 'h':
                priority = 3
            case 'm':
                priority = 2
            case 'l':
                priority = 1
        task = Task.create(
            name=args.name, priority=priority, parent=args.parent)
        if args.skills:
            skills = [Skill.get_by_id(skill_id) for skill_id in args.skills]
            task.add_skills(skills)
        Task.inherit_skills()
        print(args)
