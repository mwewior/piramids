from solver import Solver
import ast


def insert_guide():
    to_solve = input(f"Type the guidence here. Allowed format:\t\t\
[...], [...], [...], [...]\n(4 separated lists with same ammount of numbers \
between 0 and table's lenght - numbers and lists must be devided by commas)\
\n\n")
    to_solve = list(ast.literal_eval(to_solve))
    guide = Solver(to_solve)
    try:
        return guide
    except Exception as error:
        print(str(error))
