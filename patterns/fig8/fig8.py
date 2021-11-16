import numpy as np # To simulate the vectors
import turtle, time

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
# Seconds per Frame
PERIOD = 1/100

# Mass of star
MASS = 1

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
    # dict(
    #     pos = np.array([0, 0], dtype = np.float64),
    #     vel = np.array([0, 0], dtype = np.float64)
    # ),
    # dict(
    #     pos = np.array([0, 1], dtype = np.float64),
    #     vel = np.array([0, 0], dtype = np.float64)
    # )
)


def deltaV(stars):

    change = [np.array([0.0, 0.0], dtype = np.float64)] * len(stars)

    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            # Generate all unordered pairs (all interactions)
            r = stars[i]["pos"] - stars[j]["pos"]
            change[j] = change[j] + (MASS / (r ** 2.0).sum()) * (r / ((r**2.0).sum() ** 0.5))
            change[i] = change[i] + (MASS / (r ** 2.0).sum()) * (-r / ((r**2.0).sum() ** 0.5))

    return change


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

    time.sleep(PERIOD)

    vel_change = deltaV(stars)

    for s, delv in zip(stars, vel_change):
        s["pos"] = s["pos"] + s["vel"] * PERIOD
        s["vel"] = s["vel"] + delv * PERIOD