"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
"""

import re


def parse_todo(path):
    """
    Parses the todo list in the given path and returns a dictionary of values
    organised by their ID.
    """

    with open(path, 'r') as f:
        data = f.readlines()

    tasks = {}
    for line in data:
        m = re.match(r'\[(?P<id>\d+)\] (?P<data>.*)', line)

        task_id = int(m.group('id'))
        task_data = m.group('data')

        tasks[task_id] = task_data

    return tasks


if __name__ == '__main__':
    import argparse

    path = '/home/michaela/todo.md'

    parser = argparse.ArgumentParser(description='Todo list manager')
    parser.add_argument('-m', '--mark-complete', type=bool)
    parser.add_argument('-a', '--add-task', type=str)

    args = parser.parse_args()

    if not args.mark_complete and not args.add_task:
        print parse_todo(path)
