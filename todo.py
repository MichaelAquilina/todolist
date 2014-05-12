#! /usr/bin/python3m

"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
Author: Michael Aquilina 2014
"""

import re
import os


def write_todo(task_list, file_path):

    with open(file_path, 'w') as f:
        for task in task_list:
            f.write('* %s\n' % task)


def read_todo(file_path):
    """
    Parses the todo list in the given path and returns a dictionary of values
    organised by their ID. Returns an empty dictionary if no todo list is available.
    """

    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as f:
        data = f.readlines()

    task_list = []
    for line in data:
        m = re.match(r'\* (?P<data>.*)', line)
        task_data = m.group('data')

        task_list.append(task_data)

    return task_list


if __name__ == '__main__':
    import argparse

    path = os.path.expanduser('~/todo.md')

    parser = argparse.ArgumentParser(description='Simple Todo list manager written in Python')
    parser.add_argument('-m', '--mark-complete', type=int, nargs='+')
    parser.add_argument('-a', '--add-task', type=str)

    args = parser.parse_args()

    # Retrieve the todo list
    tasks = read_todo(path)

    if args.add_task:
        tasks.append(args.add_task)

        write_todo(tasks, path)
    elif args.mark_complete:

        for task_index in sorted(args.mark_complete, reverse=True):
            print('Marking task "%s" as complete' % tasks[task_index])
            del(tasks[task_index])

        write_todo(tasks, path)

    # Always print the tasks at the end of an operation
    for index, data in enumerate(tasks):
        print('[%d] %s' % (index, data))
