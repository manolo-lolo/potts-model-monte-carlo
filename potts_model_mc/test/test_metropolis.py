from interaction import kronecker
from metropolis import calculate_interaction_of_one_spin, calculate_energy_difference
import numpy as np
import pytest

test_field = np.array([
    [0, 1, 2, 2],
    [3, 2, 2, 2],
    [0, 2, 2, 1]
])


@pytest.mark.parametrize('x, y, expected', [
    (0, 0, -0 * 2),
    (0, 1, -0 * 2),
    (0, 2, -2 * 2),
    (0, 3, -2 * 2),
    (1, 0, -0 * 2),
    (1, 1, -2 * 2),
    (1, 2, -4 * 2),
    (1, 3, -2 * 2),
    (2, 0, -0 * 2),
    (2, 1, -2 * 2),
    (2, 2, -2 * 2),
    (2, 3, -0 * 2),
])
def test_calculate_interaction_of_one_spin(x, y, expected):
    assert calculate_interaction_of_one_spin(test_field, x, y, kronecker, interaction_coefficient=1.) == expected


@pytest.mark.parametrize('x, y, new_spin, expected', [
    (0, 0, 2, +0.0 * 2),
    (1, 2, 1, +4.0 * 2),
    (2, 0, 2, -1.0 * 2),
    (2, 3, 2, -2.0 * 2)
])
def test_calculate_energy_difference(x, y, new_spin, expected):
    assert calculate_energy_difference(test_field, x, y, new_spin, kronecker, 1.0, 1.0)[0] == expected




