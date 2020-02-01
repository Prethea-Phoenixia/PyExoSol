from Generation import generate
from Visualize import Celestial, datastream

subject = generate()
for system in subject:
    for star in system.content:
        print(star.name)
        cestar = Celestial()
        cestar.name = star.name
        cestar.mass = 1048 * star.mass  # convert Msol into Mj
        vis_list = [cestar]

        def random_radian():
            import random, math
            return random.randrange(0, int(2 * math.pi * 1000)) / 1000

        for planet in star.planets:
            print(planet.designation)
            if planet.type != "Asteroid Belt":
                ceplanet = Celestial()
                ceplanet.cordFromEphem(
                    planet.designation,
                    cestar.mass,
                    planet.mass,
                    planet.semi_major_axis,
                    planet.eccentricity,
                    0,
                    random_radian(),
                    random_radian(),
                    random_radian(),
                )
                vis_list.append(ceplanet)

        datastream(vis_list,0.1,10)
