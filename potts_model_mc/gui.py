import tkinter
from typing import Callable

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


def init_gui(root, init_figure: Figure, step_function: Callable) -> (tkinter.Label, FigureCanvasTkAgg):
    def event_key_press(event):
        step_function()
        key_press_handler(event, canvas, toolbar)

    def do_several_steps(n: int):
        for _ in range(n):
            step_function()

    def quit_():
        root.quit()
        root.destroy()

    root.wm_title('MC simulation of Potts model')
    label = tkinter.Label(root, text='')
    label.pack()

    canvas = FigureCanvasTkAgg(init_figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    canvas.mpl_connect("key_press_event", event_key_press)

    button = tkinter.Button(master=root, text="Quit", command=quit_)
    button.pack(side=tkinter.BOTTOM)

    button_group = tkinter.Frame(master=root)
    button_group.pack(side=tkinter.BOTTOM)
    button_1_step = tkinter.Button(master=button_group, text='1 MC step', command=lambda: do_several_steps(1))
    button_1_step.pack(side=tkinter.LEFT)
    button_10_step = tkinter.Button(master=button_group, text='10 MC steps', command=lambda: do_several_steps(10))
    button_10_step.pack(side=tkinter.LEFT)
    button_100_step = tkinter.Button(master=button_group, text='100 MC steps', command=lambda: do_several_steps(100))
    button_100_step.pack(side=tkinter.LEFT)
    button_1000_step = tkinter.Button(master=button_group, text='1.000 MC steps', command=lambda: do_several_steps(1000))
    button_1000_step.pack(side=tkinter.LEFT)
    button_10000_step = tkinter.Button(master=button_group, text='10.000 MC steps', command=lambda: do_several_steps(10000))
    button_10000_step.pack(side=tkinter.LEFT)

    label_help = tkinter.Label(master=root, text='Pressing any keyboard button will do 1 MC step')
    label_help.pack(side=tkinter.BOTTOM)

    return label, canvas


def update_energy_label(label: tkinter.Label, mc_step: int, free_energy: float) -> None:
    label['text'] = f'Free energy: {round(free_energy, 1)}, MC step: {mc_step}'


def draw_figure(canvas: FigureCanvasTkAgg, figure: Figure) -> None:
    canvas.figure = figure
    canvas.draw()

