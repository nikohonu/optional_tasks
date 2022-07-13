'''Example cli application'''
import argparse

import optional_tasks.models
from optional_tasks.actions.add_skill import AddSkill
from optional_tasks.actions.add_task import AddTask
from optional_tasks.actions.do import Do
from optional_tasks.actions.list_skill import ListSkill
from optional_tasks.actions.list_task import ListTask


def main():
    '''Entry point'''
    parser = argparse.ArgumentParser(prog='optional_tasks')
    subparsers = parser.add_subparsers(dest='command')
    actions = [
        AddSkill(subparsers),
        AddTask(subparsers),
        Do(subparsers),
        ListSkill(subparsers),
        ListTask(subparsers),
    ]
    args = parser.parse_args()
    for action in actions:
        if args.command in action.names:
            action.do(args)


if __name__ == '__main__':
    main()
