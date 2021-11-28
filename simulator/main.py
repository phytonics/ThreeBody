# sim.py

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from np.magic import np
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen
from numpy.linalg import norm
from typing import Tuple
from turtle import *
from io import StringIO
from tkinter.filedialog import asksaveasfilename as save
import pyscreenshot as ImageGrab
import math
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import pathlib

rcParams["figure.dpi"] = 150
rcParams["figure.figsize"] = (16.0, 8.0)


def ode45_step(f, x, t, dt, *args):
    """
    One step of 4th Order Runge-Kutta method
    """
    k = dt
    k1 = k * f(t, x, *args)
    k2 = k * f(t + 0.5 * k, x + 0.5 * k1, *args)
    k3 = k * f(t + 0.5 * k, x + 0.5 * k2, *args)
    k4 = k * f(t + dt, x + k3, *args)
    return x + 1 / 6. * (k1 + 2 * k2 + 2 * k3 + k4)


def ode45(f, t, x0, *args):
    """
    4th Order Runge-Kutta method
    """
    n = len(t)
    x = np.zeros((n, *x0.shape))
    x[0] = x0
    for i in range(n - 1):
        dt = t[i + 1] - t[i]
        x[i + 1] = ode45_step(f, x[i], t[i], dt, *args)
    return x


def zdot(G: float, m: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
    G is the Gravitational Constant
    m is an array of shape [1, 3], i.e. a row vector with [m1 m2 m3]
    z is the location and velocity each of the points in the following format:
    [p1_x  p1_y
     p2_x  p2_y
     p3_x  p3_y
     v1_x  v1_y
     v2_x  v2_y
     v3_x  v3_y]
    """
    r = z[:3] - z[[1, 2, 0]]
    F = (G * m * m[[1, 2, 0]] / norm(r, axis=1) ** 3).reshape(3, 1) * r
    a = (F[[2, 0, 1]] - F) / m.reshape(3, 1)
    return np.vstack((z[3:], a))


def toSolve(t, z):
    x = ode45(lambda t, z: zdot(1, np[1, 1, 1], z), [0, t], z)
    tarray, zarray = x[0], x[1]
    defect = zarray[-1] - zarray[0]
    return defect


def getSoln(n: int = 1) -> Tuple[np.ndarray, int]:
    """
    Returns z, tend
    """

    if n == 1:  # Triple Rings Lined Up
        return (
            np.m[-0.0347, 1.1856::0.2693, -1.0020::-0.2328, -
                                                            0.5978::0.2495, -0.1076::0.2059, -0.9396::-0.4553, 1.0471],
            375
        )

    elif n == 2:  # Flower in circle
        return (
            np.m[-0.602885898116520, 1.059162128863347 - 1::0.252709795391000,
            1.058254872224370 - 1::-0.355389016941814, 1.038323764315145 -
                                                       1::0.122913546623784, 0.747443868604908::-0.019325586404545,
            1.369241993562101::-0.103587960218793, -2.116685862168820],
            284
        )

    elif n == 3:  # Classic Montgomery 8
        return (
            np.m[-0.97000436, 0.24308753::0.97000436, -0.24308753::0, 0::-0.5 * 0.93240737, -
                                                                                            0.5 * 0.86473146::-0.5 * 0.93240737,
            -0.5 * 0.86473146::0.93240737, 0.86473146],
            632
        )

    elif n == 4:  # Ovals with flourishes
        return (
            np.m[0.716248295712871, 0.384288553041130::0.086172594591232, 1.342795868576616::0.538777980807643,
            0.481049882655556::1.245268230895990,
            2.444311951776573::-0.675224323690062, -0.962879613630031::-0.570043907205925, -1.481432338146543],
            2048  # 1024
        )

    if n == 5:  # Three Diving Into Middle
        return (
            np.m[1, 0::-0.5, np.sqrt(3) / 2::-0.5, -np.sqrt(3) / 2::0,
            1::-np.sqrt(3) / 2, -0.5::np.sqrt(3) / 2, -0.5] * 0.5,
            1516
        )

    if n == 6:  # Two Ovals (2 on one, 1 on other)
        return (
            np.m[0.486657678894505, 0.755041888583519::-0.681737994414464, 0.293660233197210::-0.022596327468640,
            -0.612645601255358::-
            0.182709864466916, 0.363013287999004::-0.579074922540872, -0.748157481446087::0.761784787007641,
            0.385144193447218],
            508
        )

    if n == 7:  # Oval,catface,starship
        return (
            np.m[0.536387073390469, 0.054088605007709::-0.252099126491433, 0.694527327749042::-0.275706601688421,
            -0.335933589317989::-
            0.569379585580752, 1.255291102530929::0.079644615251500, -0.458625997341406::0.489734970329286,
            -0.796665105189482],
            636
        )

    if n == 8:  # 3 lined up ovals, with extra phase
        return (
            np.m[0.517216786720872, 0.556100331579180::0.002573889407142, 0.116484954113653::-0.202555349022110, -
                                                                                                                 0.731794952123173::0.107632564012758,
            0.681725256843756::-0.534918980283418, -0.854885322576851::0.427286416269208, 0.173160065733631],
            655
        )

    if n == 9:  # Skinny Pineapple
        return (
            np.m[0.419698802831451, 1.190466261251569::0.076399621770974, 0.296331688995343::0.100310663855700, -
                                                                                                                0.729358656126973::0.102294566002840,
            0.687248445942575::0.148950262064203, 0.240179781042517::-0.251244828059670, -0.927428226977280],
            645
        )

    if n == 10:  # Hand-in-Hand Oval
        return (
            np.m[0.906009977920936, 0.347143444586515::-0.263245299491018, 0.140120037699958::-0.252150695248079, -
                                                                                                                  0.661320078798829::0.242474965162160,
            1.045019736387070::-0.360704684300259, -0.807167979921595::0.118229719138103, -0.237851756465475],
            869
        )

    if n == 11:  # Loop-ended triangles inside an oval
        return (
            np.m[1.666163752077218 - 1, -1.081921852656887 + 1::0.974807336315507 - 1,
            -0.545551424117481 + 1::0.896986706257760 - 1, -1.765806200083609 +
                                                           1::0.841202975403070, 0.029746212757039::0.142642469612081,
            -0.492315648524683::-0.983845445011510, 0.462569435774018],
            482
        )

    if n == 12:  # Lined-up 3 ovals with nested ovals inside
        return (
            np.m[1.451145020734434, -0.209755165361865::-0.729818019566695, 0.408242931368610::0.509179927131025,
            0.050853900894748::0.424769074671482, -0.201525344687377::0.074058478590899,
            0.054603427320703::-0.498827553247650, 0.146921917372517],
            448
        )

    if n == 13:  # Oval and crossed triple loop
        return (
            np.m[1.451145020734434, -0.209755165361865::-0.729818019566695, 0.408242931368610::0.509179927131025,
            0.050853900894748::0.424769074671482, -0.201525344687377::0.074058478590899,
            0.054603427320703::-0.498827553247650, 0.146921917372517],
            5
        )

    with open(pathlib.Path(__file__).parent.resolve().parent.resolve() / "data/data.csv") as f:
        data = f.readlines()[14 - 13].split(',')
        return (
            np.loadtxt(
                StringIO(
                    ",".join(data[:-4])
                ),
                delimiter=','
            ).reshape(6, 2),
            math.ceil(124.4 * float(data[-4]))
        )


def move(turtle: RawTurtle, coords: Tuple[float, float]):
    turtle.pu()
    turtle.goto(*coords)
    turtle.pd()


def lightcurve(pos, RADIUS, axis=0):
    """
    Same as lightkurve but c
    c for circle!
    stars are now circles
    """

    # Area of circle is constant as they are all the same circle
    C_AREA = RADIUS * RADIUS * math.pi

    xpos = pos[:, axis]

    s, top = 0, float("-inf")
    for x in sorted(xpos):
        a, b = x - RADIUS, x + RADIUS

        if top < a:
            top = a

        if top < b:
            # Set dist to be the distance between the centre of circle and chord bisecting area intersecting prev circle
            # min ensures distance is at most the radius (floating point error i am looking at u)
            dist = min(RADIUS, x - (top + a) / 2)

            # Add the circle sector added
            # The max is to counter stupid errors due to floating point
            tri = math.sqrt(RADIUS * RADIUS - dist * dist) * dist
            sector = math.acos(dist / RADIUS) * RADIUS * RADIUS

            s += C_AREA - 2 * (sector - tri)

            # Update new top
            top = b

    # Divided to normalise the data
    return s / (len(pos) * C_AREA)


class Plot(ttk.Frame):
    def __init__(self, parent, x=np.array([]), y=np.array([])):
        super().__init__(parent)
        self.fig, self.axes = plt.subplots(
            1, 2, figsize=(16, 8), facecolor="white", sharey=True)

        self.lightcurve_x = x
        self.lightcurve_y = y

        self.line_x = self.axes[0].plot(self.lightcurve_x, color="orange")[0]
        # self.axes[0].plot(self.lightkurve_x, color="blue", label="Curve")
        self.axes[0].set_title("Light Curve measured about x-axis")
        # self.axes[0].legend(loc="upper right")

        self.line_y = self.axes[1].plot(self.lightcurve_y, color="orange")[0]
        # self.axes[1].plot(self.lightkurve_y, color="blue", label="Curve")
        self.axes[1].set_title("Light Curve mesasured about y-axis")
        # self.axes[1].legend(loc="upper right")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.pack(side=BOTTOM, fill=BOTH, expand=1)

    def clear(self):
        self.axes[0].clear()
        self.axes[1].clear()

    def systemClear(self):
        self.clear()
        self.lightcurve_x = np.array([])
        self.lightcurve_y = np.array([])

    def updateXY(self, x, y):
        self.lightcurve_x = np.append(self.lightcurve_x, x)
        self.lightcurve_y = np.append(self.lightcurve_y, y)

        self.clear()

        self.line_x = self.axes[0].plot(self.lightcurve_x, color="orange")[0]
        # self.axes[0].plot(self.lightkurve_x, color="blue", label="Curve")
        self.axes[0].set_title("Light Curve measured about x-axis")
        # self.axes[0].legend(loc="upper right")

        self.line_y = self.axes[1].plot(self.lightcurve_y, color="orange")[0]
        # self.axes[1].plot(self.lightkurve_y, color="blue", label="Curve")
        self.axes[1].set_title("Light Curve mesasured about y-axis")
        # self.axes[1].legend(loc="upper right")

        # self.line_x.set_xdata(np.arange(self.lightcurve_x.shape[0]))
        # self.line_x.set_ydata(self.lightcurve_x)

        # self.line_y.set_xdata(np.arange(self.lightcurve_y.shape[0]))
        # self.line_y.set_ydata(self.lightcurve_y)

        self.canvas.draw()


class ThreeBodySim(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.menu = ttk.Frame(self)

        self.runButton = ttk.Button(self.menu, text="Start Simulation", command=self.runSimulation)
        self.runButton.pack(side=LEFT)

        self.bodyConfig = IntVar(value=3)
        self.chooseConfig = ttk.Spinbox(self.menu, from_=1, to=30, width=5, textvariable=self.bodyConfig)
        self.chooseConfig.pack(side=LEFT)

        self.stopButton = ttk.Button(
            self.menu, text="Stop Simulation", command=self.stopSimulation)
        self.stopButton.pack(side=LEFT)

        self.saveButton = ttk.Button(
            self.menu, text="Save Simulation", command=self.saveSimulation)
        self.saveButton.pack(side=RIGHT)

        self.resetButton = ttk.Button(
            self.menu, text="Reset Simulation", command=self.resetSimulation)
        self.resetButton.pack(side=RIGHT)

        self.menu.pack(side=TOP)

        self.canvas = ScrolledCanvas(self)
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        # self.canvas.config(width=1000, height=1000)

        self.screen = TurtleScreen(self.canvas)

        self.radius = 0.05 * 300

        self.plot = Plot(self)

        self.screen.listen()

        self.pack(fill=BOTH, expand=1)

        self.isRunning = BooleanVar(value=False)

    def saveSimulation(self):
        lightcurve_x = self.plot.lightcurve_x.copy()
        lightcurve_y = self.plot.lightcurve_y.copy()
        df = pd.DataFrame({"lightcurve_x": lightcurve_x, "lightcurve_y": lightcurve_y})

        x2 = self.parent.winfo_rootx()
        y2 = self.parent.winfo_rooty()
        x1 = x2 + self.parent.winfo_width()
        y1 = y2 + self.parent.winfo_height()

        imageFile = save(title="Save ThreeBody Configuration Image at:",
                         filetypes=(
                             ("PNG Image Files", "*.png"),
                             ("JPEG Image Files", "*.jpg"),
                             ("GIF Image Files", "*.gif"),
                             ("Icon Image Files", "*.ico")
                         ))
        if imageFile:
            ImageGrab.grab().crop((x2, y2, x1, y1)).save(imageFile)

        csvFile = save(title="Save ThreeBody LightCurve at:",
                       filetypes=(
                           ("CSV Files", "*.csv"),
                           ("TXT Files", "*.txt"),
                           ("TSV Files", "*.tsv"),
                           ("Excel Files", "*.xlsx *.xls"),
                           ("JSON Files", "*.json"),
                           ("HTML Files", "*.html *.xhtml *.htm *.php"),
                           ("All Files", "*")
                       ))
        if csvFile:
            extension = csvFile.split(".")[-1].lower()
            if extension == "tsv":
                df.to_csv(csvFile, sep="\t", index=False)
            elif "xls" in extension:
                df.to_excel(csvFile, index=False)
            elif "json" in extension:
                df.to_json(csvFile, index=False)
            elif "htm" in extension:
                df.to_html(csvFile, index=False)
            else:
                df.to_csv(csvFile, index=False)

    def resetSimulation(self):
        self.stopSimulation()
        self.plot.systemClear()
        self.screen.clearscreen()

    def runSimulation(self):
        self.resetSimulation()

        self.isRunning.set(True)
        G = 1
        m = np[1, 1, 1]
        dt = 0.01
        z, tend = getSoln(self.bodyConfig.get())

        # Turtle 1
        self.obj1 = RawTurtle(self.canvas, shape="circle")
        self.obj1.shapesize(
            self.radius / 20, self.radius / 20, self.radius / 20)
        self.obj1.color("red")
        self.obj1.speed(0)

        # Turtle 2
        self.obj2 = RawTurtle(self.canvas, shape="circle")
        self.obj2.shapesize(
            self.radius / 20, self.radius / 20, self.radius / 20)
        self.obj2.speed(0)
        self.obj2.color("blue")

        # Turtle 3
        self.obj3 = RawTurtle(self.canvas, shape="circle")
        self.obj3.shapesize(
            self.radius / 20, self.radius / 20, self.radius / 20)
        self.obj3.color("green")
        self.obj3.speed(0)

        move(self.obj1, 300 * z[0])
        move(self.obj2, 300 * z[1])
        move(self.obj3, 300 * z[2])

        # for i in range(tend):  # 240
        while self.isRunning.get():
            t, z = ode45(lambda t, z: zdot(1, np[1, 1, 1], z), [0, dt], z)
            # z -= dt * zdot(G, m, z)
            p = z[:3] * 300

            sim.obj1.goto(*p[0])
            sim.obj2.goto(*p[1])
            sim.obj3.goto(*p[2])

            sim.plot.updateXY(lightcurve(p, self.radius), lightcurve(p, self.radius, 1))

        self.isRunning.set(False)
        # self.screen.clearscreen()
        # self.plot.systemClear()

    def stopSimulation(self):
        self.isRunning.set(False)


if __name__ == "__main__":
    window = Tk()
    window.state("zoomed")
    window.iconbitmap(pathlib.Path(__file__).parent.resolve() / 'phyton.ico')
    style = ttk.Style(window)
    style.theme_use("vista")
    window.title("Three Body Simulator")

    sim = ThreeBodySim(window)
    window.mainloop()




