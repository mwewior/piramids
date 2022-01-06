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
                if int(overwritten_table[i][j]) > n:
                    raise InvalidTableError(
                        "Height of pyramid on table is incorrect"
                    )
        return overwritten_table

    def is_rows_and_cols_correct(self, table=None):

        # w pliku main będzie trzeba dodać,
        # że jeśli is_rows_and_cols_coorect is False ->
        # -> raise InvalidTableError(
        #         " There are same pyramids in one row"
        #    )

        # trzeba uwzględnić to, że np [2, 0, 0, 3] jest ok,
        # (set zrobi z niej [2, 0, 3])

        n = self.lenght()
        if table is None:
            pass
        else:
            for i in range(n):
                a = table[i]
                b = list(set(table[i]))
                if a != b:
                    return False
                column = []
                for j in range(n):
                    column.append(table[i][j])
                    if column != list(set(column)):
                        return False
            return True

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

# ### wstępne implementacje funkcji wyjściowych

# def final_table(self):
#     pass

# def show(self):
#     if self.final_table():
#         for row in self.final_table():
#             for point in range(len(row)):
#                 row[point] = str(row[point])
#         str_table = []
#         for old_row in self.final_table():
#             new_row = "".join(old_row)
#             str_table.append(new_row)
#         output_string = '\n'
#         for z in str_table:
#             str_row = f'{z}\n'
#             output_string += str_row
#         return output_string
#     else:
#         return f'zadania nie da się rozwiązać.'
