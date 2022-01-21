"""
This program solves the puzzle called 'Pyramids'.
version 1.0f

Algorithm used for solving the puzzle https://en.wikipedia.org/wiki/Backtracking

Terminology:
Guidance / guide - List of 4 lists (each of the same lenght and containing only ints inside) with prompts to solve the puzzle;
N - Lenght of table;
Table - List of N lists containing N elements - kind of NxN matrix.
""" # noqa

import copy
from project_errors_piramidy import InvalidGuideError, PyraminInterposeError, InvalidTableError # noqa


class Solver:
    """
    Main class of the whole program. Contains methods which gradually solve whole puzzle.
    Some of them are based on backtracking algorithm.

    :param guide: Guide for solving the table.
    :type guide: list
    """ # noqa

    def __init__(self, guide: list):
        if len(guide) != 4:
            message = 'Invalid guidance. There must be exactly 4 lists' # noqa
            raise InvalidGuideError(message)

        for i in range(3):
            if len(guide[i]) != len(guide[i+1]):
                message = 'Invalid guidance. All of the rows must have same lenght' # noqa
                raise InvalidGuideError(message)

        for i in range(4):
            for j in range(len(guide[i])):
                if isinstance(guide[i][j], str):
                    if guide[i][j].isdigit():
                        guide[i][j] = int(guide[i][j])
                    else:
                        message = 'Invalid guidance. Lists must contain only ints in them' # noqa
                        raise InvalidGuideError(message)
                if isinstance(guide[i][j], float) or int(guide[i][j]) < 0:
                    message = 'Invalid guidance. Number of the pyramids you can see must be a positive number.' # noqa
                    raise InvalidGuideError(message)
                if int(guide[i][j]) > len(guide[i]):
                    message = 'Invalid guidance. Number of the pyramids you can see must not exceed the lenght of the table' # noqa
                    raise InvalidGuideError(message)

        self._guide = guide

    def guide(self):
        """
        :return: Guidance - table of prompts.
        :rtype: list
        """
        return self._guide

    def lenght(self):
        """
        :return: Table's lenght.
        :rtype: int
        """
        return int(len(self.guide()[0]))

    def generate_raw_table(self):
        """
        :return: Generates clear table. Every position of table becomes '0'.
        :rtype: list
        """ # noqa

        n = int(self.lenght())
        blank = []
        for i in range(n):
            blank.append([])
            for j in range(n):
                blank[i].append(0)
        return blank

    def set_table(self, table=None):
        """
        Checks if table is partly solved and returns it to other methods (if correct).

        :type table: list, optional
        :param table: previous table (if exists)
        :raises InvalidTableError: if height of pyramid on given table is out of range
        """ # noqa

        if table is None:
            overwritten_table = self.generate_raw_table()
        else:
            overwritten_table = table
            n = self.lenght()
            for i in range(n):
                for j in range(n):
                    if type(overwritten_table[i][j]) is int:
                        if int(overwritten_table[i][j]) > n:
                            message = "Height of pyramid on table is incorrect"
                            raise InvalidTableError(message)
        return overwritten_table

    def is_table_correct(self, table=None):
        """
        Checks if the each number occures only once in the row and in the column of the table.

        :type table: list
        :param table: previous table
        :return: returns True when given combination is correct (only one occurence of each number in row and column), otherwise returns False.
        :rtype: bool
        """ # noqa

        row = self.is_row_correct(table)
        col = self.is_column_correct(table)
        if row is True and col is True:
            return True
        else:
            return False

    def is_row_correct(self, table=None):
        n = self.lenght()
        if table is None:
            pass
        else:
            for i in range(n):
                row = []
                for elem in table[i]:
                    if type(elem) is int and elem != 0:
                        row.append(elem)
                row.sort()
                b = list(set(row))
                b.sort()
                if len(row) == 0:
                    pass
                if row != b:
                    return False
        return True

    def is_column_correct(self, table=None):
        n = self.lenght()
        if table is None:
            pass
        else:
            for i in range(n):
                column = []
                for j in range(n):
                    if type(table[j][i]) is int and table[j][i] != 0:
                        column.append(table[j][i])
                column.sort()
                b = list(set(column))
                b.sort()
                if len(column) == 0:
                    pass
                if column != b:
                    return False
        return True

    def interposer(self, table, in1, in2, v):
        """
        Substitude for more overall approach to the solving methods.

        :type in1: int
        :param in1: indexes of the first list - which row
        :type in2: int
        :param in2: indexes of the second list - which column
        :type v: int
        :param v: value that will overwrite the '0'
        """
        if table[in1][in2] == 0 or table[in1][in2] == v:
            table[in1][in2] = v
        else:
            raise PyraminInterposeError()

    def solve_if_ONE(self, table=None):
        """
        Method finds if there is '1' in guidance, then overwrites the '0' in table with 'N' on proper position

        :return: returns overwritten table
        :rtype: list
        :raises InvalidTableError: raises if there is value other than '0' or 'N' on position where 'N' were meant to be
        """ # noqa
        table = self.set_table(table)
        n = self.lenght()
        for row in range(4):
            for col in range(n):
                try:
                    if self.guide()[row][col] == 1:
                        if row == 0:
                            self.interposer(table, 0, col, n)
                        if row == 1:
                            self.interposer(table, n-1, col, n)
                        if row == 2:
                            self.interposer(table, col, 0, n)
                        if row == 3:
                            self.interposer(table, col, n-1, n)
                except PyraminInterposeError:
                    raise PyraminInterposeError()
        return table

    def solve_if_N(self, table=None):
        """
        Method finds if there is 'N' in guidance, then overwrites in succession the '0' in row or column with values in range from 1 to N on proper positions

        :return: returns overwritten table
        :rtype: list
        :raises InvalidTableError: raises if there is value other than '0' or 'K' on position where 'K' were meant to be. (K is a value in range from 1 to N)
        """ # noqa

        table = self.set_table(table)
        n = self.lenght()
        for row in range(4):
            for col in range(n):
                index_list = list(range(n))
                for val in index_list:
                    if row == 1 or row == 3:
                        value = index_list[-val - 1] + 1
                    else:
                        value = val + 1
                    try:
                        if self.guide()[row][col] == n:
                            if row == 0 or row == 1:
                                self.interposer(table, val, col, value)
                            if row == 2 or row == 3:
                                self.interposer(table, col, val, value)
                    except PyraminInterposeError:
                        raise PyraminInterposeError()
        return table

    def zero_into_list(self, table=None):
        """
        When program finnish solving cases with '1' or 'N' from guide, then replace every '0' from the table to list.
        Each of this lists contains every value in range from 1 to N.
        List contains possible options to interpose in this position.
        """ # noqa

        table = self.set_table(table)
        n = self.lenght()
        for i in range(n):
            for j in range(n):
                if table[i][j] == 0:
                    table[i][j] = list(range(1, n+1))
        return table

    def reduce_from_guide_overall(self, table):
        """
        Reduces possible options that can occur.
        If guide prompt excludes the possibility of value to occur, then it is removed from list of possible options.
        For example:
        if the guidance shows '3' and the lenght is 5 then:
        '5' cannot occur on the first and second position and '4' cannot occur on the first position.
        """ # noqa

        self.reduce_from_guide_top(table)
        self.reduce_from_guide_bottom(table)
        self.reduce_from_guide_left(table)
        self.reduce_from_guide_right(table)
        self.unlist_single_value(table)
        return table

    def unlist_single_value(self, table):
        """
        If list with possible options contains only one value, then it must be this value.
        Method replaces the list with this value.
        """ # noqa

        n = self.lenght()
        for i in range(n):
            for j in range(n):
                if type(table[i][j]) is list:
                    if len(table[i][j]) == 1:
                        table[i][j] = table[i][j][0]
        return table

    def reduce_from_guide_top(self, table):
        n = self.lenght()
        values = self.guide()[0]
        for i in range(n):
            value = values[i]
            if value == 0 or value == 1 or value == n:
                pass
            else:
                x = value - 1
                for p in range(x):
                    for y in range(x-p):
                        t = table[y][i]
                        if type(t) is list:
                            if n-p in table[y][i]:
                                t.remove(n-p)
        return table

    def reduce_from_guide_bottom(self, table):
        n = self.lenght()
        values = self.guide()[1]
        for i in range(n):
            value = values[i]
            if value == 0 or value == 1 or value == n:
                pass
            else:
                x = value - 1
                for p in range(x):
                    for y in range(x-p):
                        t = table[-(y+1)][i]
                        if type(t) is list:
                            if n-p in table[-(y+1)][i]:
                                t.remove(n-p)
        return table

    def reduce_from_guide_left(self, table):
        n = self.lenght()
        values = self.guide()[2]
        for i in range(n):
            value = values[i]
            if value == 0 or value == 1 or value == n:
                pass
            else:
                x = value - 1
                for p in range(x):
                    for y in range(x-p):
                        t = table[i][y]
                        if type(t) is list:
                            if n-p in table[i][y]:
                                t.remove(n-p)
        return table

    def reduce_from_guide_right(self, table):
        n = self.lenght()
        values = self.guide()[3]
        for i in range(n):
            value = values[i]
            if value == 0 or value == 1 or value == n:
                pass
            else:
                x = value - 1
                for p in range(x):
                    for y in range(x-p):
                        t = table[i][-(y+1)]
                        if type(t) is list:
                            if n-p in table[i][-(y+1)]:
                                t.remove(n-p)
        return table

    def limit_potential_solutions(self, base_table):
        """
        Method reduces possible options that can occur.
        It uses two types of other methods:

        1) limiter():
        Runs first.
        Finds values which are stated in table. Next removes them from lists of possible options which are in the same row (or column) as these values.
        for example: [ 1, [1, 2, 3, 4, 5], 4, [2, 4, 5], [1, 3, 5] ] --> [ 1, [2, 3, 5], 4, [2, 5], [3, 5] ]

        2) find_uniqe():
        Runs after limiter.
        If in one row (or column) there are lists of possible options and there is a value that occur only in one of them, it must replace the list where it was.
        for example: [ [1, 2, 3], [1, 3, 5], [1, 3] ] --> [ 2, 5, [1, 3] ]

        Whole method runs in loop unless there are no differences in the following tables.
        In one loop method makes copy of a table. Then reduces the possible options with limiter() and find_uniqe() functions, firstly for rows, secondly for columns.
        Next step is comparing the copy of not changed table with the changed one. If there are differences next loop appears.
        """ # noqa

        x = True
        temporary = base_table
        old_table = copy.deepcopy(temporary)
        while x is True:
            t1 = self.find_unique_in_row(self.limiter_row(temporary))
            new_table = self.find_unique_in_col(self.limiter_column(t1))
            if new_table != old_table:
                x = True
                old_table = copy.deepcopy(new_table)
            else:
                x = False
                finnished_table = new_table
        return finnished_table

    def limiter_row(self, prev_table):
        table = prev_table
        n = self.lenght()
        for i in range(n):
            rows = []
            for j in range(n):
                if type(table[i][j]) is int:
                    rows.append(table[i][j])
            for k in range(n):
                if type(table[i][k]) is list:
                    for elem in rows:
                        if elem in table[i][k]:
                            table[i][k].remove(elem)
        table = self.unlist_single_value(table)
        return table

    def limiter_column(self, prev_table):
        table = prev_table
        n = self.lenght()
        for i in range(n):
            cols = []
            for j in range(n):
                if type(table[j][i]) is int:
                    cols.append(table[j][i])
            for k in range(n):
                if type(table[k][i]) is list:
                    for elem in cols:
                        if elem in table[k][i]:
                            table[k][i].remove(elem)
        table = self.unlist_single_value(table)
        return table

    def find_unique_in_row(self, prev_table):
        new_table = prev_table
        table = self.limiter_row(new_table)
        n = self.lenght()
        for repeat in range(n):
            for i in range(n):
                for value in range(1, n+1):
                    counter = 0
                    for elem in table[i]:
                        if type(elem) is list:
                            if value in elem:
                                counter = counter + 1
                                if counter > 1:
                                    break
                    if counter == 1:
                        index = 0
                        for elem in table[i]:
                            index = index + 1
                            if type(elem) is list:
                                if value in elem:
                                    if value not in table[i]:
                                        table[i].remove(elem)
                                        table[i].insert(index-1, value)
        return table

    def find_unique_in_col(self, prev_table):
        new_table = prev_table
        table = self.limiter_column(new_table)
        n = self.lenght()
        for repeat in range(n):
            for i in range(n):
                col = []
                for j in range(n):
                    col.append(table[j][i])
                for value in range(1, n+1):
                    counter = 0
                    for elem in col:
                        if type(elem) is list:
                            if value in elem:
                                counter = counter + 1
                                if counter > 1:
                                    break
                    if counter == 1:
                        index = 0
                        for elem in col:
                            index = index + 1
                            if type(elem) is list:
                                if value in elem:
                                    if value not in col:
                                        table[index-1][i] = value
        return table

    def is_everything_alright(self, table):
        """
        Checks if the solved table is consistent with guidance and if there are no conflicts.
        """ # noqa
        if self.is_table_correct(table) is True:
            if self.check_guidance_prompts(table) is True:
                return True
            else:
                return False
        else:
            return False

    def check_if_only_ints(self, table):
        """
        Checks if type of every element of table is int (must be positive number).
        :rtype: bool
        """ # noqa
        n = self.lenght()
        for i in range(n):
            for j in range(n):
                each = table[i][j]
                if type(each) is not int or each == 0:
                    return False
        return True

    def check_guidance_prompts(self, table):
        """
        Contains counter() methods (each of them works cognately).
        It compares the growth of the pyraminds' height with the value from guidance.
        If compared values are different, returns False, so that means there are some invalid values on the game table. If values are the same, returns True.
        :rtype: bool
        """ # noqa
        if self.counter_top(table) is False:
            return False
        if self.counter_bottom(table) is False:
            return False
        if self.counter_left(table) is False:
            return False
        if self.counter_right(table) is False:
            return False
        return True

    def counter_top(self, table):
        n = self.lenght()
        for i in range(n):
            value = self.guide()[0][i]
            for j in range(1, n+1):
                if type(table[i][-j]) is not int:
                    raise InvalidTableError
            if value != 0:
                grow = 1
                last_one = table[0][i]
                for k in range(n-1):
                    if table[k+1][i] > last_one:
                        grow = grow + 1
                        last_one = table[k+1][i]
                if grow != value:
                    return False
        return True

    def counter_bottom(self, table):
        n = self.lenght()
        for i in range(n):
            value = self.guide()[1][i]
            for j in range(1, n+1):
                if type(table[i][-j]) is not int:
                    raise InvalidTableError
            if value != 0:
                grow = 1
                last_one = table[-1][i]
                for k in range(1, n):
                    if table[-(k+1)][i] > last_one:
                        grow = grow + 1
                        last_one = table[-(k+1)][i]
                if grow != value:
                    return False
        return True

    def counter_left(self, table):
        n = self.lenght()
        for i in range(n):
            value = self.guide()[2][i]
            for j in range(n):
                if type(table[i][j]) is not int:
                    raise InvalidTableError
            if value != 0:
                grow = 1
                last_one = table[i][0]
                for k in range(n-1):
                    if table[i][k+1] > last_one:
                        grow = grow + 1
                        last_one = table[i][k+1]
                if grow != value:
                    return False
        return True

    def counter_right(self, table):
        n = self.lenght()
        for i in range(n):
            value = self.guide()[3][i]
            for j in range(1, n+1):
                if type(table[i][-j]) is not int:
                    raise InvalidTableError
            if value != 0:
                grow = 1
                last_one = table[i][-1]
                for k in range(1, n):
                    if table[i][-(k+1)] > last_one:
                        grow = grow + 1
                        last_one = table[i][-(k+1)]
                if grow != value:
                    return False
        return True

    # The backtracking methods begins here

    def sort_possible_options(self, table):
        """
        Method runs across the table and finds list of possible options.
        When finds one, appends it to the proper place in a dictionary of options - keys means ammount of elements in list, values means index of position in table
        :return: Returns dictionary where keys represent ammount of elements in lists possible options and values represent indexes of position on table
        :rtype: dictionary
        """ # noqa
        n = self.lenght()
        probs = {}
        for k in range(2, n+1):
            probs[k] = []
            for i in range(n):
                for j in range(n):
                    if type(table[i][j]) is list:
                        if len(table[i][j]) == k:
                            probs[k].append([i, j])
        for k, v in probs.copy().items():
            if v == []:
                del probs[k]
        return probs

    def get_new_root(self, table):
        """
        Backtracking algoritm can be visualised as a roots of tree, and checking every possible connections to the bottom.
        In this method program finds the list of possible options which contains the least elements.
        When it is choosing lists with fewer elements it will have less options to check when the program get back
        :return: returns tuple containing index of list of possible options and the elements which this list contains
        :rtype: tuple
        """ # noqa
        options = self.sort_possible_options(table)
        ways_number = min(options.keys())
        for index in options[ways_number]:
            elems = table[index[0]][index[1]]
            return (index, elems)

    def guess_solution(self, table):
        tree = {}
        ways = {}
        stage = 0
        solved = self.try_to_fill(table, tree, ways, stage)
        return solved

    def get_stage_info(self, table, tree: dict, stage):
        """
        While program is going deeper in solving puzzle, it is making some choices, so it is creating stages where it has to choose.
        At this point it is coping current state of table and passing most significant information further.
        Firstly this method is getting dictionary (tree), which contains information of previous decissions. Then it creates current stage, and adds information (position and elements inside) of one of the lists of possible options for further solving.
        When program is going back and chooses another option it deletes stages which were on the deeper level in relation to current one.

        :param table: current state of table
        :type table: list
        :param tree: tree, which contains information of previous moves/choices of program
        :type tree: dictionary
        :param stage: current stage of the tree
        :type stage: int
        :return: returns tuple which cointains updated tree, and last stage
        :rtype: tuple
        """ # noqa
        unchanged = copy.deepcopy(table)
        tree[stage] = {}
        way = self.get_new_root(table)
        tree[stage]['table'] = unchanged
        tree[stage]['indexes'] = way[0]
        tree[stage]['options'] = way[1]
        involved_keys = []
        for i in tree.keys():
            if len(tree[i]['options']) > 0:
                involved_keys.append(i)
        last_stage = max(involved_keys)
        return (tree, last_stage)
        # ### można spróbować przetestować

    def get_previous_way_info(self, ways: dict, stage):
        """
        For every stage in the 'tree' it deletes the value from 'options' that has been choosen to try.
        In that case this method appends options that has been already tried in current state.

        :param ways: dictionary with previous moves
        :type ways: dictionary
        :return: updated ways dictionary
        :rtype: dictionary
        """ # noqa
        ways[stage] = []
        return ways

    def fill_table_with(self, table, index, attempt, tree, stage):
        """
        Interposes particular list of possible options with one of its elements and solves the table with this value.

        :param table: current state of table
        :type table: list
        :param index: indexes of position on table
        :type index: list
        :param attempt: value that will be interposed
        :type attempt: int
        :param tree: tree of previous stages
        :type tree: dictionary
        :param stage: stage on which program is making changes
        :type stage: int
        """ # noqa

        table[index[0]][index[1]] = attempt
        self.limit_potential_solutions(table)
        if self.check_if_only_ints(table) is True:
            return (table, tree, stage)
        else:
            stage = stage + 1
            upd_tree = self.get_stage_info(table, tree, stage)[0]
            return (table, upd_tree, stage)

    def try_to_fill(self, table, tree, ways, stage, backing=False):
        """"
        Method gets information from last stage. Then fills the table with one of the possible options from list of these options and solves for this combination.
        Next checks if the table is fully filled with ints. If not, the method is running again and agian, until every position of table will be a number.
        When table is completed, is_everything_allright() function tests its cerrectness. If so, program returns final solution.
        In other case method must step some stages back and try filling table in other way.
        Whole program runs until it finds the correct answer.

        :param table: current state of table
        :type table: list
        :param tree: tree of previous stages
        :type tree: dictionary
        :param ways: dictionary with previous moves
        :type ways: dictionary
        :param stage: stage on which program is making changes
        :type stage: int
        :param backing: information if algorithm is going back (default False)
        :type backing: bool, optional
        :return: solved puzzle if it is solvable
        """ # noqa
        if backing is False:
            info = self.get_stage_info(table, tree, stage)
            ways = self.get_previous_way_info(ways, stage)
            index = info[0][info[1]]['indexes']
            attempt = info[0][info[1]]['options']
        else:
            index = tree[stage]['indexes']
            attempt = tree[stage]['options']

        for i in attempt:
            if i in tree[stage]['options']:
                tree[stage]['options'].remove(i)
                ways[stage].append(i)
            new_one = self.fill_table_with(table, index, i, tree, stage)
            new_table = new_one[0]
            upd_tree = new_one[1]
            next_stage = new_one[2]
            if self.check_if_only_ints(new_table) is False:
                return self.try_to_fill(new_table, upd_tree, ways, next_stage)
            else:
                if self.is_everything_alright(new_table) is True:
                    correct_solution = copy.deepcopy(table)
                    return correct_solution
                else:
                    if len(tree[stage]['options']) != 0:
                        q_tab = upd_tree[stage]['table']
                        back = True
                        return self.try_to_fill(q_tab, tree, ways, stage, back)
                    else:
                        involved_keys = []
                        for e in tree.keys():
                            if len(tree[e]['options']) > 0:
                                involved_keys.append(e)
                        stage = max(involved_keys)
                        q_tab = upd_tree[stage]['table']
                        back = True
                        return self.try_to_fill(q_tab, tree, ways, stage, back)
