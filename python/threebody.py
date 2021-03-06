from np.magic import np
from math import pi

s = np[0, 0, 0]

G = 6.6743015e-11
density = 1410  # kg/m^3

bodies = 3

u = np.zeros(9)
densities = np.array([density for i in range(bodies)])
m = np.array([])


def rangeKutta(dt, u_new, du_func):
    a = np[dt / 2, dt / 2, dt, 0]
    b = np[dt / 6, dt / 3, dt / 3, dt / 6]
    u0 = u_new[:]
    dim = len(u_new)
    ut = np.zeros(dim)
    for j in range(4):
        du = du_func(u_new)

        u_new = u0 + a[j] * du
        ut += b[j] * du

    return u0 + ut

def calculateRadiusFromMass(mass, den):
    return (0.75 * mass / (pi * den)) ** (1/3)

def calculateDiameters():
    return 2 * calculateRadiusFromMass(m, density)
    
def calculateCOMVelocity():
    v = np[0, 0]
    for i in range(bodies):
        bodyStart = i * 4
        v[0] += m[i] * u[bodyStart + 2]
        v[1] += m[i] * u[bodyStart + 3]

    return v / sum(m)

def calculateCOM():
    x = np[0, 0]
    msum = sum(m)
    for i in range(bodies):
        bodyStart = i * 4
        x[0] += m[i] * u[bodyStart]
        x[1] += m[i] * u[bodyStart + 1]

    return x / msum

def resetStateToInitialConditions():
    for i in range(bodies):
        bodyStart = i * 4
