class InvalidGuideError(Exception):
    pass


class PyraminInterposeError(Exception):
    pass


class Solver:
    """
    class Solver:
    próbuje rozwiązać zadanie z podanej podpowiedzi

    (podpowiedź jest zapisana jako lista list -
        - zawsze 4 wiersze o liczbie kolumn równej długości boku planszy)
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
        return overwritten_table

    def solve_if_ONE(self, prev_table=None):
        table = self.set_table(prev_table)
        n = self.lenght()
        for row in range(n):
            # patrząc od góry
            if self.guide()[0][row] == 1:
                if table[0][row] == 0 or table[0][row] == n:
                    table[0][row] = n
                else:
                    raise PyraminInterposeError()
            # patrząc od dołu
            if self.guide()[1][row] == 1:
                if table[n-1][row] == 0 or table[n-1][row] == n:
                    table[n-1][row] = n
                else:
                    raise PyraminInterposeError()
            # patrząc od lewej
            if self.guide()[2][row] == 1:
                if table[row][0] == 0 or table[row][0] == n:
                    table[row][0] = n
                else:
                    raise PyraminInterposeError()
            # patrząc od prawej
            if self.guide()[3][row] == 1:
                if table[row][n-1] == 0 or table[row][n-1] == n:
                    table[row][n-1] = n
                else:
                    raise PyraminInterposeError()
        return self.set_table(table)

    def solve_if_N(self, prev_table=None):
        table = self.set_table(prev_table)
        n = self.lenght()
        for col in range(n):
            # patrząc od  góry
            if self.guide()[0][col] == n:
                for val in range(n):
                    if table[val][col] == 0 or table[val][col] == val + 1:
                        table[val][col] = val + 1
                    else:
                        raise PyraminInterposeError()
            # patrząc od dołu
            if self.guide()[1][col] == n:
                i = list(range(n))
                for val in i:
                    value = i[-val - 1] + 1
                    if table[val][col] == 0 or table[val][col] == value:
                        table[val][col] = value
                    else:
                        raise PyraminInterposeError()
            # patrząc od lewej
            if self.guide()[2][col] == n:
                for val in range(n):
                    if table[col][val] == 0 or table[col][val] == val + 1:
                        table[col][val] = val + 1
                    else:
                        raise PyraminInterposeError()
            # patrząc od prawej
            if self.guide()[3][col] == n:
                i = list(range(n))
                for val in i:
                    value = i[-val - 1] + 1
                    if table[col][val] == 0 or table[col][val] == value:
                        table[col][val] = value
                    else:
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
