from np.magic import np
import numpy.linalg as la

G = 1000

def getU(m, M, s, totalMass):
    return np.sqrt(
        (G * (m ** 2 + M ** 2 + m * M)) / (s * totalMass)
    )

def angleComp(x_relative):
    x_relative /= la.norm(x_relative)
    cmplx = (0 + 1j) * complex(*x_relative)
    return np[cmplx.real, cmplx.imag]

def calculate(x, x_dot, dt):
    x1, x2, x3 = x
    x_dot1, x_dot2, x_dot3 = x_dot

    x1 = x1 + x_dot1 * dt
    x2 = x2 + x_dot2 * dt
    x3 = x3 + x_dot3 * dt

    return x1, x2, x3

