from datetime import datetime

from optional_tasks.models.skill import Skill
from optional_tasks.models.task import Task, TaskCompletion


class Tasks:
    def __init__(self):
        pass

    @staticmethod
    def _update_indexes():
        i = 0
        for task in Task.select():
            task.index = i
            i += 1
            task.save()

    @staticmethod
    def add(name, priority, parent_index, skill_indexes):
        parent = None
        if parent_index != None:
            parent = Task.get(Task.index == parent_index)
        task = Task.create(name=name, priority=priority, parent=parent)
        Tasks._update_indexes()
        if skill_indexes:
            skills = [Skill.get(Skill.index == skill_index)
                      for skill_index in skill_indexes]
            task.add_skills(skills)

    @staticmethod
    def complete(index):
        task = Task.get(Task.index == index)
        skills = [None] + task.skills
        date = datetime.now().date()
        for skill in skills:
            TaskCompletion.get_or_create(task=task, skill=skill, date=date)

    @staticmethod
    def print():
        queue = [(-1, None)]
        while queue:
            current = queue.pop()
            queue += [(current[0] + 1, task) for task in
                      Task._get_children(current[1])]
            if current[1]:
                print(f'{"    "*current[0]}{current[1]}')

    @staticmethod
    def print_now():
        def sort_queue(queue):
            return sorted(queue, key=lambda x: x[1].score, reverse=True)
        priority_queue = [(-1, None)]
        queue = []
        while priority_queue:
            current = priority_queue.pop()
            if current[1] and  current[1].priority != None:
                queue.append(current)
            else:
                priority_queue += [(0, task) for task in
                                   Task._get_children(current[1])]

        queue = sort_queue(queue)
        while queue:
            current = queue.pop()
            queue += sort_queue([(current[0] + 1, task) for task in
                      Task._get_children(current[1])])
            print(f'{"    "*current[0]}{current[1]}')

    @staticmethod
    def get_indexes():
        return [task.index for task in Task.select()]
