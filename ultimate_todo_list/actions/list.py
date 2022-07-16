import time
from datetime import date, datetime

from ultimate_todo_list.actions.action import Action
from ultimate_todo_list.models import (Category, Project, Task, TaskCategory,
                                       TaskProject)


class List(Action):
    def __init__(self, subparsers):
        super().__init__(subparsers, ['ls'], 'list of tasks')
        list_types = ['tasks', 'projects', 'categories']
        self.parser.add_argument('-l', '--list', choices=list_types,
                                 default=list_types[0], help='type of list')
        sort_types = ['index', 'abc', 'priority', 'interval', 'due', 'completions',
                      'coefficient', 'score']
        self.parser.add_argument('-s', '--sort', choices=sort_types,
                                 default=sort_types[0], help='type of sorting')
        group_types = [None, 'priority', 'interval', 'due', 'coefficient',
                       'completions' 'score']
        self.parser.add_argument('-g', '--group', choices=group_types,
                                 default=group_types[0], help='type of grouping')
        self.parser.add_argument('-r', '--reverse', action='store_true')

    def interval_to_int(self, interval):
        if interval and interval != 'optional':
            strict = True if interval.startswith('+') else False
            interval_type = interval[-1]
            if strict:
                value = interval[1:-1]
            else:
                value = interval[:-1]
            value = int(value)
            match interval_type:
                case 'd':
                    return value
                case 'w':
                    return value*7
                case 'm':
                    return value*28
                case 'y':
                    return value*365
        else:
            return None

    def fix_sort(self, value, reverse):
        if reverse:
            return value if value else 0
        else:
            return value if value else float('inf')

    def fix_interval(self, interval, reverse):
        return self.fix_sort(self.interval_to_int(interval), reverse)

    def fix_date(self, date, reverse):
        date = time.mktime(date.timetuple()) if date else None
        return self.fix_sort(date, reverse)

    def sort_tasks(self, tasks, sort_type, reverse):
        match sort_type:
            case 'index':
                return sorted(tasks, key=lambda x: x.index, reverse=reverse)
            case 'abc':
                return sorted(tasks, key=lambda x: x.name, reverse=reverse)
            case 'priority':
                if reverse:
                    return sorted(tasks, key=lambda x: 9 - x.priority)
                else:
                    return sorted(tasks, key=lambda x: 9 - x.priority
                                  if x.priority > 0 else 0, reverse=True)
            case 'interval':
                return sorted(tasks, key=lambda x: self.fix_interval(
                    x.interval, reverse), reverse=reverse)
            case 'due':
                return sorted(tasks, key=lambda x: self.fix_date(x.due, reverse),
                              reverse=reverse)
            case 'completions':
                return sorted(
                    tasks, key=lambda x: self.fix_sort(
                        len(x.completions),
                        reverse),
                    reverse=reverse)
            case _:
                return []

    def group_tasks(self, sort_type, group_type, reverse):
        tasks = Task.select()
        match group_type:
            case None:
                tasks = self.sort_tasks(tasks, sort_type, reverse)
                for task in tasks:
                    print(task)
            case 'priority':
                priorities = list(range(1, 9)) + [0] \
                    if not reverse else reversed(range(0, 9))
                print(priorities)
                for priority in priorities:
                    tasks = self.sort_tasks(tasks, sort_type, reverse)
                    tmp_tasks = list(filter(lambda x: x.priority == priority, tasks))
                    if tmp_tasks:
                        result = f'Priority: {priority}'
                        print(f'{result}\n{"=" * len(result)}')
                        for task in tmp_tasks:
                            print(task)
                        print()
            # TODO: group by interval
            case 'interval':
                def print_interval(interval):
                    t = ''
                    if interval % 365 == 0:
                        v = int(interval / 365)
                        t = 'year'
                    elif interval % 28 == 0:
                        v = int(interval / 28)
                        t = 'month'
                    elif interval % 7 == 0:
                        v = int(interval / 7)
                        t = 'week'
                    else:
                        v = interval
                        t = 'day'
                    v = f' {v}' if v > 1 else ''
                    t = t + 's' if v != '' else t
                    result = f'Recurence: every{v} {t}'
                    print(f'{result}\n{"=" * len(result)}')
                tasks = self.sort_tasks(tasks, 'interval', reverse)
                intervals = sorted(set([self.interval_to_int(task.interval)
                                        for task in tasks
                                        if self.interval_to_int(task.interval)]))
                for interval in intervals:
                    print_interval(interval)
                    for task in filter(lambda x: self.interval_to_int(x.interval) ==
                                       interval, tasks):
                        print(task)
                    print()
            case 'due':
                def print_delta(delta):
                    result = 'Due: today'
                    v = abs(delta[0]) if abs(delta[0]) > 1 else 'a'
                    t = ''
                    match delta[1]:
                        case 'd':
                            t = 'day'
                        case 'w':
                            t = 'week'
                        case 'm':
                            t = 'month'
                        case 'y':
                            t = 'year'
                    t = t + 's' if v != 'a' else t
                    if delta[0] > 0:
                        result = f'Due: in {v} {t}'
                    elif delta[0] < 0:
                        result = f'Due: {v} {t} ago'
                    print(f'{result}\n{"=" * len(result)}')

                tasks = self.sort_tasks(tasks, 'due', reverse)
                tasks = filter(lambda x: x.due != None, tasks)
                now = datetime.now().date()
                deltas = {}
                for task in tasks:
                    days = (task.due-now).days
                    years = int(days / 365.25)
                    months = int(days / (365.25/12))
                    weeks = int(days / 7)
                    if abs(years) >= 1:
                        key = (years, 'y')
                        if key not in deltas:
                            deltas[key] = [task]
                        else:
                            deltas[key].append(task)
                    elif abs(months) >= 1:
                        key = (months, 'm')
                        if key not in deltas:
                            deltas[key] = [task]
                        else:
                            deltas[key].append(task)
                    elif abs(weeks) >= 1:
                        key = (weeks, 'w')
                        if key not in deltas:
                            deltas[key] = [task]
                        else:
                            deltas[key].append(task)
                    else:
                        key = (days, 'd')
                        if key not in deltas:
                            deltas[key] = [task]
                        else:
                            deltas[key].append(task)
                for delta in deltas:
                    print_delta(delta)
                    tasks = self.sort_tasks(deltas[delta], sort_type, reverse)
                    for task in tasks:
                        print(task)
                    print()

    def sort_projects_or_categories(self, entities, sort_type, reverse):
        match sort_type:
            case ('abc' | 'index'):
                return sorted(entities, key=lambda x: x.name, reverse=reverse)
            case 'coefficient':
                return sorted(entities, key=lambda x: x.coefficient, reverse=reverse)
            case 'score':
                return sorted(entities, key=lambda x: x.score, reverse=reverse)
            case _:
                return []

    def group_categories(self, sort_type, group_type, reverse):
        categories = Category.select()
        match group_type:
            case None:
                categories = self.sort_projects_or_categories(
                    categories, sort_type, reverse)
                for category in categories:
                    print(category)
            case '':
                pass

    def do(self, args):
        match args.list:
            case 'tasks':
                self.group_tasks(args.sort, args.group, args.reverse)
            case 'projects':
                pass
            case 'categories':
                self.group_categories(args.sort, args.group, args.reverse)
