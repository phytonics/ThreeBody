"""
* Assuming equal mass, luminosity and radius
* Assuming the fact that light detected is parallel (due to large distance between us and system)
* Assuming the fact that light intensity is equal at all distance (distance between stars << distance between us and system)

mass = 1, radius = 6 pixels (whatever that means)

Star 1
[
    Position: x = 0.97000436, y = -0.24308753,
    Speed: x: -0.466203685, y: -0.43236573
]

Star 2
[
    Position: x = -0.97000436, y = 0.24308753,
    Speed: x: -0.466203685, y: -0.43236573
]

Star 3
[
    Position: x = 0, y = 0,
    Speed: x = -0.93240737, y = -0.86473146
]

"""

import numpy as np # To simulate the vectors
import turtle, time

def deltaV(stars):

    change = [np.array([0.0, 0.0], dtype = np.float64)] * len(stars)

    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            # Generate all unordered pairs (all interactions)
            r = stars[i]["pos"] - stars[j]["pos"]
            change[j] += -6.67e-11 / (r ** 2.0).sum() * r / (r**2.0).sum() ** 0.5
            change[i] -= -6.67e-11 / (r ** 2.0).sum() * r / (r**2.0).sum() ** 0.5
            print(change)

    return change


star1, star2, star3 = (
    dict(
        pos = np.array([0.97000436, -0.24308753]),
        vel = np.array([0.466203685, 0.43236573])
    ),
    dict(
        pos = np.array([-0.97000436, 0.24308753]),
        vel = np.array([0.466203685, 0.43236573])
    ),
    dict(
        pos = np.array([0.0, 0.0]),
        vel = np.array([-0.93240737, -0.86473146])
    )
)

# Seconds per Frame
PERIOD = 1

# Instant drawing
turtle.speed(0)

while True:
    # Background
    turtle.clearstamps()

    # First star
    turtle.up()
    turtle.goto(tuple(star1["pos"] * 100))
    turtle.stamp()

    # Second star
    turtle.goto(tuple(star2["pos"] * 100))
    turtle.stamp()

    # Third star
    turtle.goto(tuple(star3["pos"] * 100))
    turtle.stamp()

    time.sleep(PERIOD)

    vel_change = deltaV((star1, star2, star3))

    star1["pos"] += star1["vel"] * PERIOD
    star2["pos"] += star2["vel"] * PERIOD
    star3["pos"] += star3["vel"] * PERIOD

    star1["vel"] += vel_change[0] * PERIOD
    star2["vel"] += vel_change[1] * PERIOD
    star3["vel"] += vel_change[2] * PERIOD

    print("FRAME")