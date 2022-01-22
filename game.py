from solver import Solver
import ast
import sys


def main():
    """
    Method which contains all of the essencial methods from *Solver.py*./n
    Order of running methods:\n
    1) ``insert_guide()``\n
    2) ``set_table()``\n
    3) ``solve_if_ONE()``\n
    4) ``solve_if_N()``\n
    5) ``is_table_correct()``\n
    6) ``zero_into_list()``\n
    7) ``reduce_from_guide()``\n
    8) ``check_if_only_ints()``\n
    9) ``is_everything_alright()``\n
    10) ``guess_solution()``\n

    When puzzle is solvable program prints the table with correct answer.
    If there is no solution for it, then proper message is printed.
    """
    no_solution = 'There is no solutioin of this puzzle.'
    guide = insert_guide()
    table = guide.set_table()
    guide.solve_if_N(guide.solve_if_ONE(table))
    if guide.is_table_correct(table) is False:
        return no_solution
    guide.zero_into_list(table)
    guide.reduce_from_guide(table)
    guide.limit_potential_solutions(table)
    if guide.check_if_only_ints(table) is True:
        if guide.is_everything_alright(table) is True:
            return table
        else:
            return no_solution
    else:
        solved = guide.guess_solution(table)
        return solved


def insert_guide():
    """
    Method that requires the guidance as an input for the program.
    """
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
    """
    Method that reads the input again after failed attempt
    """
    yes = [
        'y', 'Y', 'yes', 'Yes', 'YES'
        ]
    exitquit = [
        'q', 'Q', 'quit', 'Quit', 'QUIT', 'exit', 'Exit', 'EXIT'
    ]
    keys = yes + exitquit
    incorrect = True
    while incorrect is True:
        again = input(f'If you want to type guidance again, press "y".\nIf you want to quit, press "q".\n\n') # noqa
        if again not in keys:
            incorrect = True
        else:
            incorrect = False
    if again in yes:
        return True
    if again in exitquit:
        sys.exit(0)


if __name__ == '__main__':
    table = main()
    if type(table) is list:
        print('\n\nThe solution:\n')
        for rows in table:
            print(rows)
    else:
        print('\n')
        print(table)
