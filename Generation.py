"""Based on 'World Generation' by Tyge Sjostrand, 2008"""
"""Exec_FusionSphere"""
"""Rebooted 11/26/2019"""


def seed_random(seed):
    import random

    random.seed(seed)


def dice_1d(x):
    import random as rd

    return rd.randrange(1, x + 1)


def rnd(a, b):
    import random as rd

    return rd.randrange(a, b + 1)


class Star:
    def __init__(self):
        self.name = None
        self.spectral_class = None
        self.size_code = None
        self.spectral_specification = None
        self.luminosity = None
        self.mass = None
        self.surface_temperature = None
        self.radius = None
        self.e = None
        self.age = None
        self.classification = None
        self.assign_priority = 100
        self.pos = None
        self.planets = []
        self.planet_abundance = None
        self.lz_min = None
        self.lz_max = None
        self.peak_fq = None


class Orbit:
    def __init__(self):
        self.body = []
        self.mean_sep = None
        self.eccentricity = None
        self.min_sep = None
        self.max_sep = None
        self.period = None


class System:
    def __init__(self):
        self.content = []
        self.orbits = []
        self.type = None
        self.abundance = None
        self.pos = [0, 0, 0]
        self.dis = None
        self.neighbor = []
        self.number = None
        self.flag = None


class Planet:
    def __init__(self):
        self.designation = None
        self.semi_major_axis = None
        self.zone = None
        self.type = None
        self.trojan = False
        self.double = False
        self.strange = False
        self.radius = None
        self.density = None
        self.mass = None
        self.gravity = None
        self.ve = None
        self.year = None
        self.tidal_lock = False
        self.eccentricity = None
        self.min_sep = None
        self.max_sep = None
        self.axial = None
        self.rotation_period = None
        self.T = None
        self.solarday = None
        self.moon = []
        self.age = None
        self.luminosity = None
        self.surface_temp = None
        self.composition = None
        self.tectonic = None
        self.mag_field = None
        self.dominant_asteroid = None
        self.double_radius = None
        self.atmosphere = None
        self.pressure = None
        self.atm_comp = None
        self.hydro = None
        self.hyd_exten = None
        self.wvf = None  # water vapor factor
        self.scale_height = None
        self.atm_average_mol = None


class Lunar:
    def __init__(self):
        self.mass = None
        self.semi_axis = None
        self.radius = None
        self.density = None
        self.year = None
        self.gravity = None
        self.roche_limit = None
        self.strange = False
        self.type = None
        self.name = None
        self.composition = None
        self.tectonic = None
        self.surface_temp = None
        self.atmosphere = None
        self.ve = None
        self.pressure = None
        self.atm_comp = None
        self.hydro = None
        self.hyd_exten = None
        self.wvf = None  # water vapor factor
        self.scale_height = None
        self.atm_average_mol = None


def constellation_wrapper(density, number, start):
    def stellar_generation():  # 1.1.1
        star = Star()
        m = dice_1d(100)
        star.e = m
        basic_type = [
            [1, "A", 5],
            [4, "F", 5],
            [12, "G", 5],
            [26, "K", 5],
            [36, "WD", 7],
            [85, "M", 5],
            [98, "BD", 0],
            [99, "Gi", 3],
            [100, "B", 5],
        ]

        for _type in basic_type:
            if m <= _type[0]:
                star.spectral_class = _type[1]
                star.size_code = _type[2]
                break

        n = dice_1d(10)

        special_rules = [
            ["A", 7, 10, "A", 4],
            ["F", 9, 10, "F", 4],
            ["G", 10, 10, "G", 4],
            ["Gi", 1, 1, "F", 3],
            ["Gi", 2, 2, "G", 3],
            ["Gi", 3, 7, "K", 3],
            ["Gi", 8, 10, "K", 4],
        ]

        for rule in special_rules:
            if (star.spectral_class == rule[0]) and (rule[1] <= n <= rule[2]):
                star.spectral_class = rule[3]
                star.size_code = rule[4]

        star.spectral_specification = dice_1d(10) - 1

        if star.spectral_class == "K" and star.size_code == 4:
            star.spectral_specification = 0

        return star

    def system_generation(base_star):  # 1.1.2
        system = System()
        system.content.append(base_star)
        e = dice_1d(10)
        pos = 0
        while e >= 7 and len(system.content) <= 16:
            base_star = system.content[pos]
            o = dice_1d(10)
            if o <= 2:
                new_star = Star()
                new_star.spectral_class = base_star.spectral_class
                new_star.size_code = base_star.size_code
                new_star.e = base_star.e
                i = dice_1d(10)
                if i == 10:
                    i = 0
                if i < base_star.spectral_specification:
                    new_star.spectral_specification = base_star.spectral_specification
                else:
                    new_star.spectral_specification = i

                if new_star.spectral_class == "K" and new_star.size_code == 4:
                    new_star.spectral_specification = 0

            else:
                new_star = stellar_generation()
                if new_star.e < base_star.e or new_star.e == 100:
                    new_star.spectral_class = "BD"
                    new_star.size_code = 0
                    new_star.e = 98

            system.content.append(new_star)
            e = dice_1d(10)
            pos += 1
        return system

    def luminosity_mass(star):  # 1.1.3
        subgiant_modifier = [0, 0, -0.1, -0.2, -0.3, -0.4, 0.1, 0.2, 0.3, 0.4]
        giant_modifier = [
            [0.3, 0.3],
            [0.4, 0.4],
            [0.5, 0.5],
            [0.6, 0.6],
            [0.7, 0.7],
            [0.8, 0.8],
            [0.9, 0.9],
            [1, 1],
            [1.25, 1.5],
            [1.5, 2],
        ]

        def apply(target, lumin, mass, surfacetemp, radius):
            target.luminosity = lumin
            target.surface_temperature = surfacetemp
            target.mass = mass
            target.radius = radius
            return target

        def check(target, t_type, t_spec, t_size):
            type_s = target.spectral_class
            spec = target.spectral_specification
            size = target.size_code
            if type_s == t_type and t_size == size and t_spec == spec:
                return True
            else:
                return False

        def match(target, t_type, spec, size, lumin, mass, surfacetemp, radius):
            nonlocal search
            if check(target, t_type, spec, size) and search:
                apply(target, lumin, mass, surfacetemp, radius)
                search = False

        search = True
        if star.size_code == 5:  # Main sequence
            match(star, "A", 0, 5, 80, 3.0, 10000, 3)
            match(star, "A", 1, 5, 62, 2.8, 9750, 2.8)
            match(star, "A", 2, 5, 48, 2.6, 9500, 2.6)
            match(star, "A", 3, 5, 38, 2.5, 9250, 2.4)
            match(star, "A", 4, 5, 29, 2.3, 9000, 2.2)
            match(star, "A", 5, 5, 23, 2.2, 8750, 2.1)
            match(star, "A", 6, 5, 18, 2.0, 8500, 2.0)
            match(star, "A", 7, 5, 14, 1.9, 8250, 1.8)
            match(star, "A", 8, 5, 11, 1.8, 8000, 1.7)
            match(star, "A", 9, 5, 8.2, 1.7, 7750, 1.6)

            match(star, "B", 0, 5, 13000, 17.5, 28000, 4.9)
            match(star, "B", 1, 5, 7800, 15.1, 25000, 4.8)
            match(star, "B", 2, 5, 4700, 13.0, 22000, 4.8)
            match(star, "B", 3, 5, 2800, 11.1, 19000, 4.8)
            match(star, "B", 4, 5, 1700, 9.5, 17000, 4.8)
            match(star, "B", 5, 5, 1000, 8.2, 15000, 4.7)
            match(star, "B", 6, 5, 600, 7.0, 14000, 4.2)
            match(star, "B", 7, 5, 370, 6.0, 13000, 3.8)
            match(star, "B", 8, 5, 220, 5.0, 12000, 3.5)
            match(star, "B", 9, 5, 130, 4.0, 11000, 3.2)

            match(star, "F", 0, 5, 6.4, 1.6, 7500, 1.5)
            match(star, "F", 1, 5, 5.5, 1.53, 7350, 1.5)
            match(star, "F", 2, 5, 4.7, 1.47, 7200, 1.4)
            match(star, "F", 3, 5, 4.0, 1.42, 7050, 1.4)
            match(star, "F", 4, 5, 3.4, 1.36, 6900, 1.3)
            match(star, "F", 5, 5, 2.9, 1.31, 6750, 1.3)
            match(star, "F", 6, 5, 2.5, 1.26, 6600, 1.2)
            match(star, "F", 7, 5, 2.16, 1.21, 6450, 1.2)
            match(star, "F", 8, 5, 1.85, 1.17, 6300, 1.2)
            match(star, "F", 9, 5, 1.58, 1.12, 6150, 1.1)

            match(star, "G", 0, 5, 1.36, 1.08, 6000, 1.1)
            match(star, "G", 1, 5, 1.21, 1.05, 5900, 1.1)
            match(star, "G", 2, 5, 1.09, 1.02, 5800, 1.0)
            match(star, "G", 3, 5, 0.98, 0.99, 5700, 1.0)
            match(star, "G", 4, 5, 0.88, 0.96, 5600, 1.0)
            match(star, "G", 5, 5, 0.79, 0.94, 5500, 1.0)
            match(star, "G", 6, 5, 0.71, 0.92, 5400, 1.0)
            match(star, "G", 7, 5, 0.64, 0.89, 5300, 1.0)
            match(star, "G", 8, 5, 0.57, 0.87, 5200, 0.9)
            match(star, "G", 9, 5, 0.51, 0.85, 5100, 0.9)

            match(star, "K", 0, 5, 0.46, 0.82, 5000, 0.9)
            match(star, "K", 1, 5, 0.39, 0.79, 4850, 0.9)
            match(star, "K", 2, 5, 0.32, 0.75, 4700, 0.9)
            match(star, "K", 3, 5, 0.27, 0.72, 4550, 0.8)
            match(star, "K", 4, 5, 0.23, 0.69, 4400, 0.8)
            match(star, "K", 5, 5, 0.19, 0.66, 4250, 0.8)
            match(star, "K", 6, 5, 0.16, 0.63, 4100, 0.8)
            match(star, "K", 7, 5, 0.14, 0.61, 3950, 0.8)
            match(star, "K", 8, 5, 0.11, 0.56, 3800, 0.8)
            match(star, "K", 9, 5, 0.10, 0.49, 3650, 0.8)

            match(star, "M", 0, 5, 0.08, 0.46, 3500, 0.8)
            match(star, "M", 1, 5, 0.04, 0.38, 3350, 0.6)
            match(star, "M", 2, 5, 0.02, 0.32, 3200, 0.5)
            match(star, "M", 3, 5, 0.012, 0.26, 3050, 0.4)
            match(star, "M", 4, 5, 0.006, 0.21, 2900, 0.3)
            match(star, "M", 5, 5, 0.003, 0.18, 2750, 0.25)
            match(star, "M", 6, 5, 0.0017, 0.15, 2600, 0.2)
            match(star, "M", 7, 5, 0.0009, 0.12, 2450, 0.17)
            match(star, "M", 8, 5, 0.0005, 0.10, 2300, 0.14)
            match(star, "M", 9, 5, 0.0002, 0.08, 2200, 0.11)

        elif star.size_code == 4:  # sub-giants
            match(star, "A", 0, 4, 156, 6, 9700, 4.5)
            match(star, "A", 1, 4, 127, 5.1, 9450, 4.2)
            match(star, "A", 2, 4, 102, 4.6, 9200, 4.0)
            match(star, "A", 3, 4, 83, 4.3, 8950, 3.8)
            match(star, "A", 4, 4, 67, 4.0, 8700, 3.6)
            match(star, "A", 5, 4, 54, 3.7, 8450, 3.5)
            match(star, "A", 6, 4, 44, 3.4, 8200, 3.3)
            match(star, "A", 7, 4, 36, 3.1, 7950, 3.2)
            match(star, "A", 8, 4, 29, 2.9, 7700, 3.1)
            match(star, "A", 9, 4, 23, 2.7, 7500, 2.9)

            match(star, "F", 0, 4, 19, 2.5, 7300, 2.7)
            match(star, "F", 1, 4, 16.9, 2.4, 7200, 2.7)
            match(star, "F", 2, 4, 15.1, 2.3, 7100, 2.6)
            match(star, "F", 3, 4, 13.4, 2.2, 6950, 2.6)
            match(star, "F", 4, 4, 12.0, 2.1, 6800, 2.5)
            match(star, "F", 5, 4, 10.7, 2.0, 6650, 2.5)
            match(star, "F", 6, 4, 9.5, 1.95, 6500, 2.5)
            match(star, "F", 7, 4, 8.5, 1.90, 6350, 2.5)
            match(star, "F", 8, 4, 7.6, 1.80, 6200, 2.4)
            match(star, "F", 9, 4, 6.7, 1.70, 6050, 2.4)

            match(star, "G", 0, 4, 6.2, 1.60, 5900, 2.4)
            match(star, "G", 1, 4, 5.9, 1.55, 5750, 2.4)
            match(star, "G", 2, 4, 5.6, 1.52, 5600, 2.5)
            match(star, "G", 3, 4, 5.4, 1.49, 5450, 2.6)
            match(star, "G", 4, 4, 5.2, 1.47, 5300, 2.7)
            match(star, "G", 5, 4, 5.0, 1.45, 5200, 2.8)
            match(star, "G", 6, 4, 4.8, 1.44, 5100, 2.8)
            match(star, "G", 7, 4, 4.6, 1.43, 5000, 2.9)
            match(star, "G", 8, 4, 4.4, 1.42, 4900, 2.9)
            match(star, "G", 9, 4, 4.2, 1.41, 4800, 3.0)

            match(star, "K", 0, 4, 4, 1.40, 4700, 3.0)

            r = dice_1d(10) - 1
            star.mass *= subgiant_modifier[r] + 1
            star.luminosity *= subgiant_modifier[r] * 2 + 1

        elif star.size_code == 3:  # 1.1.3 Giants
            match(star, "A", 0, 3, 280, 12, 9500, 6.2)
            match(star, "A", 1, 3, 240, 11.5, 9250, 6.1)
            match(star, "A", 2, 3, 200, 11.0, 9000, 5.9)
            match(star, "A", 3, 3, 170, 10.5, 8750, 5.7)
            match(star, "A", 4, 3, 140, 10, 8500, 5.6)
            match(star, "A", 5, 3, 120, 9.6, 8250, 5.5)
            match(star, "A", 6, 3, 100, 9.2, 8000, 5.3)
            match(star, "A", 7, 3, 87, 8.9, 7750, 5.2)
            match(star, "A", 8, 3, 74, 8.6, 7500, 5.1)
            match(star, "A", 9, 3, 63, 8.3, 7350, 4.9)

            match(star, "F", 0, 3, 53, 8.0, 7200, 4.7)
            match(star, "F", 1, 3, 51, 7.0, 7050, 4.8)
            match(star, "F", 2, 3, 49, 6.0, 6900, 4.9)
            match(star, "F", 3, 3, 47, 5.2, 6750, 5.1)
            match(star, "F", 4, 3, 46, 4.7, 6600, 5.2)
            match(star, "F", 5, 3, 45, 4.3, 6450, 5.4)
            match(star, "F", 6, 3, 46, 3.9, 6300, 5.7)
            match(star, "F", 7, 3, 47, 3.5, 6150, 6.1)
            match(star, "F", 8, 3, 48, 3.1, 6000, 6.5)
            match(star, "F", 9, 3, 49, 2.8, 5900, 6.8)

            match(star, "G", 0, 3, 50, 2.5, 5800, 7.1)
            match(star, "G", 1, 3, 55, 2.4, 5700, 7.7)
            match(star, "G", 2, 3, 60, 2.5, 5600, 8.3)
            match(star, "G", 3, 3, 65, 2.5, 5500, 9.0)
            match(star, "G", 4, 3, 70, 2.6, 5400, 9.7)
            match(star, "G", 5, 3, 77, 2.7, 5250, 10.7)
            match(star, "G", 6, 3, 85, 2.7, 5100, 11.9)
            match(star, "G", 7, 3, 92, 2.8, 4950, 13.2)
            match(star, "G", 8, 3, 101, 2.8, 4800, 14.7)
            match(star, "G", 9, 3, 110, 2.9, 4650, 16.3)

            match(star, "K", 0, 3, 120, 3, 4500, 18.2)
            match(star, "K", 1, 3, 140, 3.3, 4400, 20.4)
            match(star, "K", 2, 3, 160, 3.6, 4300, 22.8)
            match(star, "K", 3, 3, 180, 3.9, 4200, 25.6)
            match(star, "K", 4, 3, 210, 4.2, 4100, 28.8)
            match(star, "K", 5, 3, 240, 4.5, 4000, 32.4)
            match(star, "K", 6, 3, 270, 4.8, 3900, 36.5)
            match(star, "K", 7, 3, 310, 5.1, 3800, 41.2)
            match(star, "K", 8, 3, 360, 5.4, 3700, 46.5)
            match(star, "K", 9, 3, 410, 5.8, 3550, 54)

            r = dice_1d(10) - 1
            star.mass *= giant_modifier[r][0]
            star.luminosity *= giant_modifier[r][1]

    def age(system):
        def assign(star, mass, radius):
            star.mass = mass
            star.radius = radius

        def handle_dwarves(star, rng, age):
            if star.size_code == 7:
                WD_list = [
                    [1.3, 0.004],
                    [1.1, 0.007],
                    [0.9, 0.009],
                    [0.7, 0.010],
                    [0.6, 0.011],
                    [0.55, 0.012],
                    [0.5, 0.013],
                    [0.45, 0.014],
                    [0.4, 0.015],
                    [0.35, 0.016],
                ]
                assign(star, WD_list[rng][0], WD_list[rng][1])

                temp_dict = {
                    1: 30000,
                    2: 25000,
                    3: 20000,
                    4: 16000,
                    5: 14000,
                    6: 12000,
                    7: 10000,
                    8: 8000,
                    9: 6000,
                    0: 4000,
                }
                q = ((age - 1) // 2) - 4 + rng  # modified age/tempreature roll
                q = max(min(q, 9), 0)
                star.surface_temperature = temp_dict[q]

            elif star.size_code == 0:

                BD_list = {
                    1: [0.07, 0.07],
                    2: [0.064, 0.08],
                    3: [0.058, 0.09],
                    4: [0.052, 0.1],
                    5: [0.046, 0.11],
                    6: [0.04, 0.12],
                    7: [0.034, 0.12],
                    8: [0.026, 0.12],
                    9: [0.020, 0.12],
                    0: [0.0014, 0.12],
                }

                assign(star, BD_list[rng][0], BD_list[rng][1])

                temp_dict = {
                    1: 2200,
                    2: 2000,
                    3: 1800,
                    4: 1600,
                    5: 1400,
                    6: 1200,
                    7: 1000,
                    8: 900,
                    9: 800,
                    0: 700,
                }
                mod_list = [0, 1, 1, 2, 2, 3, 4, 5, 6, 7]
                q = mod_list[age - 1] + rng  # modified age/tempreature roll
                q = max(min(q, 9), 0)
                star.surface_temperature = temp_dict[q]
            star.luminosity = (
                star.radius ** 2 * star.surface_temperature ** 4 / 5800 ** 4
            )
            if star.age is None:
                star.age = age

        def roll_age(system):
            primary = system.content[0]
            id_0 = primary.spectral_class
            id_1 = primary.spectral_specification
            id_2 = primary.size_code

            n = dice_1d(10) - 1  # dwarf star random generation sequencer
            r = dice_1d(10)  # main age multiplyer

            if id_2 == 5:
                if id_0 == "B":
                    L = 0.1
                elif id_0 == "A":
                    if id_1 <= 4:
                        L = 0.6
                    else:
                        L = 1.2
                elif id_0 == "F":
                    if id_1 <= 4:
                        L = 3.2
                    else:
                        L = 5
                else:
                    L = 10

                primary.age = L * r / 10

            elif id_2 == 4 or id_2 == 3:

                primary.age = 10 * primary.mass / primary.luminosity

            elif id_2 == 7 or id_2 == 0:
                handle_dwarves(primary, n, r)

            for star in system.content:
                star.age = primary.age

        def assign_lum_by_age(star):
            id_0 = star.spectral_class
            id_1 = star.spectral_specification
            id_2 = star.size_code
            mod = 0

            if id_2 == 5:
                if id_0 == "A":
                    if id_1 <= 4:
                        mod = 0
                    else:
                        num = star.age / 1.2 * 10
                        x = (num + 1) // 2
                        mod = x * 0.1 - 0.2

                elif id_0 == "F":
                    if id_1 <= 4:
                        num = star.age / 3.2 * 10
                        mod = int(num) * 0.1 - 0.5
                    else:
                        num = star.age / 5 * 10
                        mod = int(num) * 0.1 - 0.5

                elif id_0 == "G":
                    if id_1 <= 4:
                        num = star.age
                        mod = int(num) * 0.1 - 0.5

                    else:
                        num = star.age / 12 * 10
                        mod = int(num) * 0.1 - 0.5

                elif id_0 == "K":
                    if id_1 <= 4:
                        num = star.age
                        if num <= 5:
                            mod = int(num) * 0.05 - 0.25
                        elif num <= 9:
                            mod = 0
                        else:
                            mod = 0.05
                    else:
                        num = star.age
                        if num <= 1.05:
                            mod = -0.1
                        elif num <= 2.05:
                            mod = -0.05

                elif id_0 == "M":
                    num = star.age
                    if num <= 1.05:
                        mod = 0.1

                mod += 1
                star.luminosity *= mod

            elif id_2 == 4:
                star.luminosity *= 1.1

            elif id_2 == 3:
                star.luminosity *= 1.2

            elif id_2 == 0 or id_2 == 7:
                handle_dwarves(star, dice_1d(10) - 1, int(round(star.age)))

        roll_age(system)
        p = rnd(2, 10)
        p += system.content[0].age
        if p <= 9:
            system.abundance = 2
        elif p <= 12:
            system.abundance = 1
        elif p <= 18:
            system.abundance = 0
        elif p <= 21:
            system.abundance = -1
        else:
            system.abundance = -3

        for star in system.content:
            assign_lum_by_age(star)

    def assign_orbit(system):
        system.orbits = []
        system.type = None

        def mean_sep(orbit):
            r = dice_1d(10)
            if r <= 3:
                orbit.mean_sep = dice_1d(10) * 0.05
            elif r <= 6:
                orbit.mean_sep = dice_1d(10) * 0.5
            elif r <= 8:
                orbit.mean_sep = dice_1d(10) * 3
            elif r == 9:
                orbit.mean_sep = dice_1d(10) * 20
            elif r == 10:
                orbit.mean_sep = dice_1d(100) * 200

        def orb_ecc(orbit):
            r = dice_1d(10)
            if orbit.mean_sep <= 0.5:
                r -= 2
            elif orbit.mean_sep <= 5:
                r -= 1

            if r <= 2:
                orbit.eccentricity = dice_1d(10) * 0.01
            elif r <= 4:
                orbit.eccentricity = dice_1d(10) * 0.01 + 0.1
            elif r <= 6:
                orbit.eccentricity = dice_1d(10) * 0.01 + 0.2
            elif r <= 8:
                orbit.eccentricity = dice_1d(10) * 0.01 + 0.3
            elif r == 9:
                orbit.eccentricity = dice_1d(10) * 0.01 + 0.4
            elif r == 10:
                orbit.eccentricity = dice_1d(10) * 0.01 + 0.5

        def mk_orbit(orbit):
            while True:
                mean_sep(orbit)
                orb_ecc(orbit)
                orbit.min_sep = (1 - orbit.eccentricity) * orbit.mean_sep
                orbit.max_sep = (1 + orbit.eccentricity) * orbit.mean_sep
                orbit.period = (
                    orbit.mean_sep ** 3 / (orbit.body[0].mass + orbit.body[1].mass)
                ) ** 0.5
                if (
                    orbit.min_sep
                    > (orbit.body[0].radius + orbit.body[1].radius) * 0.00465
                ):
                    break

        def modify_orbit(orbit, scale):
            if (
                orbit.min_sep * scale
                > (orbit.body[0].radius + orbit.body[1].radius) * 0.00465
            ):
                orbit.mean_sep *= scale
                orbit.min_sep *= scale
                orbit.max_sep *= scale
                orbit.period = (
                    orbit.mean_sep ** 3 / (orbit.body[0].mass + orbit.body[1].mass)
                ) ** 0.5

        classification_list = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
        ]
        for star in system.content:
            n = system.content.index(star)
            star.classification = classification_list[n]

        if len(system.content) > 1:
            AB_orbit = Orbit()
            A = system.content[0]
            B = system.content[1]
            AB_orbit.body.append(A)
            AB_orbit.body.append(B)
            mk_orbit(AB_orbit)
            system.orbits.append(AB_orbit)
            system.type = "[AB]"

            if len(system.content) > 2:
                C = system.content[2]
                r = dice_1d(10)
                if AB_orbit.min_sep <= 0.15 and len(system.content) == 3:
                    r = max(r, 7)
                elif AB_orbit.min_sep <= 0.45 and len(system.content) > 3:
                    r = max(r, 7)
                elif AB_orbit.max_sep >= 6666 and len(system.content) == 3:
                    r = min(r, 6)
                elif AB_orbit.max_sep >= 2222 and len(system.content) > 3:
                    r = min(r, 6)

                if r <= 3:  # orbits A
                    AC_orbit = Orbit()
                    AC_orbit.body.append(A)
                    AC_orbit.body.append(C)
                    while True:
                        mk_orbit(AC_orbit)
                        if AC_orbit.max_sep <= AB_orbit.min_sep / 3:
                            break

                    system.orbits.append(AC_orbit)
                    system.type = "[[AC]B]"

                elif r <= 6:  # orbits B
                    BC_orbit = Orbit()
                    BC_orbit.body.append(B)
                    BC_orbit.body.append(C)
                    while True:
                        mk_orbit(BC_orbit)
                        if BC_orbit.max_sep <= AB_orbit.min_sep / 3:
                            break
                    system.orbits.append(BC_orbit)
                    system.type = "[A[BC]]"

                elif r <= 10:  # orbits AB barycenter
                    AB_bary = Star()
                    AB_bary.classification = "A-B"
                    AB_bary.mass = A.mass + B.mass
                    AB_bary.radius = A.radius + B.radius
                    ABC_orbit = Orbit()
                    ABC_orbit.body.append(AB_bary)
                    ABC_orbit.body.append(C)
                    while True:
                        mk_orbit(ABC_orbit)
                        if ABC_orbit.min_sep >= AB_orbit.max_sep * 3:
                            break
                    system.orbits.append(ABC_orbit)
                    system.type = "[[AB]C]"

                if len(system.content) > 3:
                    D = system.content[3]
                    e = dice_1d(10)
                    if e <= 7:  # CD
                        CD_orbit = Orbit()
                        CD_orbit.body.append(C)
                        CD_orbit.body.append(D)
                        mk_orbit(CD_orbit)
                        while True:
                            if r <= 3:
                                if CD_orbit.max_sep <= AC_orbit.min_sep / 3:
                                    system.type = "[[A[CD]]B]"
                                    break
                                else:
                                    modify_orbit(CD_orbit, 0.75)
                            elif r <= 6:
                                if CD_orbit.max_sep <= BC_orbit.min_sep / 3:
                                    system.type = "[A[B[CD]]]"
                                    break
                                else:
                                    modify_orbit(CD_orbit, 0.75)
                            elif r <= 10:
                                if CD_orbit.max_sep <= ABC_orbit.min_sep / 3:
                                    system.type = "[[AB][CD]]"
                                    break
                                else:
                                    modify_orbit(CD_orbit, 0.75)

                        system.orbits.append(CD_orbit)

                    elif e <= 9:  # ABC-D
                        ABC_bary = Star()
                        ABC_bary.mass = A.mass + B.mass + C.mass
                        ABC_bary.radius = A.radius + B.radius + C.radius
                        ABC_bary.classification = "A-B-C"
                        ABCD_orbit = Orbit()
                        ABCD_orbit.body.append(ABC_bary)
                        ABCD_orbit.body.append(D)
                        max_sep = []
                        for i in range(0, 2):
                            max_sep.append(system.orbits[i].max_sep)
                        mk_orbit(ABCD_orbit)
                        while True:
                            if ABCD_orbit.min_sep >= max(max_sep) * 3:
                                break
                            else:
                                modify_orbit(ABCD_orbit, 1.25)
                        system.orbits.append(ABCD_orbit)
                        system.type = "[" + system.type + "D]"

                    elif e == 10:  # close-paired trinary
                        n = dice_1d(10)
                        if n <= 7:
                            AD_orbit = Orbit()
                            AD_orbit.body.append(A)
                            AD_orbit.body.append(D)
                            min_sep = []
                            for i in range(0, 2):
                                if A in system.orbits[i].body:
                                    min_sep.append(system.orbits[i].min_sep)
                            mk_orbit(AD_orbit)
                            while True:
                                if AD_orbit.max_sep <= min(min_sep) / 3:
                                    break
                                else:
                                    modify_orbit(AD_orbit, 0.75)

                            system.orbits.append(AD_orbit)
                            system.type = system.type.replace("A", "[AD]")
                            # print('replaced')

                        else:
                            BD_orbit = Orbit()
                            BD_orbit.body.append(B)
                            BD_orbit.body.append(D)
                            min_sep = []
                            for i in range(0, 2):
                                if B in system.orbits[i].body:
                                    min_sep.append(system.orbits[i].min_sep)
                            mk_orbit(BD_orbit)
                            while True:
                                if BD_orbit.max_sep <= min(min_sep) / 3:
                                    break
                                else:
                                    modify_orbit(BD_orbit, 0.75)

                            system.orbits.append(BD_orbit)
                            system.type = system.type.replace("B", "[BD]")

                    if len(system.content) > 4:

                        for star in system.content:
                            star.assign_priority = 100

                        for i in range(0, len(system.content) - 4):
                            X = system.content[i + 4]
                            for e in range(0, i + 4):
                                system.content[e].assign_priority = 0
                            for orbit in system.orbits:
                                for star in system.content:
                                    if star in orbit.body:
                                        star.assign_priority += 1
                            priority_list = []
                            for star in system.content:
                                priority_list.append(star.assign_priority)

                            loneliest = system.content[
                                priority_list.index(min(priority_list))
                            ]

                            k = dice_1d(10)
                            if k <= 7:

                                L = loneliest
                                #  print(L.classification,priority_list)
                                LX_orbit = Orbit()
                                LX_orbit.body.append(L)
                                LX_orbit.body.append(X)
                                min_sep = []
                                for e in range(0, i + 4 - 1):
                                    if L in system.orbits[e].body:
                                        min_sep.append(system.orbits[e].min_sep)
                                mk_orbit(LX_orbit)
                                while True:
                                    if LX_orbit.max_sep <= min(min_sep) / 3:
                                        break
                                    else:
                                        modify_orbit(LX_orbit, 0.75)
                                system.orbits.append(LX_orbit)
                                system.type = system.type.replace(
                                    L.classification,
                                    "[" + L.classification + X.classification + "]",
                                )
                            else:
                                All_bary = Star()
                                All_bary.radius = All_bary.mass = 0
                                All_bary.classification = ""
                                for e in range(0, i + 4):
                                    if e != 0:
                                        All_bary.classification += "-"
                                    All_bary.mass += system.content[e].mass
                                    All_bary.radius += system.content[e].radius
                                    All_bary.classification += system.content[
                                        e
                                    ].classification
                                AllX_orbit = Orbit()
                                AllX_orbit.body.append(All_bary)
                                AllX_orbit.body.append(X)
                                max_sep = []
                                for e in range(0, i + 4 - 1):
                                    max_sep.append(system.orbits[e].max_sep)
                                mk_orbit(AllX_orbit)
                                while True:
                                    if AllX_orbit.min_sep >= max(max_sep) * 3:
                                        break
                                    else:
                                        modify_orbit(AllX_orbit, 1.25)
                                system.orbits.append(AllX_orbit)
                                system.type = "[" + system.type + X.classification + "]"

    def planet_wrapper(system):
        def add_planet(system):
            def calculate_modifier(system):
                abundance = -1 * system.abundance
                for star in system.content:
                    a, b, c = (
                        star.spectral_class,
                        star.spectral_specification,
                        star.size_code,
                    )
                    if a == "K":
                        if b >= 5:
                            abundance += 1
                    elif a == "M":
                        if b <= 4:
                            abundance += 2
                        else:
                            abundance += 3
                    elif a == "BD":
                        abundance += 5

                    if abundance == 1:
                        star.planet_abundance = dice_1d(10) + 10
                    elif abundance <= 5:
                        star.planet_abundance = dice_1d(10) + 5
                    elif abundance <= 7:
                        star.planet_abundance = dice_1d(10)
                    elif abundance <= 9:
                        star.planet_abundance = int(dice_1d(10) / 2)
                    else:
                        star.planet_abundance = 0

            def assign_slot(system):
                import math

                for star in system.content:
                    dis = []
                    parent_mass = star.mass
                    e = star.planet_abundance

                    for orbit in system.orbits:
                        for body in orbit.body:
                            if star.classification in body.classification:
                                dis.append(orbit.mean_sep)

                    if len(dis) == 0:
                        first_planet = Planet()
                        first_planet.semi_major_axis = (
                            0.05 * parent_mass ** 2 * dice_1d(10)
                        )
                        star.planets.append(first_planet)
                        previous_planet = first_planet
                        while e > 0:
                            planet = Planet()
                            planet.semi_major_axis = (
                                previous_planet.semi_major_axis
                                * (1.1 + dice_1d(10) * 0.1)
                                + 0.1
                            )
                            star.planets.append(planet)
                            e -= 1
                            previous_planet = planet
                    else:
                        first_planet_semi_major_axis = (
                            0.05 * parent_mass ** 2 * dice_1d(10)
                        )
                        dis.sort(reverse=False)
                        max_orbit_sma = dis[0] / 3
                        min_circumbinary_sma = dis[0] * 3
                        if len(dis) > 1:
                            max_circumbinary_sma = dis[1] / 3
                        else:
                            max_circumbinary_sma = math.inf
                        first = True
                        while e > 0:
                            planet = Planet()
                            if first:
                                planet.semi_major_axis = first_planet_semi_major_axis
                                first = False
                            else:
                                planet.semi_major_axis = (
                                    previous_planet.semi_major_axis
                                    * (1.1 + dice_1d(10))
                                    + 0.1
                                )
                            if planet.semi_major_axis <= max_orbit_sma:
                                star.planets.append(planet)
                            elif (
                                max_circumbinary_sma
                                >= planet.semi_major_axis
                                >= min_circumbinary_sma
                            ):
                                star.planets.append(planet)
                            e -= 1
                            previous_planet = planet

                    if star.spectral_class == "WD":
                        x = dice_1d(10)
                        if star.mass > 0.9:
                            x += 4
                        elif 0.9 > star.mass > 0.6:
                            x += 2

                        if x <= 4:
                            min_sma = 2
                        elif x <= 8:
                            min_sma = 4
                        elif x <= 11:
                            min_sma = 6
                        else:
                            min_sma = 10

                        remain = []
                        for planet in star.planets:
                            if planet.semi_major_axis < min_sma:
                                pass
                            else:
                                remain.append(planet)
                        star.planets = remain

                    untenable_thermal = 0.025 * star.luminosity ** (1 / 2)
                    zone_line = 4 * star.luminosity ** 0.5

                    for planet in star.planets:
                        if planet.semi_major_axis < zone_line:
                            planet.zone = "Inner"
                        else:
                            planet.zone = "Outer"

                    remain = []
                    for planet in star.planets:
                        if planet.semi_major_axis < untenable_thermal:
                            pass
                        else:
                            remain.append(planet)

                    if star.size_code != 5 or star.spectral_class == "WD":
                        for planet in star.planets:
                            if planet.semi_major_axis < zone_line:
                                if planet in remain:
                                    remain.remove(planet)

                    star.planets = remain

            calculate_modifier(system)
            assign_slot(system)

        def assign_name(system):
            listed = [
                "I",
                "II",
                "III",
                "IV",
                "V",
                "VI",
                "VII",
                "IIX",
                "IX",
                "X",
                "XI",
                "XII",
                "XIII",
                "XIV",
                "XV",
                "XVI",
                "XVII",
                "XIIX",
                "XIX",
                "XX",
                "XXI",
            ]
            for star in system.content:
                star.planets = sorted(
                    star.planets, key=lambda planet: planet.semi_major_axis
                )
                prev = 0
                x = 0
                new_list = []
                for planet in star.planets:
                    if "Asteroid" not in planet.type:
                        new_list.append(planet)
                for planet in new_list:
                    p = new_list.index(planet)
                    if planet.semi_major_axis == prev:
                        x += 1
                    planet.designation = listed[p - x]
                    if planet.semi_major_axis == prev:
                        planet.designation += "-2"
                        i = new_list.index(planet)
                        new_list[i - 1].designation += "-1"
                    prev = planet.semi_major_axis

                    """if planet.double is True:
                        planet.designation += 'D'
                    if planet.trojan is True:
                        planet.designation += 'T'"""
                e = 0
                for planet in star.planets:
                    if planet.designation is None:
                        e += 1
                        planet.designation = str(e)

        def define_planet_type(system):
            def roll_inner():
                x = dice_1d(100)
                if x <= 18:
                    planet_type = "Asteroid Belt"
                elif x <= 62:
                    planet_type = "Terrestrial"
                elif x <= 71:
                    planet_type = "Planetesimal"
                elif x <= 82:
                    planet_type = "Gas Giant"
                elif x <= 86:
                    planet_type = "Superjovian"
                elif x <= 96:
                    planet_type = "Empty"
                elif x <= 97:
                    planet_type = "Interloper"
                elif x <= 98:
                    planet_type = "Trojan"
                elif x <= 99:
                    planet_type = "Double"
                else:
                    planet_type = "Captured"
                return planet_type, x

            def roll_outer():
                x = dice_1d(100)
                if x <= 15:
                    planet_type = "Asteroid Belt"
                elif x <= 23:
                    planet_type = "Terrestrial"
                elif x <= 35:
                    planet_type = "Planetesimal"
                elif x <= 74:
                    planet_type = "Gas Giant"
                elif x <= 84:
                    planet_type = "Superjovian"
                elif x <= 94:
                    planet_type = "Empty"
                elif x <= 95:
                    planet_type = "Interloper"
                elif x <= 97:
                    planet_type = "Trojan"
                elif x <= 99:
                    planet_type = "Double"
                else:
                    planet_type = "Captured"
                return planet_type, x

            for star in system.content:
                for planet in star.planets:
                    if planet.zone == "Inner":
                        planet_type, x = roll_inner()
                        if planet_type == "Empty":
                            planet.type = "Deleted"

                        elif planet_type == "Interloper":
                            planet.zone = "Outer"
                            while 1 > 0:
                                planet.type, x = roll_outer()
                                if 16 <= x <= 74:
                                    break
                        elif planet_type == "Trojan":
                            k = dice_1d(10)
                            if k == 1:
                                planet.type = "Terrestrial"
                            else:
                                planet.type = "Gas Giant"
                            m = dice_1d(10)
                            trojan = Planet()
                            if m == 1:
                                trojan.type = "Terrestrial"
                            else:
                                trojan.type = "Planetesimal"
                            trojan.semi_major_axis = planet.semi_major_axis
                            star.planets.append(trojan)
                            trojan.trojan = True
                        elif planet_type == "Double":
                            while 1 > 0:
                                planet.type, x = roll_inner()
                                if 19 <= x <= 86:
                                    break
                            double = Planet()
                            double.semi_major_axis = planet.semi_major_axis
                            while 1 > 0:
                                double.type, x = roll_inner()
                                if 19 <= x <= 86:
                                    break
                            star.planets.append(double)
                            double.double = True
                        elif planet_type == "Captured":
                            planet.strange = True
                            while 1 > 0:
                                planet.type, x = roll_inner()
                                if 19 <= x <= 86:
                                    break
                        if planet.type is None:
                            planet.type = planet_type

                    if planet.zone == "Outer":
                        planet_type, x = roll_outer()
                        if planet_type == "Empty":
                            planet.type = "Deleted"

                        elif planet_type == "Interloper":
                            planet.zone = "Inner"
                            while 1 > 0:
                                planet.type, x = roll_outer()
                                if 19 <= x <= 82:
                                    break
                        elif planet_type == "Trojan":
                            k = dice_1d(10)
                            if k == 1:
                                planet.type = "Terrestrial"
                            else:
                                planet.type = "Gas Giant"
                            trojan = Planet()
                            m = dice_1d(10)
                            if m == 1:
                                trojan.type = "Terrestrial"
                            else:
                                trojan.type = "Planetesimal"
                            trojan.semi_major_axis = planet.semi_major_axis
                            star.planets.append(trojan)
                            trojan.trojan = True
                        elif planet_type == "Double":
                            while 1 > 0:
                                planet.type, x = roll_outer()
                                if 16 <= x <= 84:
                                    break
                            double = Planet()
                            double.semi_major_axis = planet.semi_major_axis
                            while 1 > 0:
                                double.type, x = roll_outer()
                                if 16 <= x <= 84:
                                    break
                            star.planets.append(double)
                            double.double = True
                        elif planet_type == "Captured":
                            planet.strange = True
                            while 1 > 0:
                                planet.type, x = roll_outer()
                                if 16 <= x <= 84:
                                    break
                        if planet.type is None:
                            planet.type = planet_type

            for star in system.content:
                remain = []
                for planet in star.planets:
                    if planet.type == "Deleted":
                        pass
                    else:
                        remain.append(planet)
                star.planets = remain

            def assign_size(system):
                for star in system.content:
                    for planet in star.planets:
                        x = dice_1d(10)
                        if x != 1:
                            x += system.abundance
                        if planet.type == "Planetesimal":
                            planet.radius = x * 200
                        elif planet.type == "Terrestrial":
                            if x <= 2:
                                planet.radius = 2000 + dice_1d(10) * 100
                            elif x <= 4:
                                planet.radius = 3000 + dice_1d(10) * 100
                            elif x <= 5:
                                planet.radius = 4000 + dice_1d(10) * 100
                            elif x <= 6:
                                planet.radius = 5000 + dice_1d(10) * 100
                            elif x <= 7:
                                planet.radius = 6000 + dice_1d(10) * 100
                            elif x <= 8:
                                planet.radius = 7000 + dice_1d(10) * 100
                            elif x <= 9:
                                planet.radius = 8000 + dice_1d(10) * 200
                            else:
                                planet.radius = 10000 + dice_1d(10) * 500
                        elif planet.type == "Gas Giant":
                            primary_mod = [
                                15000,
                                18000,
                                21000,
                                24000,
                                27000,
                                30000,
                                40000,
                                50000,
                                60000,
                                70000,
                            ]
                            secondary_mod = [300] * 5 + [1000] * 5
                            x -= 1
                            if x < 0:
                                x = 0
                            elif x > 9:
                                x = 9
                            planet.radius = primary_mod[x] + secondary_mod[x] * dice_1d(
                                10
                            )

            assign_size(system)

            def assign_density(system):
                for star in system.content:
                    for planet in star.planets:
                        if (
                            planet.type == "Planetesimal"
                            or planet.type == "Asteroid Belt"
                        ):
                            if planet.zone == "Inner":
                                planet.density = (
                                    0.3
                                    + (dice_1d(10) + system.abundance)
                                    * 0.127
                                    / (
                                        0.4
                                        + (
                                            planet.semi_major_axis
                                            / star.luminosity ** 0.5
                                        )
                                    )
                                    ** 0.67
                                )
                            else:
                                planet.density = (
                                    0.1 + (dice_1d(10) + system.abundance) * 0.05
                                )
                        elif planet.type == "Terrestrial":
                            if planet.zone == "Inner":
                                planet.density = (
                                    0.3
                                    + (dice_1d(10) + system.abundance)
                                    * 0.127
                                    / (
                                        0.4
                                        + (
                                            planet.semi_major_axis
                                            / star.luminosity ** 0.5
                                        )
                                    )
                                    ** 0.67
                                )
                            else:
                                planet.density = (
                                    0.1 + (dice_1d(10) + system.abundance) * 0.05
                                )
                        elif planet.type == "Gas Giant":
                            if planet.zone == "Inner":
                                planet.density = (
                                    0.1 + (dice_1d(10) + system.abundance) * 0.025
                                )
                            else:
                                planet.density = (
                                    0.08 + (dice_1d(10) + system.abundance) * 0.025
                                )

            assign_density(system)

            def assign_mdve(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.radius and planet.density is not None:
                            planet.mass = (planet.radius / 6380) ** 3 * planet.density
                            planet.gravity = planet.mass / (planet.radius / 6380) ** 2
                            planet.ve = (
                                19600 * planet.gravity * planet.radius
                            ) ** 0.5 / 11200

            assign_mdve(system)

            def assign_super_jovian(system):
                import math

                for star in system.content:
                    for planet in star.planets:
                        if planet.type == "Superjovian":
                            x = dice_1d(10)
                            x -= 1
                            mod_prime = [
                                500,
                                500,
                                500,
                                500,
                                1000,
                                1000,
                                1000,
                                2000,
                                2000,
                                3000,
                            ]
                            mod_second = [50, 50, 50, 50, 100, 100, 100, 100, 100, 100]
                            planet.mass = mod_prime[x] + mod_second[x] * dice_1d(10)
                            planet.radius = (
                                60000 + (dice_1d(10) - 1 / 2 * star.age) * 2000
                            )
                            planet.gravity = planet.mass / (planet.radius / 6380) ** 2
                            planet.ve = (
                                19600 * planet.gravity * planet.radius
                            ) ** 0.5 / 11200
                            planet.density = planet.mass / (planet.radius / 6380) ** 3

            assign_super_jovian(system)

            def modify_age_for_captured(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.strange:
                            planet.age = dice_1d(10)
                        else:
                            planet.age = star.age

            modify_age_for_captured(system)

        def moon_around_planet(system):
            for star in system.content:
                for planet in star.planets:
                    if (
                        not planet.double
                        and not planet.trojan
                        and not planet.tidal_lock
                    ):
                        x = dice_1d(10)
                        if planet.zone == "Outer":
                            x += 5
                        e = 0
                        if planet.type == "Planetesimal":
                            if x >= 10:
                                e = 1
                        elif planet.type == "Terrestrial":
                            if 6 <= x <= 7:
                                e = 1
                            elif 8 <= x <= 9:
                                e = int(dice_1d(10) / 5)
                            elif 10 <= x <= 13:
                                e = int(dice_1d(10) / 2)
                            elif x >= 14:
                                e = dice_1d(10)

                        elif planet.type == "Gas Giant" or planet.type == "Superjovian":
                            if 1 <= x <= 5:
                                e = int(dice_1d(10) / 2)
                            elif 6 <= x <= 7:
                                e = dice_1d(10)
                            elif 8 <= x <= 9:
                                e = dice_1d(10) + 5
                            elif 10 <= x <= 13:
                                e = dice_1d(10) + 10
                            elif x >= 14:
                                e = dice_1d(10) + 20

                        while e > 1:
                            sat = Lunar()
                            planet.moon.append(sat)
                            e -= 1

            for star in system.content:
                for planet in star.planets:
                    if len(planet.moon) > 0:
                        for moon in planet.moon:
                            x = dice_1d(10)
                            if x <= 4:
                                moon.semi_axis = 1 + dice_1d(10) * 0.5
                            elif x <= 6:
                                moon.semi_axis = 6 + dice_1d(10) * 1
                            elif x <= 8:
                                moon.semi_axis = 16 + dice_1d(10) * 3
                            elif x <= 9:
                                moon.semi_axis = 45 + dice_1d(100) * 3
                            else:
                                moon.strange = True
                                moon.semi_axis = 10 + dice_1d(10) * 2
                            moon.semi_axis *= planet.radius

                        for moon in planet.moon:
                            x = dice_1d(100)
                            mod = system.abundance
                            if mod < 0:
                                mod *= 2
                            x += mod
                            if x <= 64:
                                moon.radius = dice_1d(10) * 10
                                moon.type = "(S)Planetesimal"
                            elif x <= 84:
                                moon.radius = dice_1d(10) * 100
                                moon.type = "Planetesimal"
                            elif x <= 94:
                                moon.radius = 1000 + dice_1d(10) * 100
                                moon.type = "(L)Planetesimal"
                            elif x <= 99:
                                moon.radius = 2000 + dice_1d(10) * 200
                                moon.type = "(S)Terrestrial"
                            else:
                                moon.radius = 4000 + dice_1d(10) * 400
                                moon.type = "Terrestrial"
                            if planet.zone == "Inner":
                                moon.density = 0.3 + dice_1d(10) * 0.1
                            else:
                                moon.density = 0.1 + dice_1d(10) * 0.05
                            if (
                                planet.type == "Gas Giant"
                                or planet.type == "Superjovian"
                            ):
                                if planet.zone == "Outer" and planet.mass > 200:
                                    q = dice_1d(10)  # captured chance
                                    dis = 7 + planet.mass / 300
                                    dis *= planet.radius
                                    if q <= 5:
                                        if moon.semi_axis <= dis:
                                            moon.density *= 2
                                        elif moon.semi_axis <= 1.5 * dis:
                                            moon.density *= 1.5
                                    else:
                                        pass

                        for moon in planet.moon:
                            moon.mass = (moon.radius / 6380) ** 3 * moon.density
                            moon.gravity = moon.mass / (moon.radius / 6380) ** 2
                            moon.year = (
                                (moon.semi_axis / 400000) ** 3
                                * 793.64
                                / (moon.mass + planet.mass)
                            ) * 0.5
                            moon.roche_limit = (
                                2.456 * (planet.density / moon.density) ** 0.33
                            )
                            moon.roche_limit *= planet.radius
                            if moon.semi_axis <= moon.roche_limit:
                                moon.type = "Ring"
                                moon.radius = None
                                moon.gravity = None

            for star in system.content:
                for planet in star.planets:
                    if planet.double:
                        assign = planet.semi_major_axis
                        for parent in star.planets:
                            if parent.semi_major_axis == assign:
                                break
                        x = dice_1d(10)
                        if x <= 4:
                            planet.double_radius = 1 + dice_1d(10) * 0.5
                        elif x <= 6:
                            planet.double_radius = 6 + dice_1d(10) * 1
                        elif x <= 8:
                            planet.double_radius = 16 + dice_1d(10) * 3
                        elif x <= 9:
                            planet.double_radius = 45 + dice_1d(100) * 3
                        else:
                            planet.double_radius = 10 + dice_1d(10) * 2
                        planet.double_radius *= parent.radius

            for star in system.content:
                for planet in star.planets:
                    planet.moon = sorted(planet.moon, key=lambda moon: moon.semi_axis)
                    list_name = [
                        "a",
                        "b",
                        "c",
                        "d",
                        "e",
                        "f",
                        "g",
                        "h",
                        "i",
                        "j",
                        "k",
                        "l",
                        "m",
                        "n",
                        "o",
                        "p",
                        "q",
                        "r",
                        "s",
                        "t",
                        "u",
                        "v",
                        "w",
                        "x",
                        "y",
                        "z",
                    ]
                    new_list = []
                    for i in list_name:
                        new = "a" + i
                        new_list.append(new)
                    list_name += new_list
                    x = 0
                    ring_count = 0
                    for moon in planet.moon:
                        if moon.type is not "Ring":
                            moon.name = list_name[x]
                            x += 1
                        else:
                            ring_count += 1

                            moon.name = str(ring_count)

        def orbit_planet(system):
            def year_tidal(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.mass is not None:
                            import math

                            planet.year = (
                                planet.semi_major_axis ** 3
                                / (star.mass + planet.mass / 332946)
                            ) ** 0.5
                            tidal = (
                                (star.mass + planet.mass / 332946)
                                * 26640000
                                / (planet.semi_major_axis * 400) ** 3
                            )
                            planet.T = tidal
                            factor = (
                                (0.83 + dice_1d(10) * 0.03) * tidal * star.age / 6.6
                            )
                            if math.log(factor, 10) >= 1:
                                planet.tidal_lock = True
                        if planet.type == "Asteroid Belt":
                            planet.year = (
                                planet.semi_major_axis ** 3 / star.mass
                            ) ** 0.5

            def assign_edat(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.mass is not None:
                            x = dice_1d(10)
                            k = dice_1d(10)
                            if planet.strange:
                                k += 3
                            if x <= 5:
                                e = k * 0.005
                            elif x <= 7:
                                e = 0.05 + 0.01 * k
                            elif x <= 9:
                                e = 0.15 + 0.01 * k
                            else:
                                e = 0.25 + 0.04 * k
                            planet.eccentricity = e
                            planet.min_sep = (1 - e) * planet.semi_major_axis
                            planet.max_sep = (1 + e) * planet.semi_major_axis

            def axial(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.mass is not None:
                            x = dice_1d(10)
                            if x <= 2:
                                planet.axial = dice_1d(10)
                            elif x <= 4:
                                planet.axial = 10 + dice_1d(10)
                            elif x <= 6:
                                planet.axial = 20 + dice_1d(10)
                            elif x <= 8:
                                planet.axial = 30 + dice_1d(10)
                            else:
                                planet.axial = 40 + dice_1d(100) * 1.4

            def period(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.mass is not None:
                            x = dice_1d(10)
                            x += int(planet.T * star.age)
                            mod = planet.T
                            if planet.type == "Planetesimal":
                                if x <= 5:
                                    planet.rotation_period = dice_1d(10) * 2 / 24
                                elif x <= 7:
                                    planet.rotation_period = dice_1d(10)
                                elif x <= 9:
                                    planet.rotation_period = dice_1d(100)
                                else:
                                    planet.rotation_period = dice_1d(1000)
                            if planet.type == "Terrestrial":
                                if x <= 5:
                                    planet.rotation_period = (10 + dice_1d(10) * 2) / 24
                                elif x <= 7:
                                    planet.rotation_period = (30 + dice_1d(100)) / 24
                                elif x <= 9:
                                    planet.rotation_period = dice_1d(100) * 2
                                else:
                                    planet.rotation_period = dice_1d(1000)

                                if planet.mass > 4:
                                    mod -= planet.mass ** 0.5

                            if planet.type == "Gas Giant" or "Superjovian":
                                if x <= 5:
                                    planet.rotation_period = (dice_1d(10) / 2 + 6) / 24
                                elif x <= 7:
                                    planet.rotation_period = (dice_1d(10) / 2 + 11) / 24
                                elif x <= 9:
                                    planet.rotation_period = (dice_1d(10) + 16) / 24
                                else:
                                    planet.rotation_period = (26 + dice_1d(10)) / 24

                                if planet.mass <= 50:
                                    mod += 2
                            planet.rotation_period *= 1 + (mod * 0.1)

                            if planet.tidal_lock is True:
                                if planet.eccentricity <= 0.21:
                                    planet.rotation_period = planet.year * 365
                                elif planet.eccentricity <= 0.39:
                                    planet.rotation_period = planet.year * 365 * 2 / 3
                                elif planet.eccentricity <= 0.57:
                                    planet.rotation_period = planet.year * 365 * 1 / 2
                                elif planet.eccentricity <= 0.72:
                                    planet.rotation_period = planet.year * 365 * 2 / 5
                                elif planet.eccentricity <= 0.87:
                                    planet.rotation_period = planet.year * 365 * 1 / 3
                                else:
                                    planet.rotation_period = planet.year * 365 * 2 / 7

                            planet.solarday = 1 / (
                                (1 / planet.rotation_period) * (1 / planet.year)
                            )

            year_tidal(system)
            assign_edat(system)
            axial(system)
            period(system)

        def post_define_planet(system):
            def assign_composition_solid(system):
                for star in system.content:
                    for planet in star.planets:
                        rho = planet.density
                        if (
                            "Planetesimal" in planet.type
                            or "Terrestrial" in planet.type
                        ):
                            if planet.zone == "Inner":
                                if rho < 0.4:
                                    planet.composition = "Silicate,low density"
                                elif 0.4 <= rho <= 0.7:
                                    planet.composition = "Silicate,pb/Metal core"
                                elif rho <= 1:
                                    planet.composition = "Iron-Nickel,medium Metal core"
                                else:
                                    planet.composition = "Iron-Nickel,large Metal core"

                            else:
                                if rho < 0.15:
                                    planet.composition = "Lose Conglomerate"
                                elif 0.15 <= rho <= 0.3:
                                    planet.composition = "Ice"
                                elif rho <= 0.45:
                                    planet.composition = "Ice,Silicate Mantle"
                                elif rho <= 0.6:
                                    planet.composition = "Silicate,pb/Metal core"
                                elif rho <= 1:
                                    planet.composition = "Iron-Nickel,medium Metal core"
                                else:
                                    planet.composition = "Iron-Nickel,large Metal core"

                        for moon in planet.moon:
                            if planet.zone == "Inner":
                                rho = moon.density
                                if (
                                    "Planetesimal" in moon.type
                                    or "Terrestrial" in moon.type
                                ):
                                    if 0.4 <= rho <= 0.7:
                                        moon.composition = "Silicate,pb/metal core"
                                    elif rho <= 1:
                                        moon.composition = (
                                            "Iron-Nickel,medium Metal core"
                                        )
                                    elif rho <= 1.3:
                                        moon.composition = (
                                            "Iron-Nickel,large Metal core"
                                        )
                            else:
                                rho = moon.density
                                if (
                                    "Planetesimal" in moon.type
                                    or "Terrestrial" in moon.type
                                ):
                                    if 0 <= rho <= 0.3:
                                        moon.composition = "Ice"
                                    elif rho <= 0.45:
                                        moon.composition = "Ice,Silicate Mantle"
                                    elif rho <= 0.7:
                                        moon.composition = "Silicate,pb/metal core"
                                    elif rho <= 1:
                                        moon.composition = (
                                            "Iron-Nickel,medium Metal core"
                                        )
                                    elif rho <= 1.3:
                                        moon.composition = (
                                            "Iron-Nickel,large Metal core"
                                        )

            assign_composition_solid(system)

            def tectonic_act(system):
                import math

                for star in system.content:
                    for planet in star.planets:
                        if ("Planetesimal" in planet.type) or (
                            "Terrestrial" in planet.type
                        ):

                            base_tf = (
                                (5 + dice_1d(10)) * planet.mass ** 0.5 / planet.age
                            )

                            for other in star.planets:
                                if other.semi_major_axis == planet.semi_major_axis:
                                    base_tf *= 2

                            if planet.rotation_period < (18 / 24):
                                base_tf *= 1.25
                            elif planet.rotation_period > (100 / 24):
                                base_tf *= 0.75

                            if (
                                planet.tidal_lock
                                or planet.rotation_period > planet.year * 365
                            ):
                                base_tf *= 0.5

                            if planet.zone == "Outer" and planet.density < 0.45:
                                base_tf *= planet.density

                            f_tidal = 0
                            if len(planet.moon) > 0:
                                for moon in planet.moon:
                                    if moon.type is not "Ring":
                                        f_tidal += (
                                            moon.mass
                                            * planet.radius
                                            * 7.43
                                            * 10 ** 14
                                            / (moon.semi_axis ** 3)
                                        )
                                    else:
                                        f_tidal += 0.01

                                base_tf *= 1 + 0.25 * max(math.log(f_tidal, 10), 0)
                            ### print(base_tf)

                            p = dice_1d(10)

                            if base_tf < 0.5:
                                planet.tectonic = "Dead"

                            elif base_tf <= 1:
                                if 8 <= p <= 9:
                                    planet.tectonic = "Hot Spot"
                                elif p == 10:
                                    planet.tectonic = "Plastic"
                                else:
                                    planet.tectonic = "Dead"

                            elif base_tf <= 2:
                                if 2 <= p <= 5:
                                    planet.tectonic = "Hot Spot"
                                elif 6 <= p <= 9:
                                    planet.tectonic = "Plastic"
                                elif p == 10:
                                    planet.tectonic = "Plate Tectonic"
                                else:
                                    planet.tectonic = "Dead"
                            elif base_tf <= 3:
                                if p <= 2:
                                    planet.tectonic = "Hot Spot"
                                elif p <= 6:
                                    planet.tectonic = "Plastic"
                                else:
                                    planet.tectonic = "Plate Tectonic"
                            elif base_tf <= 5:
                                if p == 1:
                                    planet.tectonic = "Hot Spot"
                                elif p <= 3:
                                    planet.tectonic = "Plastic"
                                elif p <= 8:
                                    planet.tectonic = "Plate Tectonic"
                                else:
                                    planet.tectonic = "Platelet Tectonic"
                            else:
                                if p == 1:
                                    planet.tectonic = "Plastic"
                                elif p == 2:
                                    planet.tectonic = "Plate Tectonic"
                                elif p <= 7:
                                    planet.tectonic = "Platelet Tectonic"
                                else:
                                    planet.tectonic = "Extreme"

                            if (
                                planet.tectonic is not "Dead"
                                and "Ice" in planet.composition
                            ):
                                planet.tectonic += ",Cryovolcanism"

                        for moon in planet.moon:
                            if moon.type is not "Ring":
                                if ("Planetesimal" in moon.type) or (
                                    "Terrestrial" in moon.type
                                ):
                                    base_tf = (
                                        (5 + dice_1d(10))
                                        * moon.mass ** 0.5
                                        / planet.age
                                    )

                                    if planet.zone == "Outer" and moon.density < 0.45:
                                        base_tf *= moon.density

                                    f_tidal = (
                                        planet.mass
                                        * moon.radius
                                        * 7.43
                                        * 10 ** 14
                                        / (moon.semi_axis ** 3)
                                    )

                                    base_tf *= 1 + 0.25 * max(math.log(f_tidal, 10), 0)

                                    if moon.semi_axis <= moon.roche_limit:
                                        base_tf *= 2
                                    if "Ice" in moon.composition:
                                        base_tf *= 2

                                    p = dice_1d(10)
                                    ### print(base_tf)

                                    if base_tf < 0.5:
                                        moon.tectonic = "Dead"

                                    elif base_tf <= 1:
                                        if 8 <= p <= 9:
                                            moon.tectonic = "Hot Spot"
                                        elif p == 10:
                                            moon.tectonic = "Plastic"
                                        else:
                                            moon.tectonic = "Dead"

                                    elif base_tf <= 2:
                                        if 2 <= p <= 5:
                                            moon.tectonic = "Hot Spot"
                                        elif 6 <= p <= 9:
                                            moon.tectonic = "Plastic"
                                        elif p == 10:
                                            moon.tectonic = "Plate Tectonic"
                                        else:
                                            moon.tectonic = "Dead"
                                    elif base_tf <= 3:
                                        if p <= 2:
                                            moon.tectonic = "Hot Spot"
                                        elif p <= 6:
                                            moon.tectonic = "Plastic"
                                        else:
                                            moon.tectonic = "Plate Tectonic"
                                    elif base_tf <= 5:
                                        if p == 1:
                                            moon.tectonic = "Hot Spot"
                                        elif p <= 3:
                                            moon.tectonic = "Plastic"
                                        elif p <= 8:
                                            moon.tectonic = "Plate Tectonic"
                                        else:
                                            moon.tectonic = "Platelet Tectonic"
                                    else:
                                        if p == 1:
                                            moon.tectonic = "Plastic"
                                        elif p == 2:
                                            moon.tectonic = "Plate Tectonic"
                                        elif p <= 7:
                                            moon.tectonic = "Platelet Tectonic"
                                        else:
                                            moon.tectonic = "Extreme"

                                    if (
                                        moon.tectonic is not "Dead"
                                        and "Ice" in moon.composition
                                    ):
                                        moon.tectonic += ",Cryovolcanism"

            def mag_act(system):
                for star in system.content:
                    for planet in star.planets:
                        if (
                            ("Terrestrial" in planet.type)
                            or ("Planetesimal" in planet.type)
                        ) and ("Metal" in planet.composition):

                            if (
                                planet.tidal_lock is True
                                or planet.year * 365 > planet.rotation_period
                            ):
                                p = planet.year * 365
                            else:
                                p = planet.rotation_period

                            mag_f = (
                                10
                                * 1
                                / (p) ** 0.5
                                * planet.density ** 2
                                * planet.mass ** 0.5
                                / planet.age
                            )
                            if planet.composition and "Ice" in planet.composition:
                                mag_f *= 0.5

                            x = dice_1d(10)
                            if mag_f < 0.05:
                                planet.mag_field = 0
                            elif mag_f <= 0.5:
                                if x <= 5:
                                    planet.mag_field = 0
                                elif x <= 7:
                                    planet.mag_field = dice_1d(10) * 0.001
                                elif x <= 9:
                                    planet.mag_field = dice_1d(10) * 0.002
                                else:
                                    planet.mag_field = dice_1d(10) * 0.01

                            elif mag_f <= 1:
                                if x <= 3:
                                    planet.mag_field = 0
                                elif x <= 5:
                                    planet.mag_field = dice_1d(10) * 0.001
                                elif x <= 7:
                                    planet.mag_field = dice_1d(10) * 0.002
                                elif x <= 9:
                                    planet.mag_field = dice_1d(10) * 0.01
                                else:
                                    planet.mag_field = dice_1d(10) * 0.05

                            elif mag_f <= 2:
                                if x <= 3:
                                    planet.mag_field = dice_1d(10) * 0.001
                                elif x <= 5:
                                    planet.mag_field = dice_1d(10) * 0.002
                                elif x <= 7:
                                    planet.mag_field = dice_1d(10) * 0.01
                                elif x <= 9:
                                    planet.mag_field = dice_1d(10) * 0.05
                                else:
                                    planet.mag_field = dice_1d(10) * 0.1

                            elif mag_f <= 4:
                                if x <= 3:
                                    planet.mag_field = dice_1d(10) * 0.05
                                elif x <= 5:
                                    planet.mag_field = dice_1d(10) * 0.1
                                elif x <= 7:
                                    planet.mag_field = dice_1d(10) * 0.2
                                elif x <= 9:
                                    planet.mag_field = dice_1d(10) * 0.3
                                else:
                                    planet.mag_field = dice_1d(10) * 0.5

                            else:
                                if x <= 3:
                                    planet.mag_field = dice_1d(10) * 0.1
                                elif x <= 5:
                                    planet.mag_field = dice_1d(10) * 0.2
                                elif x <= 7:
                                    planet.mag_field = dice_1d(10) * 0.3
                                elif x <= 9:
                                    planet.mag_field = dice_1d(10) * 0.5
                                else:
                                    planet.mag_field = dice_1d(10) * 1
                            planet.mag_field *= 65

                        elif ("Superjovian" in planet.type) or (
                            "Gas Giant" in planet.type
                        ):
                            roll = dice_1d(10)
                            if planet.mass < 50:
                                if roll == 1:
                                    planet.mag_field = dice_1d(10) * 0.1
                                elif roll <= 4:
                                    planet.mag_field = dice_1d(10) * 0.25
                                elif roll <= 7:
                                    planet.mag_field = dice_1d(10) * 0.5
                                elif roll <= 9:
                                    planet.mag_field = dice_1d(10) * 0.75
                                elif roll == 10:
                                    planet.mag_field = dice_1d(10)
                            elif planet.mass <= 200:
                                if roll == 1:
                                    planet.mag_field = dice_1d(10) * 0.25
                                elif roll <= 4:
                                    planet.mag_field = dice_1d(10) * 0.5
                                elif roll <= 7:
                                    planet.mag_field = dice_1d(10) * 0.75
                                elif roll <= 9:
                                    planet.mag_field = dice_1d(10) * 1
                                elif roll == 10:
                                    planet.mag_field = dice_1d(10) * 1.5
                            elif planet.mass <= 500:
                                if roll == 1:
                                    planet.mag_field = dice_1d(10) * 0.5
                                elif roll <= 4:
                                    planet.mag_field = dice_1d(10) * 0.1
                                elif roll <= 7:
                                    planet.mag_field = dice_1d(10) * 1.5
                                elif roll <= 9:
                                    planet.mag_field = dice_1d(10) * 2
                                elif roll == 10:
                                    planet.mag_field = dice_1d(10) * 3
                            else:
                                if roll == 1:
                                    planet.mag_field = dice_1d(10) * 1.5
                                elif roll <= 4:
                                    planet.mag_field = dice_1d(10) * 2.5
                                elif roll <= 7:
                                    planet.mag_field = dice_1d(10) * 5
                                elif roll <= 9:
                                    planet.mag_field = dice_1d(10) * 10
                                elif roll == 10:
                                    planet.mag_field = dice_1d(10) * 25
                            planet.mag_field *= 65

            def calc_lz(system):
                for star in system.content:
                    star.lz_min = 0.75 * star.luminosity ** 0.5
                    star.lz_max = 1.4 * star.luminosity ** 0.5

            def asteroid_belt(system):
                for star in system.content:
                    for planet in star.planets:
                        if planet.type == "Asteroid Belt":
                            roll = dice_1d(10)
                            if planet.zone == "Outer":
                                roll += 6

                            if 0.6 <= planet.density <= 0.8:
                                roll -= 1
                            elif 0.8 < planet.density <= 1.0:
                                roll -= 2
                            elif 1.0 < planet.density <= 1.2:
                                roll -= 3
                            elif 1.2 < planet.density:
                                roll -= 5

                            if planet.semi_major_axis < star.lz_min:
                                roll -= 2

                            if roll <= -2:
                                planet.dominant_asteroid = "M"
                            elif roll <= 5:
                                planet.dominant_asteroid = "S"
                            elif roll <= 10:
                                planet.dominant_asteroid = "C"
                            else:
                                planet.dominant_asteroid = "Ice"

                        if planet.type == "Asteroid Belt":
                            roll = dice_1d(10)
                            roll += system.abundance
                            if planet.zone is "Outer":
                                roll += 2
                            else:
                                roll -= 1
                            if star.age > 7:
                                roll -= 1
                            if len(system.content) > 1:
                                roll += 2

                            if roll < 5:
                                planet.mass = 0.0001 * dice_1d(10)
                            elif roll <= 6:
                                planet.mass = 0.001 * dice_1d(10)
                            elif roll <= 8:
                                planet.mass = 0.01 * dice_1d(10)
                            elif roll <= 10:
                                planet.mass = 0.1 * dice_1d(10)
                            else:
                                planet.mass = 1 * dice_1d(10)

            def base_temp(system):
                for s in system.content:
                    for p in s.planets:
                        p.surface_temp = None
                        for m in p.moon:
                            m.surface_temp = None

                def jovian_heating(system):
                    for star in system.content:
                        for planet in star.planets:
                            if planet.type is "Superjovian":
                                age = planet.age
                                mass = planet.mass
                                if mass > 500:
                                    surface_list = [
                                        200,
                                        240,
                                        280,
                                        340,
                                        400,
                                        460,
                                        530,
                                        610,
                                    ]
                                    lumin_list = [
                                        1.6e-8,
                                        3.4e-8,
                                        6.2e-8,
                                        1.4e-7,
                                        2.6e-7,
                                        4.5e-7,
                                        8e-7,
                                        1.4e-6,
                                    ]
                                    x = mass // 500
                                    x = x - int(age)
                                    x -= 1
                                    if x > 9:
                                        x = 9
                                    elif x < 0:
                                        x = 0
                                    x = int(x)
                                    planet.luminosity = lumin_list[x]
                                    planet.surface_temp = surface_list[x]

                jovian_heating(system)
                for s in system.content:
                    s.peak_fq = 3000000 / s.surface_temperature
                star = system.content[0]
                star_list = []
                distance_list = []
                star_list.append(star)
                distance_list.append(0)

                while len(star_list) < len(system.content):
                    for orbit in system.orbits:
                        prime = orbit.body[0]
                        secondary = orbit.body[1]

                        if (prime in star_list) and (secondary not in star_list):
                            i = star_list.index(prime)
                            d = distance_list[i]
                            d += orbit.mean_sep
                            star_list.append(secondary)
                            distance_list.append(d)

                        if "-" in prime.classification:
                            e = 0
                            m = 0
                            for star in system.content:
                                if star.classification in prime.classification:
                                    n = star_list.index(star)
                                    e += distance_list[n] * star.mass
                                    m += star.mass
                            e = e / m
                            e += orbit.mean_sep
                            star_list.append(secondary)
                            distance_list.append(e)

                for s in system.content:
                    for p in s.planets:
                        if p.surface_temp is None:
                            p.surface_temp = 0
                        for m in p.moon:
                            if p.luminosity is not None:
                                m.surface_temp = (
                                    255
                                    / ((m.semi_axis / 150000000) / p.luminosity ** 0.5)
                                    ** 0.5
                                )
                            else:
                                m.surface_temp = 0
                    base = distance_list[star_list.index(s)]
                    for p in s.planets:
                        for c in star_list:
                            dis = abs(distance_list[star_list.index(c)] - base)
                            dis += p.semi_major_axis
                            lum = c.luminosity
                            mod = 255 / (dis / lum ** 0.5) ** 0.5
                            p.surface_temp += mod
                            for m in p.moon:
                                m.surface_temp += mod

            def atmosphere(system):
                def check_atms(body, star):
                    if "Terrestrial" in body.type:
                        body.ve = (body.gravity * body.radius * 19600) ** 0.5 / 11200
                        roll = dice_1d(10)
                        temp = body.surface_temp

                        if temp > 400:
                            if roll <= 4:
                                body.atmosphere = "N2,CO2"
                            elif roll <= 6:
                                body.atmosphere = "CO2"
                            elif roll <= 8:
                                body.atmosphere = "NO2,SO2"
                            else:
                                body.atmosphere = "SO2"
                        elif temp >= 240:
                            if roll <= 4:
                                body.atmosphere = "N2,CO2"
                            elif roll <= 6:
                                body.atmosphere = "CO2"
                            elif roll <= 8:
                                body.atmosphere = "N2,CH4"
                            else:
                                body.atmosphere = "CO2,CH4,NH3"
                        elif temp >= 150:
                            if roll <= 4:
                                body.atmosphere = "N2,CO2"
                            elif roll <= 6:
                                body.atmosphere = "CO2"
                            elif roll <= 8:
                                body.atmosphere = "N2,CH4"
                            else:
                                body.atmosphere = "H2,He"
                        elif temp >= 50:
                            if roll <= 4:
                                body.atmosphere = "N2,CH4"
                            elif roll <= 6:
                                body.atmosphere = "H2,He,N2"
                            elif roll <= 8:
                                body.atmosphere = "N2,CO"
                            else:
                                body.atmosphere = "He,H2"
                        elif temp < 50:
                            if roll <= 4:
                                body.atmosphere = "H2"
                            elif roll <= 6:
                                body.atmosphere = "He"
                            elif roll <= 8:
                                body.atmosphere = "He,H2"
                            else:
                                body.atmosphere = "Ne"

                        mol_ret = 0.02783 * temp / body.ve ** 2

                        if "H2" in body.atmosphere and 2 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("H2", "_H2_")
                        if "He" in body.atmosphere and 4 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("He", "_He_")
                        if "CH4" in body.atmosphere and 16 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("CH4", "_CH4_")
                        if "NH3" in body.atmosphere and 17 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("NH3", "_NH3_")
                        if "H2O" in body.atmosphere and 18 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("H2O", "_H2O_")
                        if "Ne" in body.atmosphere and 20 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("Ne", "_Ne_")
                        if "N2" in body.atmosphere and 28 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("N2", "_N2_")
                        if "CO" in body.atmosphere and 28 < mol_ret:
                            if "CO2" not in body.atmosphere:
                                body.atmosphere = body.atmosphere.replace("CO", "_CO_")
                        if "NO" in body.atmosphere and 30 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("NO", "_NO_")
                        if "CO2" in body.atmosphere and 44 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("CO2", "_CO2_")
                        if "NO2" in body.atmosphere and 46 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("NO2", "_NO2_")
                        if "SO2" in body.atmosphere and 64 < mol_ret:
                            body.atmosphere = body.atmosphere.replace("SO2", "_SO2_")

                        def UV_breakdown(body):
                            if "NH3" in body.atmosphere:
                                body.atmosphere = body.atmosphere.replace(
                                    "NH3", "_NH3_"
                                )
                            if "CH4" in body.atmosphere:
                                body.atmosphere = body.atmosphere.replace(
                                    "CH4", "_CH4_"
                                )
                            if "H2O" in body.atmosphere:
                                body.atmosphere = body.atmosphere.replace(
                                    "H2O", "_H2O_"
                                )

                        if star.spectral_class == "A" or star.spectral_class == "B":
                            if body.surface_temp > 150:
                                UV_breakdown(body)
                        elif star.spectral_class == "F":
                            if body.surface_temp > 180:
                                UV_breakdown(body)
                        elif star.spectral_class == "G":
                            if body.surface_temp > 200:
                                UV_breakdown(body)
                        elif star.spectral_class == "K":
                            if body.surface_temp > 230:
                                UV_breakdown(body)
                        elif star.spectral_class == "M":
                            if body.surface_temp > 260:
                                UV_breakdown(body)

                        roll = dice_1d(10)

                        new_list = body.atmosphere.split(",")

                        if body.tectonic is "Dead":
                            roll -= 1
                        elif "Extreme" in body.tectonic:
                            roll += 1
                        if any("_" in gas for gas in new_list):
                            roll -= 1

                        if temp > 500:
                            roll -= 1
                        if temp > 1000:
                            roll -= 1
                        if temp > 1500:
                            roll -= 1
                        if all("_" in gas for gas in new_list) is True:
                            body.pressure = 0
                        else:
                            if roll <= 2:
                                body.pressure = dice_1d(10) * 0.01
                            elif roll <= 4:
                                body.pressure = dice_1d(10) * 0.1
                            elif roll <= 7:
                                body.pressure = dice_1d(10) * 0.2
                            elif roll <= 8:
                                body.pressure = dice_1d(10) * 0.5
                            elif roll <= 9:
                                body.pressure = dice_1d(10) * 2
                            else:
                                body.pressure = dice_1d(10) * 20

                        body.pressure *= 101.325

                        roll = dice_1d(10)
                        if all("_" in gas for gas in new_list):
                            body.atm_comp = 0
                        else:
                            if roll <= 5:
                                body.atm_comp = (
                                    0.5
                                    + (
                                        dice_1d(10)
                                        + dice_1d(10)
                                        + dice_1d(10)
                                        + dice_1d(10)
                                    )
                                    * 0.01
                                )
                            elif roll <= 8:
                                body.atm_comp = (
                                    0.75 + (dice_1d(10) + dice_1d(10)) * 0.01
                                )
                            else:
                                body.atm_comp = 0.95 + dice_1d(10) / 2 * 0.01

                        for gas in new_list:
                            mod = True
                            for other in new_list:
                                if other == gas or "_" in other:
                                    pass
                                else:
                                    mod = False
                            if mod:
                                body.atm_comp = 0.95 + dice_1d(10) / 2 * 0.01

                        primary_gas = new_list[0]
                        if "_" not in primary_gas:
                            gas_dict = {
                                "H2": 2,
                                "He": 4,
                                "CH4": 16,
                                "NH3": 17,
                                "H2O": 18,
                                "Ne": 20,
                                "N2": 28,
                                "CO": 28,
                                "NO": 30,
                                "O2": 32,
                                "H2S": 34,
                                "Ar": 40,
                                "CO2": 44,
                                "NO2": 46,
                                "SO2": 64,
                            }
                            primary_gas_mol_contribution = (
                                gas_dict[primary_gas] * body.atm_comp
                            )
                            remining_minor_component = 0
                            secondary_gas_mol_contribution = 0
                            for gas in new_list:
                                if "_" not in gas and gas != primary_gas:
                                    remining_minor_component += 1
                            for gas in new_list:
                                if "_" not in gas and gas != primary_gas:
                                    secondary_gas_mol_contribution += (
                                        gas_dict[gas]
                                        * (1 - body.atm_comp)
                                        / remining_minor_component
                                    )

                            body.atm_average_mol = (
                                primary_gas_mol_contribution
                                + secondary_gas_mol_contribution
                            )
                            body.scale_height = (
                                8.314
                                * body.surface_temp
                                / (body.atm_average_mol / 1000)
                                / (body.gravity * 9.8)
                            )

                for star in system.content:
                    for planet in star.planets:
                        check_atms(planet, star)
                        for moon in planet.moon:
                            check_atms(moon, star)

            def hydrosphere(system):
                def chk_hyd(body, planet):
                    if "Terrestrial" in body.type:
                        temp = body.surface_temp
                        if "NH3" in body.atmosphere:
                            mod = -90
                        else:
                            mod = 0
                        if body.pressure <= 0.006 * 101.32:
                            low_pres = True
                        else:
                            low_pres = False

                        proceed = False
                        if temp < 245 + mod:
                            body.hydro = "Ice Sheets"
                            proceed = True
                        elif temp <= 370 + mod and not low_pres:
                            body.hydro = "Liquid"
                            proceed = True
                        elif temp <= 500 + mod and not low_pres:
                            body.hydro = "Vapor"
                            body.atmosphere += ",_H2O_"
                        else:
                            body.hydro = None

                        if proceed:
                            roll = dice_1d(10)
                            radius = body.radius
                            if radius < 2000:
                                if roll <= 5:
                                    body.hyd_exten = 0
                                elif roll <= 7:
                                    body.hyd_exten = dice_1d(10) * 0.01
                                elif roll == 8:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.1
                                elif roll <= 9:
                                    body.hyd_exten = (
                                        dice_1d(10)
                                        + dice_1d(10)
                                        + dice_1d(10)
                                        + dice_1d(10)
                                        + dice_1d(10)
                                    ) * 0.01
                                else:
                                    body.hyd_exten = 0.1
                                    for i in range(0, 10):
                                        body.hyd_exten += dice_1d(10) * 0.01

                            elif radius <= 4000:
                                if roll <= 2:
                                    body.hyd_exten = 0
                                elif roll <= 4:
                                    body.hyd_exten = dice_1d(10) * 0.01
                                elif roll == 5:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.1
                                elif roll == 6:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.2
                                elif roll == 7:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.3
                                elif roll == 7:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.3
                                elif roll == 8:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.4
                                elif roll == 9:
                                    body.hyd_exten = dice_1d(10) * 0.01 + 0.5
                                else:
                                    body.hyd_exten = 0.1
                                    for i in range(0, 10):
                                        body.hyd_exten += dice_1d(10) * 0.01

                            elif radius <= 7000:
                                if roll <= 1:
                                    body.hyd_exten = 0
                                elif roll <= 2:
                                    body.hyd_exten = (dice_1d(10) + dice_1d(10)) * 0.01
                                elif roll <= 8:
                                    body.hyd_exten = (roll - 1) * 0.1 + dice_1d(
                                        10
                                    ) * 0.01
                                elif roll == 9:
                                    body.hyd_exten = (
                                        dice_1d(10) + dice_1d(10)
                                    ) * 0.01 + 0.8
                                else:
                                    body.hyd_exten = 1

                            else:
                                if roll <= 1:
                                    body.hyd_exten = 0
                                elif roll <= 2:
                                    body.hyd_exten = (dice_1d(10) + dice_1d(10)) * 0.01
                                elif roll <= 4:
                                    body.hyd_exten = (roll - 2) * 0.2 + (
                                        dice_1d(10) + dice_1d(10)
                                    ) * 0.01
                                elif roll <= 8:
                                    body.hyd_exten = (roll + 1) * 0.1 + dice_1d(
                                        10
                                    ) * 0.01
                                else:
                                    body.hyd_exten = 1

                            if body.hyd_exten is None:
                                body.hydro = None
                                body.wvf = 0

                            if body.hyd_exten is not None:
                                body.wvf = (
                                    (temp - 240) / 100 * body.hyd_exten * dice_1d(10)
                                )
                                if body.wvf < 0:
                                    body.wvf = 0

                        else:
                            body.hyd_exten = 0
                            body.wvf = 0

                for star in system.content:
                    for planet in star.planets:
                        chk_hyd(planet, planet)
                        for m in planet.moon:
                            chk_hyd(m, planet)

            def albedo(system):
                def chk_abd(body, planet):
                    def roll_inner(body, roll):
                        if body.atmosphere is None or all(
                            "_" in gas for gas in body.atmosphere
                        ):
                            roll += 2
                        if body.pressure >= 5 * 101.3:
                            roll -= 2
                        if body.pressure >= 50 * 101.3:
                            roll -= 4
                        if body.hydro == "Ice Sheets" and body.hyd_exten >= 0.9:
                            roll -= 4
                        elif body.hydro == "Ice Sheets" and body.hyd_exten >= 0.5:
                            roll -= 2
                        return roll

                    if "Terrestrial" in body.type:
                        roll = dice_1d(10)
                        if planet.zone == "Inner":
                            roll = roll_inner(body, roll)
                        else:
                            if body.pressure >= 101.3:
                                roll += 1

                        if planet.zone == "Inner" or body in planet.moon:
                            if roll <= 1:
                                body.albedo = 0.75 + dice_1d(10) * 0.01
                            elif roll <= 3:
                                body.albedo = 0.85 + dice_1d(10) * 0.01
                            elif roll <= 6:
                                body.albedo = 0.95 + dice_1d(10) * 0.01
                            elif roll <= 9:
                                body.albedo = 1.05 + dice_1d(10) * 0.01
                            else:
                                body.albedo = 1.15 + dice_1d(10) * 0.01

                        else:
                            if 1 <= roll <= 3:
                                body.albedo = 0.75 + dice_1d(10) * 0.01
                            elif 4 <= roll <= 5:
                                body.albedo = 0.85 + dice_1d(10) * 0.01
                            elif 6 <= roll <= 7:
                                body.albedo = 0.95 + dice_1d(10) * 0.01
                            elif 8 <= roll <= 9:
                                body.albedo = 1.05 + dice_1d(10) * 0.01
                            elif roll >= 10:
                                body.albedo = 1.15 + dice_1d(10) * 0.01

                def apl_grh(body):
                    if body.atmosphere is not None and "Terrestrial" in body.type:
                        listed = body.atmosphere.split(",")
                        major = []
                        part_p = []
                        for gas in listed:
                            if "_" not in gas:
                                major.append(gas)

                        for gas in major:
                            if major.index(gas) == 0:
                                part_p.append(body.pressure * body.atm_comp / 101.3)
                        if len(major) == 2:
                            part_p.append(body.pressure * (1 - body.atm_comp) / 101.3)
                        else:
                            x = dice_1d(10)

                            part_p.append(
                                body.pressure * (1 - body.atm_comp) * (x / 10) / 101.3
                            )
                            part_p.append(
                                body.pressure
                                * (1 - body.atm_comp)
                                * ((10 - x) / 10)
                                / 101.3
                            )

                        pgr = 0
                        if "CO2" in major:
                            pgr += part_p[major.index("CO2")]
                        if "CH4" in major:
                            pgr += part_p[major.index("CH4")]
                        if "SO2" in major:
                            pgr += part_p[major.index("SO2")]
                        if "NO2" in major:
                            pgr += part_p[major.index("NO2")]
                        gf = (
                            1
                            + body.pressure ** 0.5 * 0.01 * dice_1d(10)
                            + pgr ** 0.5 * 0.1
                            + body.wvf * 0.1
                        )
                        body.surface_temp *= gf * body.albedo

                for star in system.content:
                    for planet in star.planets:
                        chk_abd(planet, planet)
                        apl_grh(planet)
                        if planet.type == "Terrestrial":
                            if planet.surface_temp > 2000:
                                return True
                        if planet.hydro == "Ice Sheets" and planet.surface_temp > 245:
                            return True
                        if planet.hydro == "Liquid" and planet.surface_temp > 370:
                            return True
                        if planet.hydro == "Vapor" and planet.surface_temp > 500:
                            return True
                        for moon in planet.moon:
                            chk_abd(moon, planet)
                            apl_grh(moon)
                            if moon.hydro == "Ice Sheets" and moon.surface_temp > 245:
                                return True
                            if moon.hydro == "Liquid" and moon.surface_temp > 370:
                                return True
                            if moon.hydro == "Vapor" and moon.surface_temp > 500:
                                return True
                            if moon.surface_temp > 2000 and moon.type == "Terrestrial":
                                return True
                return False

            tectonic_act(system)
            mag_act(system)
            calc_lz(system)
            asteroid_belt(system)
            base_temp(system)
            """"Geology"""
            reroll = True
            atp = 0
            while reroll is True:
                if reroll is True and atp != 0:
                    base_temp(system)
                atmosphere(system)
                hydrosphere(system)
                reroll = albedo(system)
                atp += 1

        add_planet(system)
        define_planet_type(system)
        orbit_planet(system)
        moon_around_planet(system)
        post_define_planet(system)
        assign_name(system)

    def determine_pos(density, store, system, start):
        volume = system.number / density
        length = volume ** (1 / 3)

        def check_pas(store, system):
            x, y, z = system.pos
            for other in store:
                x_ = other.pos[0]
                y_ = other.pos[1]
                z_ = other.pos[2]

                if (
                    (x_ - 1 < x < x_ + 1)
                    and (y_ - 1 < y < y_ + 1)
                    and (z_ - 1 < z < z_ + 1)
                ):
                    return True
            return False

        proceed = True
        import random
        while proceed:
            x = round(-length / 2 + random.uniform(0, length), 4)
            y = round(-length / 2 + random.uniform(0, length), 4)
            z = round(-length / 2 + random.uniform(0, length), 4)
            system.pos = x, y, z
            proceed = check_pas(store, system)

    def name_star(system, num):
        for star in system.content:
            star.name = str(num) + str(star.classification)

    constellation = []
    for i in range(start, start + number):
        seed_random(i)
        new_system = system_generation(stellar_generation())
        new_system.number = i - start
        determine_pos(density, constellation, new_system, start)
        for star in new_system.content:
            luminosity_mass(star)
        age(new_system)
        assign_orbit(new_system)
        planet_wrapper(new_system)
        name_star(new_system, i)
        constellation.append(new_system)

    return constellation


def filter(system, option="C"):

    if option == "C":
        system.flag = False
        for star in system.content:
            body_to_check = []
            for planet in star.planets:
                if planet.type == "Terrestrial" or planet.type == "Planetesimal":
                    body_to_check.append(planet)
                for moon in planet.moon:
                    if "Planetesimal" in moon.type or "Terrestrial" in moon.type:
                        body_to_check.append(moon)

            for candidate in body_to_check:
                if 258 <= candidate.surface_temp <= 395.15:
                    temp_flag = True
                else:
                    temp_flag = False

                if candidate.pressure is not None and candidate.pressure <= 1.1e8:
                    pres_flag = True
                else:
                    pres_flag = False

                if candidate.hyd_exten is not None and candidate.hyd_exten > 0:
                    water_flag = True
                else:
                    water_flag = False

                if all([temp_flag, water_flag, pres_flag]):
                    system.flag = True
    else:
        system.flag = True


def print_wrapper(constellation, number, start, gist, filter_option, write_to_file):
    if write_to_file:
        import sys

        original_out = sys.stdout
        f = open(str(write_to_file + ".txt"), "w", encoding="utf-8")
        sys.stdout = f

    def fine_print(system, gist=False):
        if system.type:
            print("     {:^50}".format(system.type))

        print()
        for o in system.orbits:
            print(
                "     {:<10} {:<10}".format(
                    o.body[0].classification, o.body[1].classification
                )
            )
            print(
                "         mean sep:{:^6} ecc:{:^6} max sep:{:^6} min sep:{:^6} period:{:^10}".format(
                    round(o.mean_sep, 3),
                    round(o.eccentricity, 3),
                    round(o.max_sep, 3),
                    round(o.min_sep, 3),
                    round(o.period, 2),
                )
            )
        print()
        for s in system.content:

            postfix = ""

            if s.size_code == 3:
                postfix = "III"
            elif s.size_code == 4:
                postfix = "IV"
            elif s.size_code == 5:
                postfix = "V"
            elif s.size_code == 7:
                postfix = "VII"

            print(
                "     {}{}{}".format(
                    s.spectral_class, s.spectral_specification, postfix
                )
            )
            print(
                "      age:{:>5.1f}Gy radius:{:>5}R_sol mass:{:>5}M_sol lum:{:>5.4}Lum_sol @{:}nm".format(
                    round(s.age, 2),
                    round(s.radius, 2),
                    round(s.mass, 2),
                    round(float(s.luminosity), 4),
                    round(s.peak_fq, 1),
                )
            )
        print()
        for s in system.content:
            if len(s.planets) >= 1:
                print()
                print(
                    "     {:_^5}{:_^12.11}{:_^15}{:_^9}{:_^8}{:_^8.6}{:_^8.6}{:_^8.6}{:_^10.6}{:_^8}{:_^8}".format(
                        s.classification,
                        "S_M_axis/AU",
                        "Type",
                        "Radius/km",
                        "e",
                        "Mass/Me",
                        "Grav/g",
                        "Day/d",
                        "Year/y",
                        "Tilt/deg",
                        "Temp/K",
                    )
                )
            for p in s.planets:
                print()  # asthetics
                if len(p.moon) > 0:
                    pre = "\u25ca"
                else:
                    pre = " "
                print(
                    "  {}|_{:-^5}{:^12.1E}{:-^15}{:^9.8}{:-^8.5}{:^8.5}{:-^8.5}{:^8.5}{:-^10.3}{:^8.5}{:-^8}".format(
                        pre,
                        p.designation,
                        p.semi_major_axis,
                        str(p.type),
                        str(p.radius),
                        str(p.eccentricity),
                        str(p.mass),
                        str(p.gravity),
                        str(p.solarday),
                        p.year,
                        str(p.axial),
                        round(p.surface_temp, 1),
                    )
                )

                if gist is True:
                    continue

                feature = ""
                if p.tidal_lock:
                    feature += "[ ] Tidally locked to star//"
                if p.strange:
                    feature += "[ ] Inclined orbit//"
                if p.composition is not None:
                    feature += "[ ] " + p.composition + "//"
                if p.luminosity is not None:
                    feature += (
                        "[+] Radiating:"
                        + str(round(p.luminosity, 2))
                        + " LumSol "
                        + str(round(p.surface_temp, 2))
                        + "K//"
                    )
                if p.tectonic is not None:
                    if p.tectonic != "Dead":
                        feature += "[*] " + p.tectonic + "//"
                if p.mag_field is not None and p.mag_field != 0:
                    feature += (
                        "[.] Magnetic field:" + str(round(p.mag_field, 2)) + "uT//"
                    )
                if p.dominant_asteroid is not None:
                    feature += "[_] " + str(p.dominant_asteroid) + " dominant//"
                if p.double_radius is not None:
                    feature += "[!] Orbiting:" + str(p.double_radius) + " km mean sep//"
                if len(p.moon) > 0:
                    feature += "[/] Moons//"
                if p.atmosphere is not None:
                    if p.pressure != 0:
                        listed = p.atmosphere.split(",")
                        for gas in listed:
                            if "_" not in gas:
                                i = listed.index(gas)
                                break
                        feature += (
                            "[)] Atmosphere "
                            + str(p.atmosphere)
                            + " @ "
                            + str(round(p.pressure, 3))
                            + " kPa"
                            + str(" ({:} {:.0%}".format(listed[i], p.atm_comp))
                            + str(" scale:{:.1f} km".format(p.scale_height / 1000))
                            + ")//"
                        )
                    else:
                        feature += "[)] Trace Gas " + str(p.atmosphere) + "//"
                if p.hydro is not None:
                    if p.hyd_exten != 0:
                        feature += (
                            "[#] Hydrosphere:"
                            + str(" {:^10} {:.0%}".format(p.hydro, p.hyd_exten))
                            + "//"
                        )

                feature_list = feature.split("//")

                # feature output formatting
                e = 0
                for thing in feature_list:
                    if thing != "":
                        if e != 0:
                            print("{}{}".format(str(" " * 20), str(thing)))
                        else:
                            e += 1
                            print(
                                "{}{}{:`<85.40}".format(
                                    str(" " * 5), str("`" * 15), str(thing)
                                )
                            )

        print()
        for s in system.content:
            for p in s.planets:
                lead = s.classification + "-" + p.designation
                if len(p.moon) > 0:
                    print()
                    print(
                        "         {:^8}{:^15}  {:^8}{:^8} {:^8} {:^6} {:^8}".format(
                            lead,
                            "Type",
                            "SMA/Rp",
                            "Mass/Me",
                            "Radius/km",
                            "Grav/g",
                            "Temp/K",
                        )
                    )
                counter = 0
                for m in p.moon:
                    if (
                        gist is True
                        and "Planetesimal" in m.type
                        and p.type != "Terrestrial"
                    ):
                        counter += 1
                        continue

                    # print decorator
                    pre = " "
                    if m.mass > 10e-4:
                        pre = "\u25CF"
                    elif m.mass > 10e-5:
                        pre = "\u25CB"
                    if m.type == "Ring":
                        pre = "\u25CC"
                    print(
                        "           {}|__{:2}{:^15.15}  {:^8} {:^8.2e} {:^8.5} {:^6.6} {:^8.2f}".format(
                            pre,
                            m.name,
                            m.type,
                            m.semi_axis / p.radius,
                            m.mass,
                            str(m.radius),
                            str(m.gravity),
                            m.surface_temp,
                        )
                    )
                    if gist is True:
                        continue
                    appendix = ""
                    if m.composition is not None:
                        appendix += " [-] " + m.composition + "//"
                    if m.strange:
                        appendix += " [-] Retrograde/Inclined//"
                    if m.tectonic is not None and m.tectonic != "Dead":
                        appendix += " [-*-] " + m.tectonic + "//"
                    if m.atmosphere is not None:
                        if m.pressure != 0:
                            listed = m.atmosphere.split(",")
                            for gas in listed:
                                if "_" not in gas:
                                    i = listed.index(gas)
                                    break
                            appendix += (
                                " [c] Atmosphere "
                                + str(m.atmosphere)
                                + " @ "
                                + str(round(m.pressure, 3))
                                + " kPa"
                                + str(" ({:} {:.0%}".format(listed[i], m.atm_comp))
                                + str(" scale:{:.1f} km".format(m.scale_height / 1000))
                                + ")//"
                            )
                        else:
                            appendix += " [c] Trace Gas " + str(m.atmosphere) + "//"
                    if m.hydro is not None:
                        if m.hyd_exten != 0:
                            appendix += (
                                " [^] Hydrosphere:"
                                + str(" {:^10} {:.0%}".format(m.hydro, m.hyd_exten))
                                + "//"
                            )

                    appendix_list = appendix.split("//")
                    e = 0
                    for thing in appendix_list:
                        if thing is not "":
                            if e == 0:
                                print(
                                    "{}{}{:`<55.50}".format(
                                        str(" " * 15), str("`" * 6), str(thing)
                                    )
                                )
                                e += 1
                            else:
                                print("{}{}".format(str(" " * 21), str(thing)))
                if counter != 0:
                    print("               {:} Planetesimals".format(counter))
        print("-" * 150)

    for i in range(0, number):
        my_sys = constellation[i]
        x, y, z = my_sys.pos
        for e in range(0, number):
            thy_sys = constellation[e]
            x1, y1, z1 = thy_sys.pos
            thy_sys.dis = ((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2) ** 0.5
        neighbor = constellation
        neighbor = sorted(neighbor, key=lambda x: x.dis)
        my_sys.neighbor = neighbor
    for i in range(0, number):
        system = constellation[i]
        filter(system, filter_option)
        if system.flag is False:
            continue
        print("seed " + str(i + start))

        x, y, z = system.pos

        print("    Cord:x.{:^8.4}y.{:^8.4}z.{:^8.4}".format(x, y, z))
        for e in range(1, min(len(constellation), 5)):
            oth_sys = system.neighbor[e]
            x1, y1, z1 = oth_sys.pos
            dis = ((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2) ** 0.5
            x_disp = x1 - x
            y_disp = y1 - y
            z_disp = z1 - z
            print(
                "     {:3}-dis:{:>5.1f}ly x.{:>5.2f} y.{:>5.2f} z.{:>5.2f}".format(
                    oth_sys.number, dis, x_disp, y_disp, z_disp
                )
            )
        fine_print(system, gist)
        for e in range(0, 3):
            print()
    if write_to_file:
        sys.stdout = original_out
        f.close()


def handle_input():
    import time

    while True:
        try:
            user_input = input("{:<25}".format("Seed?(integer)"))
            if not user_input:
                start = int(time.time())
                break
            else:
                start = int(user_input)
                break
        except ValueError:
            print("(integer,leave blank for default:time)")

    while True:
        try:
            user_input = input("{:<25}".format("Amount?(integer)"))
            if not user_input:
                number = 1
                break
            elif int(user_input) > 0:
                number = int(user_input)
                break
        except ValueError:
            print("(integer,leave blank for default:1)")
    while True:
        try:
            user_input = input("{:<25}".format("density?(ly^-3)"))
            if not user_input:
                density = 0.004
                break
            elif float(user_input) > 0:
                density = float(user_input)
                break
        except ValueError:
            print("(float,leave blank for default:0.004)")
    while True:
        try:
            user_input = input("{:<25}".format("verbose?(n/y)"))
            if not user_input:
                # not verbose, default value
                gist = True
                break
            elif str(user_input) == "y":
                gist = False
                break
            elif str(user_input) == "n":
                gist = True
                break
        except ValueError:
            print("(y/n,leave blank for default:n)")

    while True:
        try:
            user_input = input("{:<25}".format("filter?(n/C)"))
            if not user_input:
                # not verbose, default value
                filter_option = "n"
                break
            elif str(user_input) == "C":
                filter_option = "C"
                break
            elif str(user_input) == "n":
                filter_option = "n"
                break
            else:
                raise ValueError
        except ValueError:
            print("(n:None,default.)")
            print(
                "(C:Requirement&Limits for life in the context of Exoplanet,C.P.McKay,2014 Jun 9)"
            )
    while True:
        user_input = input("{:<25}".format("output?(-h)"))
        if not user_input:
            write_to_file = False
            break
        elif str(user_input) == "-h":
            print("(terminal:result will print to terminal.)")
            print("(file:result will be saved to a text file named after your input)")
        else:
            write_to_file = str(user_input)
            break
    return density, number, start, gist, filter_option, write_to_file


def generate():
    density, number, start, gist, filter_option, write_to_file = handle_input()
    constellation = constellation_wrapper(density, number, start)
    print("\nFinished!\n")
    print_wrapper(constellation, number, start, gist, filter_option, write_to_file)
    return constellation


if __name__ == "__main__":
    while True:
        generate()
