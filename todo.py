"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
"""

if __name__ == '__main__':

    import os
    import argparse

    path = '/home/michaela/todo.md'

    parser = argparse.ArgumentParser(description='Todo list manager')
    parser.add_argument('-m', '--mark-complete', type=bool)
    parser.add_argument('-a', '--add-task', type=str)

    args = parser.parse_args()

    if not args.mark_complete and not args.add_task:
        if os.path.exists(path):

            with open(path, 'r') as f:
                print f.read()
