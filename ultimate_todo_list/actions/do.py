from datetime import date, datetime, timedelta

from ultimate_todo_list.actions.action import Action
from ultimate_todo_list.models import Completion, Task


class Do(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['do'], 'complete a task')
        self.parser.add_argument(
            "index", type=int, choices=Task.get_indexes(), help='index of a task')

    def new_due(self, interval, due):
        strict = True if interval.startswith('+') else False
        interval_type = interval[-1]
        now = datetime.now().date()
        if strict:
            value = interval[1:-1]
        else:
            value = interval[:-1]
        value = int(value)
        if not strict:
            due = now
        while due <= now:
            match interval_type:
                case 'd':
                    due += timedelta(days=value)
                case 'w':
                    due += timedelta(days=value*7)
                case 'm':
                    due += timedelta(days=value*28)
                case 'y':
                    due += timedelta(days=value*365)
        return due

    def do(self, args):
        task = Task.by_index(args.index)
        date = datetime.now().date()
        completion, result = Completion.get_or_create(task=task, date=date)
        if result and task.interval and task.interval != 'optional':
            task.due = self.new_due(task.interval, task.due)
            task.save()
        if not task.interval:
            task.option = 'deleted'
            task.save()
        print(task)
        Task.fix_indexes() 
        print(args)
