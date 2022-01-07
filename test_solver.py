from solver import Solver
from solver import PyraminInterposeError, InvalidGuideError
import pytest


# tests basic functions (guide, lenght)

def test_guide_valid():
    guide1 = Solver([
        [1, 0, 3, 0],
        [2, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 4, 0, 2]
        ])
    assert guide1.guide() == [
        [1, 0, 3, 0],
        [2, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 4, 0, 2]
        ]


def test_guide_lenght():
    guide1 = Solver([
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0]
        ])
    assert guide1.lenght() == 4
    guide2 = Solver([
        [5, 3, 0, 1, 0],
        [0, 1, 0, 0, 2],
        [4, 0, 0, 1, 0],
        [0, 1, 1, 0, 0]
        ])
    assert guide2.lenght() == 5


def test_guide_number_str_instead_of_int():
    guide1 = Solver([
        ['2', '0', 1, 0],
        [0, 1, 3, 4],
        [2, 0, '1', 0],
        ['4', 1, 0, '3']
        ])
    assert guide1.guide() == [
        [2, 0, 1, 0],
        [0, 1, 3, 4],
        [2, 0, 1, 0],
        [4, 1, 0, 3]
        ]


def test_guide_not_numbers():
    with pytest.raises(InvalidGuideError):
        Solver([
            ['/@fg', 0, 1, '['],
            [0, 'a', 3, 4],
            [2, '. 12x6h', 1, 0],
            ['"', 1, 0, 'Kói=OnNĘ']
        ])


def test_guide_valid_rows():
    with pytest.raises(InvalidGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0]
            ])
    with pytest.raises(InvalidGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 2],
            [4, 0, 1, 0]
            ])


def test_guide_different_row_lenght():
    with pytest.raises(InvalidGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0],
            [0, 0, 1, 0],
            [4, 0, 1, 0]
            ])
    with pytest.raises(InvalidGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0, 3],
            [0, 0, 1, 0],
            [4, 0, 1, 0, 2]
            ])
    with pytest.raises(InvalidGuideError):
        Solver([
            [],
            [0, 1, 0, 3, 2],
            [0, 0],
            [4, 0, 1, 0, 2, 1]
            ])


def test_guide_height_over_lenght():
    with pytest.raises(InvalidGuideError):
        Solver([
            [1, 0, 9, 0],
            [0, 1, 0, 30],
            [0, 0, 1, 10],
            [0, 111, 0, 2]
            ])


def test_guide_negative_height():
    with pytest.raises(InvalidGuideError):
        Solver([
            [-1, 0, 9, 0],
            [0, 1, 0, -5],
            [0, 0, 1, 4],
            [0, -71, 0, -2]
            ])


def test_guide_height_as_float():
    with pytest.raises(InvalidGuideError):
        Solver([
            [1, 0, 0.9, 0.0],
            [0, 1, 0, 3.0],
            [0, 0, 1, 1.167],
            [0, 9.01, 0, 2.0]
            ])


# tests table creator

def test_raw_table_create():
    guide1 = Solver([
        [2, 0, 1, 0],
        [0, 1, 3, 4],
        [2, 0, 1, 0],
        [4, 1, 0, 3]
        ])
    assert guide1.generate_raw_table() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    guide2 = Solver([
        [3, 0, 1, 0, 6, 0, 0, 3],
        [0, 2, 0, 8, 0, 4, 0, 0],
        [0, 0, 4, 0, 0, 2, 0, 0],
        [0, 3, 0, 0, 7, 0, 5, 0]
    ])
    assert guide2.generate_raw_table() == [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    guide3 = Solver([
        [0, 1],
        [2, 0],
        [0, 0],
        [0, 0]
    ])
    assert guide3.generate_raw_table() == [
        [0, 0],
        [0, 0]
    ]


# tests filling table when there is 1 in guide

def test_if_ONE_in_row_0():
    guide1 = Solver([
        [0, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ])
    assert guide1.solve_if_ONE() == [
        [0, 0, 4, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # with partly completed table
    assert guide1.solve_if_ONE([
        [0, 0, 4, 0],
        [0, 0, 3, 0],
        [0, 0, 2, 0],
        [0, 0, 1, 0]
    ]) == [
        [0, 0, 4, 0],
        [0, 0, 3, 0],
        [0, 0, 2, 0],
        [0, 0, 1, 0]
    ]


def test_if_ONE_in_row_1():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ])
    assert guide1.solve_if_ONE() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 4, 0, 0]
    ]

    # with partly completed table
    assert guide1.solve_if_ONE([
        [0, 3, 0, 1],
        [0, 2, 3, 0],
        [3, 1, 0, 0],
        [0, 4, 0, 0]
    ]) == [
        [0, 3, 0, 1],
        [0, 2, 3, 0],
        [3, 1, 0, 0],
        [0, 4, 0, 0]
    ]


def test_if_ONE_in_row_2():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
        ])
    assert guide1.solve_if_ONE() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # with partly completed table
    assert guide1.solve_if_ONE([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 0]
    ]) == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 0]
    ]


def test_if_ONE_in_row_3():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
        ])
    assert guide1.solve_if_ONE() == [
        [0, 0, 0, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # with partly completed table
    assert guide1.solve_if_ONE([
        [3, 1, 4, 2],
        [1, 2, 3, 0],
        [4, 3, 2, 1],
        [2, 4, 1, 3]
    ]) == [
        [3, 1, 4, 2],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 4, 1, 3]
    ]


def test_if_ONE_in_mix():
    guide = Solver([
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
        ])

    assert guide.solve_if_ONE() == [
        [0, 4, 0, 0],
        [4, 0, 0, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0]
    ]

    # with partly completed table
    assert guide.solve_if_ONE([
        [0, 4, 0, 1],
        [0, 2, 3, 0],
        [2, 3, 1, 0],
        [3, 1, 0, 0]
    ]) == [
        [0, 4, 0, 1],
        [4, 2, 3, 0],
        [2, 3, 1, 4],
        [3, 1, 0, 0]
    ]


def test_if_ONE_invalid_previous_table():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]
        ])
    with pytest.raises(PyraminInterposeError):
        guide1.solve_if_ONE([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 3]
            ])

    guide2 = Solver([
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0]
        ])
    with pytest.raises(PyraminInterposeError):
        guide2.solve_if_ONE([
            [0, 4, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 4, 1]
            ])


# tests filling table when there is n in guide

def test_if_N_in_row_0():
    guide1 = Solver([
        [0, 0, 4, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ])
    assert guide1.solve_if_N() == [
        [0, 0, 1, 0],
        [0, 0, 2, 0],
        [0, 0, 3, 0],
        [0, 0, 4, 0]
        ]

    # with partly completed table
    assert guide1.solve_if_N([
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]) == [
        [0, 0, 1, 0],
        [0, 0, 2, 0],
        [0, 0, 3, 0],
        [0, 0, 4, 0]
        ]


def test_if_N_in_row_1():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 4, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ])
    assert guide1.solve_if_N() == [
        [0, 4, 0, 0],
        [0, 3, 0, 0],
        [0, 2, 0, 0],
        [0, 1, 0, 0]
        ]

    # with partly completed table
    assert guide1.solve_if_N([
        [0, 0, 0, 0],
        [0, 3, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ]) == [
        [0, 4, 0, 0],
        [0, 3, 0, 0],
        [0, 2, 0, 0],
        [0, 1, 0, 0]
        ]


def test_if_N_in_row_2():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0]
        ])
    assert guide1.solve_if_N() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 2, 3, 4]
    ]

    # with partly completed table
    assert guide1.solve_if_N([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 2, 3, 4]
    ]) == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 2, 3, 4]
    ]


def test_if_N_in_row_3():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 0]
        ])
    assert guide1.solve_if_N() == [
        [4, 3, 2, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # with partly completed table
    assert guide1.solve_if_N([
        [4, 0, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]) == [
        [4, 3, 2, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]


def test_if_N_in_mix():
    guidemix = Solver([
        [4, 0, 0, 0],
        [0, 0, 0, 4],
        [4, 0, 0, 0],
        [0, 0, 0, 4]
    ])
    assert guidemix.solve_if_N() == [
        [1, 2, 3, 4],
        [2, 0, 0, 3],
        [3, 0, 0, 2],
        [4, 3, 2, 1]
    ]


def test_if_N_invalid_previous_table():
    guide1 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 0]
        ])
    with pytest.raises(PyraminInterposeError):
        guide1.solve_if_N([
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
        )

    guide2 = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0]
        ])
    with pytest.raises(PyraminInterposeError):
        guide2.solve_if_N([
            [0, 0, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 4, 1]]
        )


def test_if_ONE_and_N_mixed():
    guide = Solver([
        [0, 1, 4, 2],
        [0, 4, 0, 2],
        [0, 0, 0, 0],
        [2, 0, 1, 0]
    ])

    x = guide.solve_if_N(guide.solve_if_ONE())
    assert x == [
        [0, 4, 1, 0],
        [0, 3, 2, 0],
        [0, 2, 3, 4],
        [0, 1, 4, 0]
    ]

    tip = Solver([
        [1, 2, 5, 4, 2, 6],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0]
    ])

    y = tip.solve_if_ONE()
    assert tip.solve_if_N(y) == [
        [6, 5, 4, 3, 2, 1],
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 6]
    ]


def test_is_correct_true():
    random = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    table = [
        [0, 4, 0, 1],
        [4, 2, 3, 0],
        [2, 3, 1, 4],
        [3, 1, 0, 0]
        ]
    assert random.is_rows_and_cols_correct(table) is True

    another = Solver([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])
    x8 = [
        [7, 5, 1, 2, 3, 4, 6],
        [6, 3, 4, 7, 2, 1, 5],
        [5, 4, 2, 3, 6, 7, 1],
        [4, 1, 6, 0, 5, 3, 2],
        [3, 2, 0, 1, 7, 5, 4],
        [2, 0, 7, 5, 1, 6, 3],
        [1, 6, 5, 0, 4, 2, 7],
    ]
    assert another.is_rows_and_cols_correct(x8) is True


def test_is_correct_false():
    first = Solver([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    table1 = [
        [0, 2, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    table2 = [
        [0, 1, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ]
    table3 = [
        [0, 3, 2, 0],
        [0, 3, 0, 0],
        [4, 0, 1, 4],
        [0, 2, 2, 0]
    ]
    assert first.is_rows_and_cols_correct(table1) is False
    assert first.is_rows_and_cols_correct(table2) is False
    assert first.is_rows_and_cols_correct(table3) is False
