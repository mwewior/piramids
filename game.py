from solver import Solver


def insert_guide():
    guide = Solver([
        # podpowiedź podana przez użytkownika jako wejście
    ])
    return guide


def main():
    no_solution = 'There is no solutioin. Puzzle cannot be solved.'
    guide = insert_guide()
    table0 = guide.set_table()
    table_over = guide.solve_if_N(guide.solve_if_ONE(table0))
    if guide.is_table_correct(table_over) is False:
        return no_solution
    # kolejność następnych funkcji
    # 1) zero_into_list()
    # 2) reduction_from_guide()
    # 3) limit_potential_solutions
    #       +++
    #           trzeba jeszcze rozważyć to, że wszystkie mogą być listą
    #           i jesli w rzedzie/kolumnie jakis element jest tylko
    #           w jednej liscie to on musi wyjsc z listy
    #           i on zostaje umieszczony w tabeli
    #       +++
    #
    #  ### ==> na ten moment mielibysmy zrobiony etap E4 a nawet chyba E5

    # 1) DONE - mamy wprowadzone warunki konieczne - sprawdzenie dla N i dla 1
    #    (jeśli one nie są okej to na pewno jest źle)
    # 2) DONE - zera zamieniamy na listy zawierające od 1 do N
    # 3) DONE - usuwamy najwyższe wartości stojące przy podpowiedzi
    # 4) NOT YET - usuwamy z list te wartości, które już są w rzędzie(kolumnie)
    # 5) porównuje listy - jeśli w jakiejś liście jest taki element,
    #    który nie pojawiwa się w innych to go wpisujemy w pozycje na planszy
    # 6) kroki 4 i 5 powtarzamy dopóki można
    # 7) gdy już nie da się skróić bardziej, to trzeba uwzględnić te opcje,
    #    które są zgodne z podpowiedzią


if __name__ == '__main__':
    if type(main()) is list:
        for rows in main():
            print(rows)
    else:
        print(main())
