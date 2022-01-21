from solver import Solver
import ast
import sys


def insert_guide():
    incorrect = True
    while incorrect is True:
        to_solve = input(f"\nType the guidence here. Allowed format:\t\t\
[...], [...], [...], [...]\n(4 separated lists with same ammount of numbers \
between 0 and table's lenght - numbers and lists must be devided by commas)\
\n\n")
        try:
            to_solve = list(ast.literal_eval(to_solve))
            incorrect = False
        except Exception:
            print('\nSomething went wrong.')
            incorrect = try_again()
    guide = Solver(to_solve)
    try:
        return guide
    except Exception as error:
        print(str(error))


def try_again():
    yes = [
        'y', 'Y', 'yes', 'Yes', 'YES'
        ]
    exitquit = [
        'q', 'Q', 'quit', 'Quit', 'QUIT', 'exit', 'Exit', 'EXIT'
    ]
    keys = yes + exitquit
    incorrect = True
    while incorrect is True:
        again = input(f'If you want to type guidance again press "y".\nIf you want to quit press "q".\n\n') # noqa
        if again not in keys:
            incorrect = True
        else:
            incorrect = False
    if again in yes:
        return True
    if again in exitquit:
        sys.exit(0)
