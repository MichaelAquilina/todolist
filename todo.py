#! /usr/bin/python3m

"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
"""

import re
import os
import operator


def garbage_collect(tasks):
    """Performs garbage collection on tasks by removing fragmented IDs"""
    gc_tasks = {}
    counter = 1

    for id, data in sort_tasks(tasks):
        gc_tasks[counter] = data
        counter += 1

    return gc_tasks


def sort_tasks(tasks):
    return sorted(tasks.items(), key=operator.itemgetter(0))


def write_todo(tasks, path):

    with open(path, 'w') as f:
        for id, data in sort_tasks(tasks):
            f.write('[%d] %s\n' % (id, data))


def read_todo(path):
    """
    Parses the todo list in the given path and returns a dictionary of values
    organised by their ID. Returns an empty dictionary if no todo list is available.
    """

    if not os.path.exists(path):
        return {}

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

    path = os.path.expanduser('~/todo.md')

    parser = argparse.ArgumentParser(description='Simple Todo list manager written in Python')
    parser.add_argument('-m', '--mark-complete', type=int)
    parser.add_argument('-a', '--add-task', type=str)

    args = parser.parse_args()

    # Retrieve the todo list
    tasks = read_todo(path)

    if args.add_task:
        # Hack which should be changed in the future
        count = max(tasks.keys())

        tasks[count + 1] = args.add_task
        # Garbage collect any fragments
        tasks = garbage_collect(tasks)

        write_todo(tasks, path)
    elif args.mark_complete:
        del(tasks[args.mark_complete])

        # Garbage collect any fragments
        tasks = garbage_collect(tasks)

        write_todo(tasks, path)
    else:
        for id, data in sort_tasks(tasks):
            print('[%d] %s' % (id, data))
