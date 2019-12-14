import tkinter
from typing import Callable

from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


def init_gui(root, init_figure: Figure, on_key_press: Callable) -> (tkinter.Label, FigureCanvasTkAgg):
    def event_key_press(event):
        print("you pressed {}".format(event.key))
        on_key_press()
        key_press_handler(event, canvas, toolbar)

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

    return label, canvas


def update_energy_label(label: tkinter.Label, mc_step: int, free_energy: float) -> None:
    label['text'] = f'Free energy: {free_energy}, MC step: {mc_step}'


def draw_figure(canvas: FigureCanvasTkAgg, figure: Figure) -> None:
    canvas.figure = figure
    canvas.draw()

