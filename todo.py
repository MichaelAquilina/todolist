#! /usr/bin/python3m

"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
Author: Michael Aquilina 2014
"""

import re
import os

# TODO: Cleanup code
#       Convert to class
#       Add color terminal support
#       Better Error Handling
#       Allow deleting and inserting at 'all' selection


def filter_tasks(task_list, sections):
    """
    Takes an input dictionary task list and a list of string sections
    and returns a filtered task list containing only the sections
    specified
    """
    filtered_tasks = {}
    for section in sections:
        filtered_tasks[section] = []
        for task in task_list[section]:
            filtered_tasks[section].append(task)

    return filtered_tasks


def write_todo(task_list, file_path):
    """
    Writes a todolist formatted dictionary to file for reading at a later stage.
    task_list dictionaries passed should contain lists of todo items organised by their
    section name.
    """

    with open(file_path, 'w') as f:

        # Always write the default list on the top
        for task in task_list['default']:
            f.write('* %s\n' % task)

        # Grab the list of all other sections
        others = task_list.keys()
        for section in others:
            if section != 'default' and len(task_list[section]) > 0:
                f.write('\n')
                f.write('>%s\n' % section)
                for task in task_list[section]:
                    f.write('* %s\n' % task)


def read_todo(file_path):
    """
    Returns a dictionary of lists organised by their section. A 'default'
    section is always available in the dictionary but does not guarantee the
    list to have any contents
    """

    task_list = {'default': []}
    if not os.path.exists(file_path):
        return task_list

    # Read all data at one go for speed
    with open(file_path, 'r') as f:
        buffer = f.readlines()

    current_section = 'default'
    for line in buffer:
        if line.startswith('>'):
            # Clean up section names
            current_section = line[1:]
            current_section = current_section.strip()
            current_section = current_section.lower()

            task_list[current_section] = []
        else:
            # Attempt to match
            m = re.match(r'\* (?P<data>.*)', line)
            if m:
                task_data = m.group('data')
                task_list[current_section].append(task_data)

    return task_list


if __name__ == '__main__':
    import argparse

    todo_path = os.path.expanduser('~/todo.md')

    parser = argparse.ArgumentParser(description='Simple Todo list manager written in Python')
    parser.add_argument('sections', default=['default'], nargs='*')
    parser.add_argument('-m', '--mark-complete', type=int, nargs='+', help='Marks a specified task as complete')
    parser.add_argument('-a', '--add-task', type=str, nargs='+', help='Adds a task to a todo list')

    args = parser.parse_args()

    # Begin Processing Here
    tasks = read_todo(todo_path)
    if args.sections == ['all']:
        args.sections = tasks.keys()

    tasks = filter_tasks(tasks, args.sections)

    # Follow the order specified in the command line
    for section in args.sections:
        print('>%s' % section)
        for index, task in enumerate(tasks[section]):
            print('[%d] %s' % (index, task))

