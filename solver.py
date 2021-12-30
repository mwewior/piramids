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
        newone = []
        for i in range(n):
            newone.append([])
            for j in range(n):
                newone[i].append(0)
        return newone

    def solve_if_ONE(self):
        table = self.generate_raw_table()
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
        return table

    def solve_if_N(self):
        table = self.generate_raw_table()
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
        return table
