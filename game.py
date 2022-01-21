from input import insert_guide


def main():
    no_solution = 'There is no solutioin of this puzzle.'
    guide = insert_guide()
    table = guide.set_table()
    guide.solve_if_N(guide.solve_if_ONE(table))
    if guide.is_table_correct(table) is False:
        return no_solution
    guide.zero_into_list(table)
    guide.reduce_from_guide_overall(table)
    guide.limit_potential_solutions(table)
    if guide.check_if_only_ints(table) is True:
        if guide.is_everything_alright(table) is True:
            return table
        else:
            return no_solution
    else:
        solved = guide.guess_solution(table)
        return solved


if __name__ == '__main__':
    table = main()
    if type(table) is list:
        print('\n\nThe solution:\n')
        for rows in table:
            print(rows)
    else:
        print('\n')
        print(table)
