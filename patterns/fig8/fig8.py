import numpy as np # To simulate the vectors
import turtle, time

"""
* Assuming equal mass, luminosity and radius
* Assuming the fact that light detected is parallel (due to large distance between us and system)
* Assuming the fact that light intensity is equal at all distance (distance between stars << distance between us and system)

How to use

1) Input Frames per second for animation
2) Input Calculations per frame for accuracy
3) Input Mass of each body for gravitational effect
4) Input stars position and velocity as tuple of dictionaries like the example given

e.g.
{
    "pos": np.array([0, 0], dtype = np.float64),
    "vel": np.array([0, 0], dtype = np.float64)
}
"""

"""<INPUT REGION>"""
# Frames per second
FPS = 30

# Calculations per frame
CPF = 10000

# Mass of star (Affects gravitational force)
MASS = 1

# Radius of star
RADIUS = 0.25

# Array storing the relative light intensity at every point
# light intensity of a star is taken to be its radius
LIGHTKURVE = np.array([], dtype = np.float64)

stars = (
    dict(
        pos = np.array([0.97000436, -0.24308753], dtype = np.float64),
        vel = np.array([0.466203685, 0.43236573], dtype = np.float64)
    ),
    dict(
        pos = np.array([-0.97000436, 0.24308753], dtype = np.float64),
        vel = np.array([0.466203685, 0.43236573], dtype = np.float64)
    ),
    dict(
        pos = np.array([0.0, 0.0], dtype = np.float64),
        vel = np.array([-0.93240737, -0.86473146], dtype = np.float64)
    )
)
"""</INPUT REGION>"""

"""====Code===="""
def deltaV(stars):

    change = [np.array([0.0, 0.0], dtype = np.float64)] * len(stars)

    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            # Generate all unordered pairs (all interactions)
            r = stars[i]["pos"] - stars[j]["pos"]
            change[j] = change[j] + (MASS / (r ** 2.0).sum()) * (r / ((r**2.0).sum() ** 0.5))
            change[i] = change[i] + (MASS / (r ** 2.0).sum()) * (-r / ((r**2.0).sum() ** 0.5))

    return change

def lightkurve(pos):
    """
    Takes an array of vectors mapping the positions of the bodies
    Calculates the light intensity when viewed from the side at a far distance
    Appends it to the array of the curve

    * Assuming the star is a square when viewed from the side
    * This becomes a interval summing problem
    ! I did not copy others solution I swear
    """

    # Calculating intervals to consider
    
    xpos = pos[:, 0]

    s, top = 0, float("-inf")
    for x in sorted(xpos):
        a, b = x - RADIUS, x + RADIUS
        if top < a: top    = a
        if top < b: s, top = s+b-top, b
    
    np.append(LIGHTKURVE, s)
    return s

# Instant drawing
turtle.speed(0)

while True:
    # Background
    turtle.clearstamps()

    # First star
    turtle.up()

    for s in stars:
        turtle.goto(tuple(s["pos"] * 100))
        turtle.stamp()

    time.sleep(1 / FPS)

    vel_change = deltaV(stars)

    for i in range(CPF): # Calculations per frame
        for s, delv in zip(stars, vel_change):
            s["pos"] = s["pos"] + s["vel"] * (1/CPF/FPS)
            s["vel"] = s["vel"] + delv * (1/CPF/FPS)