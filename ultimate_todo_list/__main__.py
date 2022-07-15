'''Example cli application'''
import argparse
import cProfile

from ultimate_todo_list.actions.add import Add
from ultimate_todo_list.actions.list import List
from ultimate_todo_list.actions.do import Do


def main():
    '''Entry point'''
    parser = argparse.ArgumentParser(prog='ultimate_todo_list')
    subparsers = parser.add_subparsers(dest='command')
    actions = [
        Add(subparsers),
        List(subparsers),
        Do(subparsers),
    ]
    args = parser.parse_args()
    for action in actions:
        if args.command in action.names:
            action.do(args)


if __name__ == '__main__':
    cProfile.run('main()', 'output.dat')
    # main()
