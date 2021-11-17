# sim.py

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk

window = Tk()
window.state("zoomed")
window.minsize(600, 550)
style = ttk.Style(window)
style.theme_use("vista")
window.title("Three Body Simulations")


class ThreeBodySim(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        



