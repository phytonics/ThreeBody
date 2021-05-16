from phyton.constants.unit import kg, m, s
from phyton.constants import MS, RS, G
from phyton.constants.quantity import Quantity

class SolarBody:
    mass = MS
    pos1 = m[0, 0]
    pos2 = m[0, 0]
    pos3 = m[0, 0]
    vel = (m/s)(0, 0)
    diameter = 2*RS

    def grav(self, other) -> Quantity:
        return G*self.mass*other.mass / self.side


class FieldOfView:
    ymin = 0
    ymax = 10

