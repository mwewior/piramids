import copy


class InvalidGuideError(Exception):
    """
    Raised when guide is in invalid format
    """
    pass


class PyraminInterposeError(Exception):
    """
    Raised when there is conflict while solving
    """
    pass


class InvalidTableError(Exception):
    """
    Raised when there is conflict on table;
    Usually when:
        1) some table's values exceed maximum height
        2) there are same values in row or column
    """
    pass


class SubstituteError(Exception):
    pass


class Solver:
    """
    class Solver. Contains atributes:
        :param guide: guide for solving table
        :type guide: list
            :note: list of lists ( always 4 lists - all the same lenght)

        :param lenght: table's lenght
        :type lenght: int

        :param generate_raw_table: creates blank table for future solvings
        :type generate_raw_table: list
            :note: table is a list of lists. contains N lists of N elements\
                (N is a self.lenght() value), fills them as '0'

        :param set_table: overwrites the  previous table with new solutions
        :type set_table: list

        :param is_correct: checks if there is no contradiction while solving
        :type is_correct: Bool

        :param solve_if_X: reads the guide and overwrites
        proper values in the table
        :type solve_if_X: list

    """

    def __init__(self, guide: list):

        if len(guide) != 4:
            raise InvalidGuideError(
                'Podano niepoprawną podpowiedź. \
Liczba wierszy musi być równa 4.'
                )

        for i in range(3):
            if len(guide[i]) != len(guide[i+1]):
                raise InvalidGuideError(
                    'Podano niepoprawną podpowiedź. \
Wszystkie wiersze muszą być tej samej długości.'
                )

        for i in range(4):
            for j in range(len(guide[i])):
                if isinstance(guide[i][j], str):
                    if guide[i][j].isdigit():
                        guide[i][j] = int(guide[i][j])
                    else:
                        raise InvalidGuideError(
                            'Podano niepoprawną podpowiedź. \
W podpowiedzi mogą znajdować się jedynie liczby.'
                        )
                if isinstance(guide[i][j], float) or int(guide[i][j]) < 0:
                    raise InvalidGuideError(
                        'Podano niepoprawną podpowiedź. \
Liczba widzianych piramid musi być całkowitą liczbą dodatnią.'
                        )
                if int(guide[i][j]) > len(guide[i]):
                    raise InvalidGuideError(
                        'Podano niepoprawną podpowiedź. \
Liczba widzianych piramid nie może przekraczać długości boku planszy.'
                        )

        self._guide = guide
        self._lenght = int(len(guide[0]))

    def guide(self):
        """
        zwraca tabelę podpowiedzi
        """
        return self._guide

    def lenght(self):
        """
        zwraca długość boku planszy
        """
        return self._lenght

    def generate_raw_table(self):
        """
        tworzy pustą planszę, na którą następnie będą nanoszone \
wartości wysokości piramid
        """
        n = int(self.lenght())
        blank = []
        for i in range(n):
            blank.append([])
            for j in range(n):
                blank[i].append(0)
        return blank

    def set_table(self, table=None):
        if table is None:
            overwritten_table = self.generate_raw_table()
        else:
            overwritten_table = table
            n = self.lenght()
            for i in range(n):
                for j in range(n):
                    if type(overwritten_table[i][j]) is int:
                        if int(overwritten_table[i][j]) > n:
                            raise InvalidTableError(
                                "Height of pyramid on table is incorrect"
                            )
        return overwritten_table

    def is_row_correct(self, table=None):
        """
        cheks if the numbers occure only once in the row of the table
        """
        n = self.lenght()
        if table is None:
            pass
        else:
            for i in range(n):
                a = []
                for elem in table[i]:
                    if type(elem) is int and elem != 0:
                        a.append(elem)
                    a.sort()
                b = list(set(a))
                if len(a) == 0:
                    pass
                if a != b:
                    return False
        return True

    def is_column_correct(self, table=None):
        """
        cheks if the numbers occure only once in the column of the table
        """
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
                if len(column) == 0:
                    pass
                if column != list(set(column)):
                    return False
        return True

    def is_table_correct(self, table=None):
        row = self.is_row_correct(table)
        col = self.is_column_correct(table)
        if row is True and col is True:
            return True
        else:
            return False

    def interposer(self, table, in1, in2, v):
        """
        (table is a list of list)
        where:
            id1 - indexes of the first list
            id2 - indexes of the second list
            v - value that will overwrite 0
        """
        if table[in1][in2] == 0 or table[in1][in2] == v:
            table[in1][in2] = v
        else:
            raise PyraminInterposeError()

    def solve_if_ONE(self, prev_table=None):
        table = self.set_table(prev_table)
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
        return self.set_table(table)

    def solve_if_N(self, prev_table=None):
        table = self.set_table(prev_table)
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
        return self.set_table(table)

    def zero_into_list(self, prev_table=None):
        table = self.set_table(prev_table)
        n = self.lenght()
        for i in range(n):
            for j in range(n):
                if table[i][j] == 0:
                    table[i][j] = list(range(1, n+1))
        return table

    def reduce_from_guide_overall(self, prev_table):
        t1 = self.reduce_from_guide_top(prev_table)
        t2 = self.reduce_from_guide_bottom(t1)
        t3 = self.reduce_from_guide_left(t2)
        table = self.reduce_from_guide_right(t3)
        return self.unlist_single_value(table)

    def reduce_from_guide_top(self, prev_table):
        table = self.set_table(prev_table)
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

    def reduce_from_guide_bottom(self, prev_table):
        table = self.set_table(prev_table)
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

    def reduce_from_guide_left(self, prev_table):
        table = self.set_table(prev_table)
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

    def reduce_from_guide_right(self, prev_table):
        table = self.set_table(prev_table)
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

    def unlist_single_value(self, prev_table):
        table = prev_table
        n = self.lenght()
        for i in range(n):
            for j in range(n):
                if type(table[i][j]) is list:
                    if len(table[i][j]) == 1:
                        table[i][j] = table[i][j][0]
        return table

    def limit_potential_solutions(self, base_table):
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

    def check_guidance_prompts(self, table):
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
        """
        compare the growth of the pyramids with guidance values
        """
        n = self.lenght()
        for i in range(n):
            value = self.guide()[0][i]
            for j in range(1, n+1):
                if type(table[i][-j]) is not int:
                    raise SubstituteError
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
        """
        compare the growth of the pyramids with guidance values
        """
        n = self.lenght()
        for i in range(n):
            value = self.guide()[1][i]
            for j in range(1, n+1):
                if type(table[i][-j]) is not int:
                    raise SubstituteError
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
        """
        compare the growth of the pyramids with guidance values
        """
        n = self.lenght()
        for i in range(n):
            value = self.guide()[2][i]
            for j in range(n):
                if type(table[i][j]) is not int:
                    raise SubstituteError
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
        """
        compare the growth of the pyramids with guidance values
        """
        n = self.lenght()
        for i in range(n):
            value = self.guide()[3][i]
            for j in range(1, n+1):
                if type(table[i][-j]) is not int:
                    raise SubstituteError
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

    def check_if_only_ints(self, table):
        n = self.lenght()
        for i in range(n):
            for j in range(n):
                each = table[i][j]
                if type(each) is not int or each == 0:
                    return False
        return True

    def is_everything_alright(self, table):
        if self.is_table_correct(table) is True:
            if self.check_guidance_prompts(table) is True:
                return table
            else:
                return False
        else:
            return False

    def sort_possible_options(self, table):
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
        options = self.sort_possible_options(table)
        ways_number = min(options.keys())
        for index in options[ways_number]:
            elems = table[index[0]][index[1]]
            return (index, elems)

    # # # # # # #

    def guess_solution(self, table):
        tree = {}
        stage = 0
        self.get_stage_info(table, tree, stage)
        pass

    def get_stage_info(self, table, tree: dict, stage):
        unchanged = copy.deepcopy(table)
        tree[stage] = {}
        way = self.get_new_root(table)
        tree[stage]['table'] = unchanged
        tree[stage]['indexes'] = way[0]
        tree[stage]['options'] = way[1]
        last_stage = max(tree.keys())
        return (tree, last_stage)
        # ### można spróbować przetestować

    def fill_table_with(self, table, index, attempt, tree, stage):
        table[index[0]][index[1]] = attempt
        self.limit_potential_solutions(table)
        stage = stage + 1
        updated_tree = self.get_stage_info(table, tree, stage)
        return (table, updated_tree, stage)

    def try_to_fill(self, table, tree, stage):

        # jescze do dopracowania

        info = self.get_stage_info(table, tree, stage)
        index = info[0][info[1]]['indexes']
        attempt = info[0][info[1]]['options']
        for i in attempt:
            new_one = self.fill_table_with(table, index, attempt, tree, stage)
            new_table = new_one[0]
            updated_tree = new_one[1]
            next_stage = new_one[2]
            if self.check_if_only_ints(new_table) is False:
                self.try_to_fill(new_table, updated_tree, next_stage)
            else:
                if self.is_everything_alright(new_table) is True:
                    return new_table
                else:
                    del updated_tree[f'{next_stage}']
                    stage = next_stage - 1
                    pass
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                                                     #
        #        |.|                                          #
        #        /\                                           #
        #       /\                                            #
        #   źle1  źle2                                        #
        #                                                     #
        #   nasuwa się pytanie jak wróicić z źle2 do |.|      #
        #   i pójść w prawo a nie w lewo                      #
        #       (np jest pomysł żeby usunąc wartość,          #
        #       którą wcześniej się wybrało)                  #
        #                                                     #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        pass

    # # # # # # # #

    # poprzednie notatki
    """
    tutaj wybiera jedeną z opcji ze słownika z indeksami
    patrzy jakie opcje są dostępne do wstawienia
    wybiera jedna -> wstawia -> limiter() itd
    zapisuje tablice

    jesli tablica jest juz zrobiona sprawdza czy poprawna

    jesli jeszcze nie ma samych intów w tablicy
    zapisuje jakos obecy stan
    i jeszcze raz robi to podstawianie

    # takie chodzenie po drzewku
    """

    # def try_to_fill(self, table):
    #     # n = self.lenght()
    #     unchanged = []
    #     unchanged.append(copy.deepcopy(table))
    #     options = self.sort_possible_options(table)
    #     for k in range(min(options.keys()), max(options.keys())+1):
    #         for elem in options[k]:
    #             indexes = elem
    #             for item in table[indexes[0]][indexes[1]]:
    #                 new = self.fill_table_with(table, indexes, item)
    #                 if type(new) is list:
    #                     return new
    #                 else:
    #                     # table = unchanged
    #                     pass

    # def fill_table_with(self, table, indexes: list, attempt: int):
    #     n = self.lenght()
    #     table[indexes[0]][indexes[1]] = attempt
    #     self.limit_potential_solutions(table)
    #     for i in range(n):
    #         for j in range(n):
    #             if type(table[i][j]) is not int:
    #                 self.try_to_fill(table)
    #     if self.is_table_correct(table) is True:
    #         if self.check_guidance_prompts(table) is True:
    #             return table
    #         else:
    #             return None
    #     else:
    #         return None

    ###

    # def old_try_to_fill(self, table):
    #     n = self.lenght()
    #     # unchanged = copy.deepcopy(table)
    #     options = self.sort_possible_options(table)
    #     for k in range(2, n+1):
    #         # options = self.sort_possible_options(table)
    #         if k in options.keys():
    #             for i in range(len(options[k])):
    #                 indexes = options[k][i]
    #                 base_list = table[indexes[0]][indexes[1]]
    #                 if type(base_list) is list:
    #                     for a in base_list:
    #                         new = self.old_fill_table_with(table, indexes, a)
    #                         if new[0] is True:
    #                             return new[1]
    #         # else:
    #         #     pass

    # def old_fill_table_with(self, table, indexes, attempt):
    #     unchanged = copy.deepcopy(table)
    #     n = self.lenght()
    #     table[indexes[0]][indexes[1]] = attempt
    #     potential_one = self.limit_potential_solutions(table)
    #     for i in range(n):
    #         for j in range(n):
    #             if type(table[i][j]) is not int:
    #                 self.old_try_to_fill(potential_one)
    #     if self.is_table_correct(potential_one) is True:
    #         if self.check_guidance_prompts(potential_one) is True:
    #             return (True, potential_one)
    #     return (False, unchanged)

    # """
    # teraz musi z tych wspołrzednych wybierac kolejne listy
    # i podstawia jenda z potencjalnych rozwiazan z tej listy
    # potem prowadzone sa te limitery dla danej wartosci
    # nastepnie sprawdza poprawnosc i countery()
    # """
    #
    # """
    # jesli jest cos nie tak to ma wrocic i wybrac kolejne elementy z list
    # i tak do konca czyli az znajdzie poprawna tablice
    #
    # tworzy kopie tablicy i jesli bedzie tylko jedna tablica
    # to bedzie to ostateczna
    # """
