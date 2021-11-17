from np.magic import np
from numpy.linalg import norm
from typing import Tuple
from turtle import *

import math
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["figure.dpi"] = 150
rcParams["figure.figsize"] = (16.0, 8.0)


def ode45_step(f, x, t, dt, *args):
    """
    One step of 4th Order Runge-Kutta method
    """
    k = dt
    k1 = k * f(t, x, *args)
    k2 = k * f(t + 0.5*k, x + 0.5*k1, *args)
    k3 = k * f(t + 0.5*k, x + 0.5*k2, *args)
    k4 = k * f(t + dt, x + k3, *args)
    return x + 1/6. * (k1 + 2*k2 + 2*k3 + k4)


def ode45(f, t, x0, *args):
    """
    4th Order Runge-Kutta method
    """
    n = len(t)
    x = np.zeros((n, *x0.shape))
    x[0] = x0
    for i in range(n-1):
        dt = t[i+1] - t[i]
        x[i+1] = ode45_step(f, x[i], t[i], dt, *args)
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
    F = (G * m * m[[1, 2, 0]] / norm(r, axis=1)**3).reshape(3, 1) * r
    a = (F[[2, 0, 1]]-F)/m.reshape(3, 1)
    return np.vstack((z[3:], a))


def toSolve(t, z):
    x = ode45(lambda t, z: zdot(1, np[1, 1, 1], z), [0, t], z)
    tarray, zarray = x[0], x[1]
    defect = zarray[-1] - zarray[0]
    return defect



def getSoln(n:int=1) -> Tuple[np.ndarray, float]:
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
            np.m[-0.602885898116520, 1.059162128863347-1::0.252709795391000, 1.058254872224370-1::-0.355389016941814, 1.038323764315145 -1::0.122913546623784, 0.747443868604908::-0.019325586404545, 1.369241993562101::-0.103587960218793, -2.116685862168820],
            284
        )

    elif n == 3:  # Classic Montgomery 8
        return (
            np.m[-0.97000436, 0.24308753::0.97000436, -0.24308753::0, 0::-0.5*0.93240737, -
                 0.5*0.86473146::-0.5*0.93240737, -0.5*0.86473146::0.93240737, 0.86473146],
            632
        )

    elif n == 4:  # Ovals with flourishes
        return (
            np.m[0.716248295712871, 0.384288553041130::0.086172594591232, 1.342795868576616::0.538777980807643, 0.481049882655556::1.245268230895990,
                 2.444311951776573::-0.675224323690062, -0.962879613630031::-0.570043907205925, -1.481432338146543],
            1024
        )

    if n == 5:  # Three Diving Into Middle
        return (
            np.m[1, 0::-0.5, np.sqrt(3)/2::-0.5, -np.sqrt(3)/2::0,
                 1::-np.sqrt(3)/2, -0.5::np.sqrt(3)/2, -0.5] * 0.5,
            1516
        )

    if n == 6:  # Two Ovals (2 on one, 1 on other)
        return (
            np.m[0.486657678894505, 0.755041888583519::-0.681737994414464, 0.293660233197210::-0.022596327468640, -0.612645601255358::-
                 0.182709864466916, 0.363013287999004::-0.579074922540872, -0.748157481446087::0.761784787007641, 0.385144193447218],
            508
        )

    if n == 7:  # Oval,catface,starship
        return (
            np.m[0.536387073390469, 0.054088605007709::-0.252099126491433, 0.694527327749042::-0.275706601688421, -0.335933589317989::-
                 0.569379585580752, 1.255291102530929::0.079644615251500, -0.458625997341406::0.489734970329286, -0.796665105189482],
            636
        )

    if n == 8:  # 3 lined up ovals, with extra phase
        return (
            np.m[0.517216786720872, 0.556100331579180::0.002573889407142, 0.116484954113653::-0.202555349022110, -
                 0.731794952123173::0.107632564012758, 0.681725256843756::-0.534918980283418, -0.854885322576851::0.427286416269208, 0.173160065733631],
            655
        )

    if n == 9:  # Skinny Pineapple
        return (
            np.m[0.419698802831451, 1.190466261251569::0.076399621770974, 0.296331688995343::0.100310663855700, -
                 0.729358656126973::0.102294566002840, 0.687248445942575::0.148950262064203, 0.240179781042517::-0.251244828059670, -0.927428226977280],
            645
        )

    if n == 10:  # Hand-in-Hand Oval
        return (
            np.m[0.906009977920936, 0.347143444586515::-0.263245299491018, 0.140120037699958::-0.252150695248079, -
                 0.661320078798829::0.242474965162160, 1.045019736387070::-0.360704684300259, -0.807167979921595::0.118229719138103, -0.237851756465475],
            869
        )

    if n == 11:  # Loop-ended triangles inside an oval
        return (
            np.m[1.666163752077218-1, -1.081921852656887+1::0.974807336315507-1, -0.545551424117481+1::0.896986706257760-1, -1.765806200083609 +
                 1::0.841202975403070, 0.029746212757039::0.142642469612081, -0.492315648524683::-0.983845445011510, 0.462569435774018],
            482
        )

    if n == 12:  # Lined-up 3 ovals with nested ovals inside
        return (
            np.m[1.451145020734434, -0.209755165361865::-0.729818019566695, 0.408242931368610::0.509179927131025,
                 0.050853900894748::0.424769074671482, -0.201525344687377::0.074058478590899, 0.054603427320703::-0.498827553247650, 0.146921917372517],
            448
        )

    else:  # Oval and crossed triple loop
        return (
            np.m[1.451145020734434, -0.209755165361865::-0.729818019566695, 0.408242931368610::0.509179927131025,
                 0.050853900894748::0.424769074671482, -0.201525344687377::0.074058478590899, 0.054603427320703::-0.498827553247650, 0.146921917372517],

        )


def move(turtle: Turtle, coords: Tuple[float, float]):
    turtle.pu()
    turtle.goto(*coords)
    turtle.pd()


def lightkurve(pos, axis=0):
    """
    Takes an array of vectors mapping the positions of the bodies
    Calculates the light intensity when viewed from the side at a far distance
    Appends it to the array of the curve

    * Assuming the star is a square when viewed from the side
    * This becomes a interval summing problem
    * Checked on https://www.codewars.com/kata/52b7ed099cdc285c300001cd
    """

    # Calculating intervals to consider

    xpos = pos[:, axis]

    s, top = 0, float("-inf")
    for x in sorted(xpos):
        a, b = x - RADIUS, x + RADIUS
        
        if top < a: top = a

        if top < b: s, top = s+b-top, b
    
    return s / (len(pos) * RADIUS * 2)


def lightcurve(pos, axis=0):
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

        if top < a: top = a

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
    
        print(top)
    print("===========================================")
    # Divided to normalise the data
    return s / (len(pos) * C_AREA)


if __name__ == "__main__":
    G = 1
    m = np[1, 1, 1]
    dt = 0.01
    z, tend = getSoln(int(input()))

    # Radius of star
    RADIUS = 0.25

    # Array storing the relative light intensity at every point
    # light intensity of a star is taken to be its radius
    lightkurve_x = []
    lightkurve_y = []
    lightcurve_x = []
    lightcurve_y = []

    # Scaling the RADIUS, such that 1 unit = 300 pixels
    RADIUS *= 300

    # Turtle 1
    obj1 = Turtle()
    obj1.shape("circle")
    obj1.shapesize(RADIUS / 20, RADIUS / 20, RADIUS / 20)
    move(obj1, 300*z[0])
    obj1.speed(0)

    # Turtle 2
    obj2 = Turtle()
    obj2.shape("circle")
    obj2.shapesize(RADIUS / 20, RADIUS / 20, RADIUS / 20)
    obj2.speed(0)
    move(obj2, 300*z[1])

    # Turtle 3
    obj3 = Turtle()
    obj3.shape("circle")
    obj3.shapesize(RADIUS / 20, RADIUS / 20, RADIUS / 20)
    move(obj3, 300*z[2])
    obj3.speed(0)

    for i in range(tend): # 240
        t, z = ode45(lambda t, z: zdot(1, np[1, 1, 1], z), [0, dt], z)
        #z -= dt * zdot(G, m, z)
        p = z[:3]*300

        obj1.goto(*p[0])
        obj2.goto(*p[1])
        obj3.goto(*p[2])

        if p[2][0] == 0 and p[2][1] == 0: print(i)

        lightkurve_x.append(lightkurve(p))
        lightkurve_y.append(lightkurve(p, 1))
        lightcurve_x.append(lightcurve(p))
        lightcurve_y.append(lightcurve(p, 1))

    fig, axes = plt.subplots(1, 2, sharey = True)
    axes[0].plot(lightcurve_x, color="blue", label = "Kurve")
    axes[0].plot(lightkurve_x, color="orange", label = "Curve")
    axes[0].set_title("Light Curve measured about x-axis")
    axes[0].legend(loc="upper right")

    axes[1].plot(lightcurve_y, color="blue", label = "Kurve")
    axes[1].plot(lightkurve_y, color="orange", label = "Curve")
    axes[1].set_title("Light Curve mesasured about y-axis")
    axes[1].legend(loc="upper right")
    plt.show()

