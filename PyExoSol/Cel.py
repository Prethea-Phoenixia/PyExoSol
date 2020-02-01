import numpy as np


class Celestial:
    def __init__(self):
        self.name = "Undefined"
        self.mass = None  # in units of Mj
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.acc = np.zeros(3)

    def fromOE(self, name, mu, mass, sma, ecc, i, loan, aop, ta):
        """sma:semi major axis, ecc:eccentricity, ta:true anomaly, 
        i:inclination,loan:longtitude of ascending node aop:argument of periapsis"""

        """ angular unit in radian, mass in Mj and length in AU"""

        def cart2spher(tupled_cart):
            import math

            x, y, z = tupled_cart

            r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
            phi = math.atan(y / x)
            theta = math.acos(z / r)
            return [r, theta, phi]

        def spher2cart(tupled_spher):
            import math

            r, theta, phi = tupled_spher
            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)
            return [x, y, z]

        def rotate(vec, unit_axis, ang):  # right hand rule applies.
            import math
            import numpy as np

            vector = np.array(vec)
            axis = np.array(unit_axis)
            v_rot = np.multiply(vector, math.cos(ang))
            v_rot = np.add(v_rot, np.multiply(np.cross(axis, vec), math.sin(ang)))
            v_rot = np.add(
                v_rot,
                np.multiply(
                    1 - math.cos(ang), np.multiply(axis, np.multiply(axis, vec))
                ),
            )
            return v_rot

        import math

        self.mass = mass
        self.name = name
        r_spher = np.array(
            [sma * (1 - ecc ** 2) / (1 + ecc * math.cos(ta)), math.pi / 2, ta]
        )
        r_cart = spher2cart(r_spher)
        r_scalar = np.linalg.norm(r_cart)
        r_spher_unit = np.array([1, math.pi / 2, r_spher[2]])
        fpa = math.acos(
            (1 + ecc * math.cos(ta)) / math.sqrt(1 + ecc ** 2 + 2 * ecc * math.cos(ta))
        )
        """flight path angle as measured against local horizon"""
        horiz_spher_unit = np.array([1, math.pi / 2, r_spher_unit[2] + math.pi / 2])
        vel_spher_unit = np.array([1, math.pi / 2, horiz_spher_unit[2] - fpa])
        vel_scalar = math.sqrt(mu * (2 / r_scalar - 1 / sma))
        v_spher = np.array([vel_scalar, math.pi / 2, vel_spher_unit[2]])
        r_2d = r_cart
        v_2d = spher2cart(v_spher)

        rot_axis = np.array(spher2cart([1, math.pi / 2, -aop]))
        # accounts for angular inclination effects.
        r_3d = rotate(r_2d, rot_axis, i)
        v_3d = rotate(v_2d, rot_axis, i)
        z_unit_cart = np.array([0, 0, 1])
        r_3d = rotate(r_3d, z_unit_cart, loan)
        v_3d = rotate(v_3d, z_unit_cart, loan)
        self.pos = r_3d
        self.vel = v_3d
        return self


def cashKarp(f, x0, y0, h):
    """Butcher Tableau for C-K:
    0   | 
    1/5 | 1/5     
    3/10| 3/40          9/40
    3/5 | 3/10          -9/10       6/5
    1   | -11/54        5/2         -70/27          35/27
    7/8 | 1631/55296    175/512     575/13824       44275/110592       253/4096
    ---------------------------------------------------------------------------------------
        |37/378         0           250/621         125/594             0           512/1771    # fifth order accurate
        |2825/27648     0           18575/48384     13525/55296         277/14336   1/4         # fourth order accurate
    """

    c = np.array([0, 0, 1 / 5, 3 / 10, 3 / 5, 1, 7 / 8])
    a = np.array(
        [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1 / 5, 0, 0, 0, 0],
            [0, 3 / 40, 9 / 40, 0, 0, 0],
            [0, 3 / 10, -9 / 10, 6 / 5, 0, 0],
            [0, -11 / 54, 5 / 2, -70 / 27, 35 / 27, 0],
            [0, 1631 / 55296, 175 / 512, 575 / 13824, 44275 / 110592, 253 / 4096],
        ]
    )
    b = np.array([0, 37 / 378, 0, 250 / 621, 125 / 594, 0, 512 / 1771])
    k = np.zeros((7, 1))
    for s in range(1, 7):

        def kSum(stage):
            ak = 0
            for i in range(1, stage):
                ak += a[stage, i] * k[i]
            return ak

        k[s] = f(x0 + c[s] * h, y0 + h * kSum(s))

    kb = 0
    for i in range(1, 7):
        kb += k[i] * b[i]
    y1 = y0 + h * kb
    return y1



Mestia=Celestial.fromOE(
    name="Mestia", mass=1, mu=1, sma=10, ecc=0.15, i=0.1, loan=0.1, aop=0.1, ta=0.1
)
print(Mestia.vel)