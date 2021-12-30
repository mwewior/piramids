class WrongGuideError(Exception):
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
            raise WrongGuideError(
                'Podano niepoprawną podpowiedź. \
Liczba wierszy musi być równa 4.'
                )

        for i in range(3):
            if len(guide[i]) != len(guide[i+1]):
                raise WrongGuideError(
                    'Podano niepoprawną podpowiedź. \
Wszystkie wiersze muszą być tej samej długości.'
                )

        for i in range(4):
            for j in range(len(guide[i])):
                if isinstance(guide[i][j], str):
                    if guide[i][j].isdigit():
                        guide[i][j] = int(guide[i][j])
                    else:
                        raise WrongGuideError(
                            'Podano niepoprawną podpowiedź. \
W podpowiedzi mogą znajdować się jedynie liczby.'
                        )
                if isinstance(guide[i][j], float) or int(guide[i][j]) < 0:
                    raise WrongGuideError(
                        'Podano niepoprawną podpowiedź. \
Liczba widzianych piramid musi być całkowitą liczbą dodatnią.'
                        )
                if int(guide[i][j]) > len(guide[i]):
                    raise WrongGuideError(
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
                table[0][row] = n
            # patrząc od dołu
            if self.guide()[1][row] == 1:
                table[n-1][row] = n
            # patrząc od lewej
            if self.guide()[2][row] == 1:
                table[row][0] = n
            # patrząc od prawej
            if self.guide()[3][row] == 1:
                table[row][n-1] = n
        return table

    def solve_if_N(self):
        table = self.generate_raw_table()
        n = self.lenght()
        for row in range(n):
            for col in range(n):
                # patrząc od  góry
                if self.guide()[0][col] == n:
                    for value in range(n):
                        table[value][col] = value + 1
                # patrząc od dołu
                if self.guide()[1][col] == n:
                    i = list(range(n))
                    for value in i:
                        table[value][col] = i[-value - 1] + 1
                # patrząc od lewej
                if self.guide()[2][col] == n:
                    for value in range(n):
                        table[col][value] = value + 1
                # patrząc od prawej
                if self.guide()[3][col] == n:
                    i = list(range(n))
                    for value in i:
                        table[col][value] = i[-value - 1] + 1
        return table
