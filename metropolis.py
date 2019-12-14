import numpy as np
from numpy.random import RandomState

from typing_helper import Interaction, States


def calculate_interaction_of_one_spin(field: np.ndarray, x: int, y: int, interaction: Interaction,
                                      magnetization_coefficient: float) -> float:
    # TODO factor 2 ?!
    energy = 0
    if x > 0:  # dim!!
        energy += interaction(field[x - 1, y], field[x, y])
    if x + 1 < field.shape[0]:
        energy += interaction(field[x, y], field[x + 1, y])
    if y > 0:
        energy += interaction(field[x, y - 1], field[x, y])
    if y + 1 < field.shape[1]:
        energy += interaction(field[x, y], field[x, y + 1])
    return 2 * magnetization_coefficient * energy


def calculate_energy_difference(field: np.ndarray, x: int, y: int, new_spin: int, interaction: Interaction,
                                magnetization_coefficient: float) -> (float, np.ndarray):
    # positive return value: update would imply energetically less favorable state

    current_energy = calculate_interaction_of_one_spin(field, x, y, interaction, magnetization_coefficient)
    field_updated = field.copy()  # Avoid side effects of function by copying
    field_updated[x, y] = new_spin
    updated_energy = calculate_interaction_of_one_spin(field_updated, x, y, interaction, magnetization_coefficient)
    energy_difference = updated_energy - current_energy \
                        + magnetization_coefficient * (field_updated[x, y] - field[x, y])
    return updated_energy - current_energy, field_updated


def update_metropolis(field: np.ndarray, states: States, free_energy: float, interaction: Interaction,
                      magnetization_coefficient, random_state: RandomState) -> (np.ndarray, float):
    assert states
    assert field.shape[0] == field.shape[1]

    size = field.shape[0]
    random_x, random_y = random_state.randint(size, size=[2])  # dim
    random_spin = random_state.choice(states)
    energy_difference, field_updated = calculate_energy_difference(field, random_x, random_y, random_spin, interaction,
                                                                   magnetization_coefficient)
    if energy_difference < 0 or random_state.uniform():
        # free_energy_updated = free_energy - energy_difference
        return field_updated, free_energy
    else:
        return field, free_energy
