import tkinter

from config import q, WIDTH, TEMPERATURE, INTERACTION, J, h, RANDOM_SEED
from field import generate_field, calculate_energy_of_field, plot_field
from gui import init_gui, draw_figure, update_energy_label
from helper import check_config_valid
from metropolis import update_metropolis
from numpy.random import RandomState

states = list(range(q))
check_config_valid()
rg = RandomState(RANDOM_SEED)

field = generate_field(states, WIDTH, rg, correlation=0.3)
figure = plot_field(field, states)
energy = calculate_energy_of_field(field, INTERACTION, interaction_coefficient=J, magnetization_coefficient=h)
free_energy = 0
mc_step = 0


def update_step() -> None:
    global mc_step, field, free_energy, figure
    field, free_energy = update_metropolis(field, states, free_energy, INTERACTION, interaction_coefficient=J,
                                           magnetization_coefficient=h, random_state=rg, temperature=TEMPERATURE)
    mc_step += 1
    figure = plot_field(field, states)
    draw_figure(canvas, figure)
    update_energy_label(label, mc_step, free_energy)


root = tkinter.Tk()
label, canvas = init_gui(root, figure, update_step)

tkinter.mainloop()




