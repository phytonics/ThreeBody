# phyton.constants.unit

import re
from inspect import getmro as inspect
from math import pi
import np
from phyton.constants import quantity
from collections.abc import Iterable

def _isnumeric(val):
    if type(val) in [np.generic, int, float, complex]: return True
    try: return bool(set(inspect(val)) & set([np.generic, int, float, complex]))
    except: return False


class Prefix:
    def __init__(self, prefix='', name='', power=1):
        self.prefix, self.name, self.power = prefix, name, power

prefixes = [Prefix(),
    Prefix('y', 'yocto', 1e-24),
    Prefix('z', 'zepto', 1e-21),
    Prefix('a', 'atto', 1e-18),
    Prefix('f', 'femto', 1e-15),
    Prefix('p', 'pico', 1e-12),
    Prefix('n', 'nano', 1e-9),
    Prefix('μ', 'micro', 1e-6),
    Prefix('m', 'milli', 1e-3),
    Prefix('c', 'centi', 1e-2),
    Prefix('d', 'deci', 1e-1),
    Prefix('da', 'deka', 1e1),
    Prefix('h', 'hecto', 1e2),
    Prefix('k', 'kilo', 1e3),
    Prefix('M', 'Mega', 1e6),
    Prefix('G', 'Giga', 1e9),
    Prefix('T', 'Tera', 1e12),
    Prefix('P', 'Peta', 1e15),
    Prefix('E', 'Exa', 1e18),
    Prefix('Z', 'Zeta', 1e21),
    Prefix('Y', 'Yota', 1e24)
]

class Unit:
    SIs = ['g', 'mol', "rad", 'm', 'A', 's', 'K', 'cd']
    def __init__(self, unit='', unitname='', unitfunc='', mul=1, add=0, scalar=False):
        self.unit, self.powers = self.fix(unit)
        self.unitname = unitname
        self.unitfunc = unitfunc
        self.mul = mul
        self.add = add
        self.scalar = scalar
        if '/' in self.unit: self.numer, self.denom = self.unit.split('/')
        else: self.numer, self.denom = self.unit, ''


    def fix(self, unit):
        numer = ''
        denom = ''

        if type(unit) == dict:
            powers = unit
        else:
            if '/' in unit: [ognum, ogden] = unit.split('/')
            else: ognum, ogden = unit, ''

            powers = dict()
            # numerator
            for u in self.SIs:
                cnt = 0
                while re.search(u+"\^[0-9.]+", ognum):
                    match = re.search(u+"\^[0-9.]+", ognum)
                    cnt += eval(match.group()[len(u)+1:])
                    ognum = ognum[:match.start()] + ognum[match.end():]

                while u in ognum:
                    cnt += 1
                    #print(ognum)
                    ognum = ognum.replace(u, '', 1)
                powers[u] = cnt

            # denominator
            for u in self.SIs:
                cnt = 0
                while re.search(u+"\^[0-9.]+", ogden):
                    match = re.search(u+"\^[0-9.]+", ogden)
                    cnt -= eval(match.group()[len(u)+1:])
                    ogden = ogden[:match.start()] + ogden[match.end():]

                while u in ogden:
                    cnt -= 1
                    ogden = ogden.replace(u, '', 1)
                powers[u] += cnt
        for u, p in powers.items():
            if p == 0: continue
            elif p == 1: numer += u
            elif p == -1: denom += u
            elif p > 0: numer += u+f"^{p}"
            else: denom += u+f"^{abs(p)}"
        if numer and denom: return numer+'/'+denom, powers
        if numer: return numer, powers
        if denom: return '1/'+denom, powers
        return '', powers

    def __repr__(self):
        s = ''
        if not(self.unitname or self.unitfunc): return str(self)
        if self.unitname: s += self.unitname
        if self.unitfunc: s += ': measure of '+self.unitfunc
        return s

    def __str__(self):
        unit = self.unit.replace('g', 'kg')
        if unit == "kgm/s^2": return "N"
        if unit == "kgm^2/s^3": return "W"
        if unit == "1/s": return "Hz"
        if unit == "kg/ms^2": return "Pa"
        if unit == "As": return "C"
        if unit == "kgm^2/As^3": return "V"
        if unit == "kgm^2/s^3A^2": return "Ω"
        if unit == "mol/s": return "kat"
        if unit == "A^2s^3/kgm^2": return "S"
        if unit == "A^2s^4/kgm^2": return "F"
        if unit == "kgm^2/As^2": return "Wb"
        if unit == "kg/As^2": return "T"
        if unit == "kgm^2/A^2s^2": return "H"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        if unit == "kgm/s^2": return "N"
        return unit

    def __mul__(self, other):
        if _isnumeric(other):
            return Unit(self.unit, mul = self.mul*float(other), add = self.add*float(other))
        if type(other) == Unit:
            return Unit(self.numer+other.numer+'/'+self.denom+other.denom, mul = self.mul*other.mul, add = self.add+other.add)

    def __rmul__(self, other):
        if _isnumeric(other):
            return Unit(self.unit, mul = self.mul*float(other), add = self.add*float(other))
        if type(other) == Unit:
            return Unit(self.numer+other.numer+'/'+self.denom+other.denom, mul = self.mul*other.mul, add = self.add+other.add)

    def __add__(self, other):
        if _isnumeric(other):
            return Unit(self.unit, self.unitname, self.unitfunc, self.mul, self.add+float(other))
        if other == self: return self
        if type(other) == Unit:
            if self.unit == other.unit: return Unit(self.unit, self.unitname, self.unitname, self.mul+other.mul, self.add)
            else: return Unit('')

    def __radd__(self, other):
        if _isnumeric(other):
            return Unit(self.unit, self.unitname, self.unitfunc, self.mul, self.add+float(other))
        if other == self: return self
        if type(other) == Unit:
            if self.unit == other.unit: return(self.unit, self.unitname, self.unitname, self.mul+other.mul, self.add+other)
            else: return Unit('')

    def __sub__(self, other):
        if _isnumeric(other):
            return Unit(self.unit, self.unitname, self.unitfunc, self.mul, self.add-float(other))
        if type(other) == Unit:
            if self.unit == other.unit: return(self.unit, self.unitname, self.unitname, self.mul-other.mul, self.add-other.add)
            else: return Unit('')

    def __rsub__(self, other):
        if _isnumeric(other):
            return Unit(self.unit, self.unitname, self.unitfunc, self.mul, float(other)-self.add)
        if type(other) == Unit:
            if self.unit == other.unit: return(self.unit, self.unitname, self.unitname, other.mul-self.mul, other.add-self.add)
            else: return Unit('')

    def __truediv__(self, other):
        if type(other) == Unit:
            return Unit(self.numer+other.denom+'/'+self.denom+other.numer, mul = self.mul/other.mul)
        if _isnumeric(other):
            return Unit(self.unit, mul = self.mul/float(other), add = self.add/float(other))

    def __rtruediv__(self, other):
        if type(other) == Unit:
            return Unit(self.denom+other.numer+'/'+self.numer+other.denom, mul = other.mul/self.mul)
        if _isnumeric(other):
            return Unit((self.denom if self.denom else '1')+'/'+self.numer, mul = float(other)/self.mul)

    def __pow__(self, other):
        powers = self.powers.copy()
        for i in powers:
            powers[i] = powers[i] * other
        return Unit(powers, mul = self.mul**other)

    def __eq__(self, other):
        return self.unit == other.unit

    def __call__(self, *args, uncertainty=0):
        name = ""
        if type(args[-1]) == str:
            name = args[-1]
            args = args[:-1]

        if len(args) == 1 or self.scalar:
            args = args[0]
        return quantity.Quantity(args, self, name, uncertainty=0)

    def __getitem__(self, key):
        if isinstance(key, Iterable):
            key = list(key)
            if self.scalar or len(key) == 1: key = key[0]
        return quantity.Quantity(key, self)

    def __xor__(self, other):
        return self ** other



templates = [
    "%sm = Unit('m', '%smetre', 'length', %s)",
    "%ss = Unit('s', '%ssecond', 'time', %s, scalar=True)",
    "%sg = Unit('g', '%sgram', 'mass', %s, scalar=True)",
    "%sA = Unit('A', '%sampere', 'electric current', %s, scalar=True)",
    "%sK = Unit('K', '%skelvin', 'thermodynamic temperature', %s, scalar=True)",
    "%smol = Unit('mol', '%smole', 'amount of substance', %s, scalar=True)",
    "%scd = Unit('cd', '%scandela', 'luminous intensity', %s, scalar=True)",
    "%sHz = Unit('1/s', '%shertz', 'frequency', %s, scalar=True)",
    "%sN = Unit('gm/s^2', '%snewton', 'force', %s)",
    "%sPa = Unit('g/ms^2', '%spascal', 'pressure, stress', %s, scalar=True)",
    "%sJ = Unit('gm^2/s^2', '%sjoule', 'energy, work, amount of heat', %s, scalar=True)",
    "%sW = Unit('gm^2/s^3', '%swatt', 'power, radiant flux', %s, scalar=True)",
    "%sC = Unit('As', '%scoulomb', 'electric charge, quantity of electricity', %s, scalar=True)",
    "%sV = Unit('gm^2/As^3', '%svolt', 'electric potential, emf', %s, scalar=True)",
    "%sΩ = Unit('gm^2/s^3A^2', '%sohm', 'electric resistance, impedance', %s, scalar=True)",
    "%sohm = Unit('gm^2/s^3A^2', '%sohm', 'electric resistance, impedance', %s, scalar=True)",
    "%skat = Unit('mol/s', '%skatal', 'catalytic activity', %s, scalar=True)",
    "%sS = Unit('A^2s^3/gm^2', '%ssiemen', 'electric conductance', %s, scalar=True)",
    "%sF = Unit('A^2s^4/gm^2', '%sfarad', 'capacitance', %s, scalar=True)",
    "%sWb = Unit('gm^2/As^2', '%sweber', 'magnetic flux', %s, scalar=True)",
    "%sT = Unit('g/As^2', '%stesla', 'magnetic field', %s)",
    "%sH = Unit('gm^2/A^2s^2', '%shenry', 'inductance', %s, scalar=True)",
    "%sdegreeCelsius = Unit('K', '%s°Celsius', 'temperature on the celsius scale', %s, -273.15, scalar=True)",
    "%sdegCelsius = Unit('K', '%s°Celsius', 'temperature on the celsius scale', %s, -273.15, scalar=True)",
    "%sdegC = Unit('K', '%s°Celsius', 'temperature on the celsius scale', %s, -273.15, scalar=True)",
    "%sGy = Unit('m^2/s^2', '%sgray', 'absorbed dose, specific energy', %s, scalar=True)",
    "%sSv = Unit('m^2/s^2', '%ssievert', 'dose equivalent(d)', %s, scalar=True)",
    "%sBq = Unit('1/s', '%sbecquerel', 'activity (of a radionuclide)', %s, scalar=True)",
    "%srad = Unit('rad', '%sradian', 'plane angle', %s, scalar=True)",
    "%ssr = Unit('m^2/m^2', '%ssteradian', 'solid angle', %s, scalar=True)",
    "%slm = Unit('cd', '%slumen', 'luminous flux', %s, scalar=True)",
    "%slx = Unit('cd/m^2', '%slux', 'illuminance', %s, scalar=True)",
    "%sdeg = Unit('rad', '%s°', 'plane angle in degree scale', %s*(pi/180), scalar=True)",
    "%seV = Unit('gm^2/s^2', '%selectron Volts', 'measure of energy', %s*1.60217648740e-19, scalar=True)",
#    "%smins = Unit('s', '%sminutes', 'measure of time', %s*60, scalar=True)",
#    "%shr = Unit('s', '%shours', 'measure of time', %s*3600, scalar=True)",
#    "%sday = Unit('s', '%sdays', 'measure of time', %s*3600*24, scalar=True)",
#    "%syr = Unit('s', '%syears', 'measure of time', %s*3600*24*365.25, scalar=True)",
    "%sly = Unit('m', '%slightyear', 'measure of distance', %s*3600*24*365.25*299792458)",
    "%spc = Unit('m', '%sparsec', 'measure of distance', %s*3.086e16, scalar=True)",
    "%sL = Unit('m^3', '%slitre', 'measure of volume', %s/1000, scalar=True)"
]
for p in prefixes:
    for temp in templates:
        try:
            exec(temp % (p.prefix, p.name, p.power))
            if temp[:3] == '%sg':
                exec(f"{p.prefix}g.mul /= 1000")
        except:
            try:exec(temp % (p.name, p.name, p.power))
            except: pass

#deg = Unit('m/m', '°', 'plane angle in degree scale', (pi/180))
kWh = Unit('gm^2/s^2', 'kilowatt hour', 'measure of energy', 3.6e6, scalar=True)
min = Unit('s', 'minutes', 'measure of time', 60, scalar=True)
hr = Unit('s', 'hours', 'measure of time', 3600, scalar=True)
day = Unit('s', 'days', 'measure of time', 3600*24, scalar=True)
yr = Unit('s', 'years', 'measure of time', 3600*24*365.25, scalar=True)
