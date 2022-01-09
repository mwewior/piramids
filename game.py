from solver import Solver


def insert_guide():
    guide = Solver([
        # podpowiedź podana przez użytkownika jako wejście
    ])
    return guide


def main():
    no_solution = 'There is no solutioin. Puzzle cannot be solved.'
    guide = insert_guide()
    table = guide.set_table()
    guide.solve_if_N(guide.solve_if_ONE(table))
    if guide.is_table_correct(table) is False:
        return no_solution
    guide.zero_into_list(table)
    guide.reduce_from_guide_overall(table)
    guide.limit_potential_solutions(table)

    # na tym etapie mamy utworzoną tablicę, na której naniesione
    # są już częściowo odpoweidzi.
    # Tam, gdzie nie da się jednoznczanie wpisać wartości
    # jest lista możliwych opcji.
    #
    # Teraz potrzeba funkcji, które:
    #   - podstawią jakąś opcję, która jest najbardziej prawdopodobna,
    #   - limiter() z tą opcją
    #   - sprawdzająca, czy wartość jest poprawna i
    #     czy zgadza się z wartością z guide'a ( counter() )
    #
    #   - jeśli jescze się nie rozwiązało powtarzamy


if __name__ == '__main__':
    if type(main()) is list:
        for rows in main():
            print(rows)
    else:
        print(main())
