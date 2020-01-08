import numpy as np
from numpy.random import RandomState

from typing_helper import Interaction, States
from output_helper import print_if_verbose


def calculate_interaction_of_one_spin(field: np.ndarray, x: int, y: int, interaction: Interaction,
                                      interaction_coefficient: float) -> float:
    energy = 0
    if x - 1 >= 0:
        energy += interaction(field[x - 1, y], field[x, y])
    if x + 1 < field.shape[0]:
        energy += interaction(field[x, y], field[x + 1, y])
    if y - 1 >= 0:
        energy += interaction(field[x, y - 1], field[x, y])
    if y + 1 < field.shape[1]:
        energy += interaction(field[x, y], field[x, y + 1])
    # About the factor 2: b interacts with c, but c also with b. A change of b thus results in *two* interaction changes
    return - 2 * interaction_coefficient * energy


def calculate_energy_difference(field: np.ndarray, x: int, y: int, new_spin: int, interaction: Interaction,
                                interaction_coefficient: float, magnetization_coefficient: float) -> (float, np.ndarray):
    # positive return value: update would imply energetically less favorable state

    current_energy = calculate_interaction_of_one_spin(field, x, y, interaction, interaction_coefficient)
    field_updated = field.copy()  # Avoid side effects of function by copying
    field_updated[x, y] = new_spin
    updated_energy = calculate_interaction_of_one_spin(field_updated, x, y, interaction, interaction_coefficient)
    magnetization_difference = magnetization_coefficient * (field_updated[x, y] - field[x, y])
    energy_difference = updated_energy - current_energy + magnetization_difference

    if magnetization_coefficient != 0.:
        if magnetization_difference > 0:
            print_if_verbose(f'Magnetization would worsen by {magnetization_difference}.')
        elif magnetization_difference < 0:
            print_if_verbose(f'Magnetization would improve by {magnetization_difference}.')
        else:
            print_if_verbose(f'Magnetization would not change.')
    return energy_difference, field_updated


def update_metropolis(field: np.ndarray, states: States, free_energy: float, interaction: Interaction,
                      interaction_coefficient: float, magnetization_coefficient: float, temperature: float,
                      random_state: RandomState) -> (np.ndarray, float):
    assert states
    assert field.shape[0] == field.shape[1]

    size = field.shape[0]
    random_x, random_y = random_state.randint(size, size=[2])  # dim

    new_spin = field[random_x, random_y]
    # spin flip always needs to lead to a change of spin
    while new_spin == field[random_x, random_y]:
        new_spin = random_state.choice(states)

    energy_delta, field_updated = calculate_energy_difference(field, random_x, random_y, new_spin, interaction,
                                                              interaction_coefficient, magnetization_coefficient)
    random_number = random_state.uniform()
    acceptance_probability = np.exp(-1. / temperature * energy_delta)
    print_if_verbose(f'Energy delta: {energy_delta}, random number: {random_number}, '
          f'acceptance_probability: {acceptance_probability}')
    if energy_delta <= 0 or random_number < acceptance_probability:
        # free_energy_updated = free_energy - energy_delta
        print_if_verbose('Change accepted')
        return field_updated, free_energy - energy_delta
    else:
        print_if_verbose('Not accepted')
        return field, free_energy
