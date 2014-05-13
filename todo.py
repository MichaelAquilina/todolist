#! /usr/bin/python3m

"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
Author: Michael Aquilina 2014
"""

import re
import os

# TODO: Cleanup code
#       Don't show empty sections
#       Convert to class
#       Add color terminal support
#       Better Error Handling


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
            if section != 'default':
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

    path = os.path.expanduser('~/todo.md')

    parser = argparse.ArgumentParser(description='Simple Todo list manager written in Python')
    parser.add_argument('section', default='default', nargs='?')
    parser.add_argument('-m', '--mark-complete', type=int, nargs='+')
    parser.add_argument('-a', '--add-task', type=str)

    args = parser.parse_args()

    tasks = read_todo(path)  # Full todo list
    selected_tasks = tasks[args.section]  # Specific section

    if args.add_task:
        selected_tasks.append(args.add_task)

        write_todo(tasks, path)
    elif args.mark_complete:

        for task_index in sorted(args.mark_complete, reverse=True):
            print('Marking task "%s" as complete' % selected_tasks[task_index])
            del(selected_tasks[task_index])

        write_todo(tasks, path)

    # Always print the tasks at the end of an operation
    print('Showing list: %s \t (available: %s)' % (args.section, list(tasks.keys())))
    for index, data in enumerate(selected_tasks):
        print('[%d] %s' % (index, data))
