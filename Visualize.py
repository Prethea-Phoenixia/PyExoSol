"""import time"""
from math import *

import numpy as np

G = 2.8240 * 10 ** -7  # au^3/Mj*day^2
resolution = [1200, 600]


class Celestial(object):
    def __init__(self):
        self.name = "Undefined"
        self.mass = None  # in units of Mj
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.acc = np.zeros(3)
        self.color = [255, 255, 255]
        self.satellite = []

    def update(self, targets, dt):
        """ update the object for one click with respect to current system.
        system: list, dt: float"""

        def grav(self, targets):
            """return acceleartion caused by gravity"""
            sa = np.zeros(3)
            for target in targets:
                d = target.pos - self.pos
                r = np.linalg.norm(d)
                if r.all() != 0:
                    di = d / r  # unit vector pointing from b->a
                    da = target.mass * G / r ** 2
                    vda = da * di
                else:
                    vda = 0
                sa += vda
            return sa

        # Velocity Verlet method, O(dt^2) error
        if np.all(self.acc) == 0:
            grav(self, targets)
        self.pos = self.pos + self.vel * dt + self.acc / 2 * dt ** 2
        currAcc = self.acc
        self.acc = grav(self, targets)
        self.vel = self.vel + (currAcc + self.acc) / 2 * dt

    def cordFromEphem(self, name, mm, mass, sma, ecc, i, loan, aop, ta):
        """ mm: mass of attractor, in Mj
            sma:semi major axis, ecc:eccentricity, ta:true anomaly,
            i:inclination,loan:longtitude of ascending node aop:argument of periapsis
            angular unit in radian, mass in Mj and length in AU"""

        mu = mm * G

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

        import numpy as np
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


def datastream(constellation, dt, tps, fps):
    """dt:delta time,used for physical calculation
        tps:actual physical update per second
        fps:updates graphics per second
        update per frame = tps / fps and should be positive integer.
        """
    import turtle
    keep = True
    try:

        def swapbanks():
            nonlocal ephem
            currpos = constellation.index(ephem)
            maxpos = len(constellation)
            if currpos + 1 == maxpos:
                ephem = constellation[0]
            else:
                ephem = constellation[currpos + 1]

        def exit():
            nonlocal keep
            keep = False

        def mkbutton(x0, y0, l, h, text, func_if_clicked):
            import tkinter as tk
            from tkinter import font

            cal10 = font.Font(family="Calibri", size=12)
            canvas = turtle.getcanvas()
            parent = canvas.master
            button = tk.Button(
                parent, text=text, command=func_if_clicked, width=10, font=cal10,
            ).pack(side=tk.LEFT)
            id = canvas.create_window((x0, y0), window=button)

        upf = int(tps / fps)

        def streamdata():
            screen.onclick(None)
            for i in range(0, upf):
                for system in constellation:
                    for star in system:
                        star.update(system, dt)
            worker.clear()
            worker.setpos(0, resolution[1] / 2)

            for star in ephem:
                worker.setheading(270)
                worker.forward(20)
                canonSetting = ("Calibri", 14, "normal")
                x, y, z = star.pos
                worker.setheading(0)
                worker.color(star.color)
                worker.write(str(star.name), align="left", font=canonSetting)
                worker.color("white")
                worker.fd(100)
                worker.write("x:" + str(round(x, 3)), align="left", font=canonSetting)
                worker.fd(150)
                worker.write("y:" + str(round(y, 3)), align="left", font=canonSetting)
                worker.fd(150)
                worker.write("z:" + str(round(z, 3)), align="left", font=canonSetting)
                worker.bk(400)
            gridWorker.clear()
            gridWorker.color("white")
            for i in range(0, 3):
                gridWorker.goto(-resolution[0] / 4, 0)
                gridWorker.setheading(90 + 135 * i)
                gridWorker.pd()
                if i != 1:
                    gridWorker.fd(resolution[0] / 4)
                else:
                    gridWorker.fd(resolution[0] / 4 / sqrt(2))
                gridWorker.pu()
            for star in ephem:
                gridWorker.color([5, 102, 8])
                x, y, z = star.pos
                projX = (-x / sqrt(2) + y) * 100
                projY = (-x / sqrt(2) + z) * 100
                gridWorker.goto(projX - resolution[0] / 4, projY)
                gridWorker.dot(5, star.color)
                gridWorker.pd()
                gridWorker.setheading(270)
                gridWorker.fd(z * 100)
                gridWorker.goto(-resolution[0] / 4, 0)
                gridWorker.pu()
            screen.update()
            if keep:
                screen.ontimer(streamdata, int(1000 / fps))
            else:
                screen.bye()

        ephem = constellation[0]
        screen = turtle.Screen()
        worker = turtle.RawTurtle(screen)
        gridWorker = turtle.RawTurtle(screen)
        worker.hideturtle()
        gridWorker.hideturtle()
        worker.penup()
        worker.speed(0)
        screen.bgcolor("black")
        screen.colormode(255)
        screen.tracer(False)
        screen.setup(width=resolution[0], height=resolution[1])
        screen.ontimer(streamdata, int(1000 / fps))
        mkbutton(10, 0, 5, 1, "END", exit)
        mkbutton(120, 0, 5, 1, "SWPB", swapbanks)
        screen.mainloop()

    except turtle.Terminator:
        pass


def test():

    Sol = Celestial()
    Sol.mass = 1047.4
    Sol.pos = np.array([0.00450, 0.00077, 0.00027])
    Sol.vel = np.array([-0.00000, 0.00000, 0.00000])
    Sol.name = "Sol"
    Sol.color = "Yellow"

    Mercury = Celestial()
    Mercury.mass = 1.7387e-4
    Mercury.pos = np.array([0.36176, -0.09078, -0.08571])
    Mercury.vel = np.array([0.00337, 0.02489, 0.01295])
    Mercury.name = "Mercury"
    Mercury.color = [192, 192, 192]

    Venus = Celestial()
    Venus.mass = 2.5637e-3
    Venus.pos = np.array([0.61275, -0.34837, -0.19528])
    Venus.vel = np.array([0.01095, 0.01562, 0.00633])
    Venus.name = "Venus"
    Venus.color = [240, 230, 140]

    Earth = Celestial()
    Earth.mass = 3.1457e-3
    Earth.pos = np.array([0.12052, -0.92584, -0.40154])
    Earth.vel = np.array([0.01681, 0.00175, 0.00076])
    Earth.name = "Earth"
    Earth.color = [0, 151, 241]

    Lunar = Celestial()
    Lunar.mass = 3.8692e-5
    Lunar.pos = np.add(Earth.pos, np.array([-0.00081, -0.00199, -0.00109]))
    Lunar.vel = np.add(Earth.vel, np.array([0.00060, -0.00017, -0.00009]))
    Lunar.name = "Lunar"
    Lunar.color = [255, 250, 250]

    Mars = Celestial()
    Mars.mass = 3.3799e-4
    Mars.pos = np.array([-0.11019, -1.3276, -0.60589])
    Mars.vel = np.array([0.01448, 0.00024, -0.00028])
    Mars.name = "Mars"
    Mars.color = [193, 68, 14]

    Jupiter = Celestial()
    Jupiter.mass = 1
    Jupiter.pos = np.array([-5.3797, -0.83048, -0.22483])
    Jupiter.vel = np.array([0.00109, -0.00652, -0.00282])
    Jupiter.name = "Jupiter"
    Jupiter.color = [227, 110, 75]

    Saturn = Celestial()
    Saturn.mass = 0.29942
    Saturn.pos = np.array([7.8944, 4.5965, 1.5587])
    Saturn.vel = np.array([-0.00322, 0.00434, 0.00193])
    Saturn.color = [234, 214, 184]
    Saturn.name = "Saturn"

    Uranus = Celestial()
    Uranus.mass = 0.045730
    Uranus.pos = np.array([-18.265, -1.1620, -0.25011])
    Uranus.vel = np.array([0.00022, -0.00376, -0.00165])
    Uranus.color = [213, 251, 252]
    Uranus.name = "Uranus"

    Neptune = Celestial()
    Neptune.mass = 0.053953
    Neptune.pos = np.array([-16.055, -23.942, -9.4001])
    Neptune.vel = np.array([0.00264, -0.00150, -0.00068])
    Neptune.name = "Neptune"
    Neptune.color = [68, 102, 127]

    Pluto = Celestial()
    Pluto.mass = 7.7104e-4
    Pluto.pos = np.array([-30.483, -0.87241, 8.9116])
    Pluto.vel = np.array([0.00032, -0.00314, -0.00108])
    Pluto.color = [150, 133, 112]
    Pluto.name = "Pluto"

    system = [
        Sol,
        Mercury,
        Venus,
        Earth,
        Lunar,
        Mars,
        Jupiter,
        Saturn,
        Neptune,
        Uranus,
        Pluto,
    ]
    datastream([system], 0.1, 100, 10)


if __name__ == "__main__":
    test()
