from optional_tasks.models.skill import Skill


class Skills:
    def __init__():
        pass

    @staticmethod
    def _update_indexes():
        i = 0
        for skill in Skill.select():
            skill.index = i
            i += 1
            skill.save()

    @staticmethod
    def _get_children(parent, reverse=False):
        return Skill.select()\
            .where(Skill.parent == parent)\
            .order_by(Skill.id.desc())

    @staticmethod
    def add(name, priority, parent_index):
        parent = None
        if parent_index != None:
            parent = Skill.get(Skill.index == parent_index)
        Skill.create(name=name, priority=priority, parent=parent)
        Skills._update_indexes()

    @staticmethod
    def print():
        queue = [(-1, None)]
        while queue:
            current = queue.pop()
            queue += [(current[0] + 1, task) for task in
                      Skills._get_children(current[1], True)]
            if current[1]:
                print(f'{"    "*current[0]}{current[1]}')

    @staticmethod
    def get_indexes():
        return [skill.index for skill in Skill.select()]
