"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
"""

import re


def write_todo(tasks, path):
    with open(path, 'w') as f:
        for id, data in tasks.items():
            f.write('[%d] %s\n' % (id, data))


def read_todo(path):
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

    # Retrieve the todo list
    tasks = read_todo(path)

    if args.add_task:
        # Hack which should be changed in the future
        count = max(tasks.keys())

        tasks[count + 1] = args.add_task

        write_todo(tasks, path)
    elif args.mark_complete:
        pass
    else:
        for id, data in tasks.items():
            print '[%d] %s' % (id, data)