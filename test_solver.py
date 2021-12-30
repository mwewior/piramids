from solver import Solver, WrongGuideError
import pytest


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
    with pytest.raises(WrongGuideError):
        Solver([
            ['/@fg', 0, 1, '['],
            [0, 'a', 3, 4],
            [2, '. 12x6h', 1, 0],
            ['"', 1, 0, 'Kói=OnNĘ']
        ])


def test_guide_valid_rows():
    with pytest.raises(WrongGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0]
            ])
    with pytest.raises(WrongGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 2],
            [4, 0, 1, 0]
            ])


def test_guide_different_row_lenght():
    with pytest.raises(WrongGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0],
            [0, 0, 1, 0],
            [4, 0, 1, 0]
            ])
    with pytest.raises(WrongGuideError):
        Solver([
            [1, 0, 1, 0],
            [0, 1, 0, 3],
            [0, 0, 1, 0],
            [4, 0, 1, 0, 2]
            ])
    with pytest.raises(WrongGuideError):
        Solver([
            [],
            [0, 1, 0, 3, 2],
            [0, 0],
            [4, 0, 1, 0, 2, 1]
            ])


def test_guide_height_over_lenght():
    with pytest.raises(WrongGuideError):
        Solver([
            [1, 0, 9, 0],
            [0, 1, 0, 30],
            [0, 0, 1, 10],
            [0, 111, 0, 2]
            ])


def test_guide_negative_height():
    with pytest.raises(WrongGuideError):
        Solver([
            [-1, 0, 9, 0],
            [0, 1, 0, -5],
            [0, 0, 1, 4],
            [0, -71, 0, -2]
            ])


def test_guide_height_as_float():
    with pytest.raises(WrongGuideError):
        Solver([
            [1, 0, 0.9, 0.0],
            [0, 1, 0, 3.0],
            [0, 0, 1, 1.167],
            [0, 9.01, 0, 2.0]
            ])
