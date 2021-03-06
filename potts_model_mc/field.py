from itertools import product
from typing import Optional

import numpy as np
import seaborn as sns
from matplotlib.figure import Figure
from numpy.random import RandomState

from config import FIX_LEFT, FIX_TOP, FIX_RIGHT, FIX_BOTTOM
from typing_helper import States, Interaction


def overwrite_edges(field: np.ndarray, size: int):
    field = field.copy()
    if FIX_LEFT is not None:
        field[:, 0] = FIX_LEFT
    if FIX_RIGHT is not None:
        field[:, size-1] = FIX_RIGHT
    if FIX_BOTTOM is not None:
        field[size-1, :] = FIX_BOTTOM
    if FIX_TOP is not None:
        field[0, :] = FIX_TOP
    return field


def generate_field(states: States, size: int, rg: RandomState, correlation: float = 0.0) -> np.ndarray:
    assert states
    assert size > 1
    assert 0.0 < correlation < 1.0

    field = np.array(rg.choice(states, size=[size, size]), dtype=np.int8)
    field = overwrite_edges(field, size)
    if correlation == 0.0:
        return field

    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            if i > 0 and j > 0 and rg.uniform() < correlation:
                if rg.uniform() < 0.5:
                    field[i, j] = field[i - 1, j]
                else:
                    field[i, j] = field[i, j - 1]

    field = overwrite_edges(field, size)
    return field


def plot_field(field: np.ndarray, states: States, title: Optional[str] = None):
    sns.set()
    figure = Figure(figsize=(6, 6))
    ax = figure.subplots()
    sns.heatmap(field, center=np.mean(states), square=True, cbar=False, ax=ax)
    if title:
        ax.set_title(title)
    return figure


def calculate_energy_of_field(field: np.ndarray, interaction: Interaction, interaction_coefficient: float = 1.0,
                              magnetization_coefficient: float = 1.0) -> float:
    size = field.shape[0]
    energy = 0
    for i, j in product(range(size - 1), range(size)):
        energy += interaction(field[i, j], field[i + 1, j])

    for i, j in product(range(size), range(size - 1)):  # dim
        energy += interaction(field[i, j], field[i, j + 1])

    return 2 * interaction_coefficient * energy + magnetization_coefficient * field.sum()
