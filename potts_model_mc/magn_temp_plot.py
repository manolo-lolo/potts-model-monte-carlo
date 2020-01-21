import pickle

import numpy as np
from numpy.random import RandomState
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from field import generate_field, calculate_energy_of_field
from interaction import kronecker
from metropolis import update_metropolis

q = 4
WIDTH = 20
INTERACTION = kronecker
J = 1.
RANDOM_SEED = 424242

states = list(range(q))
rg = RandomState(RANDOM_SEED)
h = 1.0
NO_REPEATS = 300
THERMALIZATION = 100000
SAVE_AND_GENERATE_GRAPH_EVERY = 5
temperatures = np.linspace(1.0, 14.0, 80)


magnetization = np.zeros((NO_REPEATS, temperatures.shape[0]), dtype=float)
for i in tqdm(range(NO_REPEATS)):
    for j, temperature in enumerate(temperatures):
        field = generate_field(states, WIDTH, rg, correlation=0.3)
        free_energy = 0
        energy = calculate_energy_of_field(field, INTERACTION, interaction_coefficient=J, magnetization_coefficient=h)

        for _ in range(THERMALIZATION):
            field, free_energy = update_metropolis(field, states, free_energy, INTERACTION, interaction_coefficient=J,
                                                   magnetization_coefficient=h, random_state=rg, temperature=temperature)
        magnetization[i, j] = -h * field.sum()

    if (i - 2) % SAVE_AND_GENERATE_GRAPH_EVERY == 0:
        with open('state.pck', 'wb') as file:
            pickle.dump({'data': magnetization, 'i': i, 'randomstate': rg}, file)

        plt.clf()
        sns_plot = sns.lineplot(x=list(temperatures)*(i+1), y=magnetization[:i+1].flatten()).get_figure()
        sns_plot.savefig(f'temperature_magnetization_it_{i}.png')
