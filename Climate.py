landAlb = 0.3
waterAlb = 0.06
iceAlb = 0.6

landEmit = 0.95
waterEmit = 0.95
iceEmit = 0.98

solInfall = 1370
sigma = 5.67e-8
F = 33  # W/mK


def secant_method(f, x0, x1, max_iter=1000, tolerance=1e-2):
    steps_taken = 1
    while steps_taken < max_iter and abs(x1 - x0) > tolerance:
        x2 = x1 - ((f(x1) * (x1 - x0)) / (f(x1) - f(x0)))
        x1, x0 = x2, x1
        steps_taken += 1
    assert steps_taken != max_iter
    return x2, steps_taken


def equivalentAlbedo(land_fract, tempreature):
    if tempreature > 263.15:
        albedo = landAlb * land_fract + (1 - land_fract) * waterAlb
    else:
        albedo = landAlb * land_fract + (1 - land_fract) * iceAlb
    return albedo


def equivalentEmittance(land_fract, tempreature):
    if tempreature > 263.15:
        emittance = landEmit * land_fract + (1 - land_fract) * waterEmit
    else:
        emittance = landEmit * land_fract + (1 - land_fract) * iceEmit
    return emittance


def solve_lat(
    latitude_deg,
    equiv_infall,
    land_fract,
    averageTemp,
    solar_declination,
    last_round,
    greenhouse_factor,
    mode,
):

    import math

    declination = solar_declination * math.pi / 180
    latitude = latitude_deg * math.pi / 180
    x = -1 * math.tan(latitude) * math.tan(declination)
    if x >= 1:
        hourAng = 0
    elif x <= -1:
        hourAng = math.pi
    else:
        hourAng = math.acos(x)
    day_portion = hourAng / math.pi
    sunset = hourAng * 180 / math.pi
    sunrise = -hourAng * 180 / math.pi
    counter = 0
    local_modifier = (
        0  # Calculates local_modifier --> accounts for average solar elevation
    )
    for local_hourDeg in range(round(sunrise), round(sunset)):
        local_hourAng = local_hourDeg * math.pi / 180
        z = math.sin(latitude) * math.sin(declination) + math.cos(latitude) * math.cos(
            declination
        ) * math.cos(local_hourAng)
        local_elev = max(math.asin(z), 0)

        local_modifier += abs(math.sin(local_elev))
        counter += 1
    if counter == 0:
        local_modifier = 0
    else:
        local_modifier /= counter
    curInfall = solInfall * equiv_infall * local_modifier

    def function(tempreature):
        if len(last_round[1]) > 0:
            curr_position = last_round[0].index(latitude_deg)
            if curr_position > 0:
                T_lowlat = last_round[1][curr_position - 1]
            else:
                T_lowlat = tempreature
            if curr_position < len(last_round[0]) - 1:
                T_highlat = last_round[1][curr_position + 1]
            else:
                T_highlat = tempreature
            circulation = F * (tempreature - T_highlat) + F * (tempreature - T_lowlat)
        else:
            circulation = 0

        effAlb = equivalentAlbedo(land_fract, tempreature)
        effEmm = equivalentEmittance(land_fract, tempreature)
        if mode == "Average":
            balance = (
                effEmm * sigma * tempreature ** 4 / greenhouse_factor
                + circulation
                - (1 - effAlb) * curInfall * day_portion
            )
        elif mode == "Day":
            balance = (
                effEmm * sigma * tempreature ** 4 / greenhouse_factor
                + circulation
                - (1 - effAlb) * curInfall
            )
        elif mode == "Night":
            balance = (
                effEmm * sigma * tempreature ** 4 / greenhouse_factor + circulation
            )
        else:
            raise ValueError
        return balance

    tempreature, steps_taken = secant_method(function, 400, 500)
    return tempreature, day_portion


def solve_globe(
    equiv_infall,
    land_fract,
    axial_tilt,
    latitude_deg_interval=90,
    time_res=4,
    greenhouse_factor=1,
    mode="Day",
    allowed_error=1,
    iter_limit=1000,
):

    time_label = []
    delta_latitude_deg = 90 / latitude_deg_interval
    delta_t_deg = 360 / time_res
    import math

    t_deg = 0
    ratio_lookup = []
    latitude_deg_lookup = []
    latitude_deg = 0
    while latitude_deg <= 90:
        if latitude_deg + delta_latitude_deg <= 90:
            ang_0 = latitude_deg * math.pi / 180
            ang_1 = (latitude_deg + delta_latitude_deg) * math.pi / 180
            ratio = math.sin(ang_1) - math.sin(ang_0)
            ratio_lookup.append(ratio)
        ratio_lookup.append(
            0
        )  # accounts for the fact that polar tempreature is effectively a point.
        latitude_deg_lookup.append(latitude_deg)
        latitude_deg += delta_latitude_deg

    globe = []
    globe_illumi = []

    while t_deg <= 360:
        solar_declination = axial_tilt * math.sin(t_deg / 360 * 2 * math.pi)
        initial_average = 270
        iterations = 0
        tempreature_lookup = []
        while iterations < iter_limit:
            latitude_deg = 0
            last_round = [latitude_deg_lookup, tempreature_lookup]
            tempreature_lookup = []
            illumination_lookup = []
            while latitude_deg <= 90:

                local_temp, local_day_portion = solve_lat(
                    latitude_deg,
                    equiv_infall,
                    land_fract,
                    initial_average,
                    solar_declination,
                    last_round,
                    greenhouse_factor,
                    mode,
                )
                illumination_lookup.append(local_day_portion)
                tempreature_lookup.append(local_temp)

                latitude_deg += delta_latitude_deg

            new_average = 0
            for latitude in latitude_deg_lookup:
                curr_position = latitude_deg_lookup.index(latitude)
                new_average += (
                    tempreature_lookup[curr_position] * ratio_lookup[curr_position]
                )

            iterations += 1

            if abs(new_average - initial_average) > allowed_error:
                initial_average = new_average
            else:
                break
        globe.append(tempreature_lookup)
        globe_illumi.append(illumination_lookup)
        time_label.append(t_deg)
        t_deg += delta_t_deg
    return globe, globe_illumi, time_label, latitude_deg_lookup


def dataPlot(data, y_label, x_label, modifier, header):
    #
    # data structure:
    # data[[x00,x01],[x10,x11],[x20,x21]......],etc
    #
    print(" " + str(header))

    print("      ", end="")
    for i in x_label:
        print("{:^6.0f}".format(i), end="")
    print()
    e = 0
    for slice_x in data:
        print("{:^6.0f}".format(y_label[e]), end="")
        for x in slice_x:
            print("{:^6.1f}".format(x + modifier), end="")
        print()
        e += 1


def handle_input():
    land_fract = float(input("Land Fraction -->"))
    equiv_infall = float(input("Equivalent Solar Infall -->"))
    resolution = int(input("Latitude Segments Solved-->"))
    time_res = int(input("Time Segments Solved -->"))
    axial_tilt = float(input("Axial Tilt -->"))
    greenhouse_factor = float(input("Greenhouse Factor-->"))
    global F
    F = float(input("Diffusion Factor -->"))
    return land_fract, equiv_infall, resolution, time_res, axial_tilt, greenhouse_factor


def main():
    (
        land_fract,
        equiv_infall,
        resolution,
        time_res,
        axial_tilt,
        greenhouse_factor,
    ) = handle_input()
    globe_day, globe_illumi, time_label, latitude_deg_lookup = solve_globe(
        equiv_infall,
        land_fract,
        axial_tilt,
        resolution,
        time_res,
        greenhouse_factor,
        "Day",
    )
    globe_night, globe_illumi, time_label, latitude_deg_lookup = solve_globe(
        equiv_infall,
        land_fract,
        axial_tilt,
        resolution,
        time_res,
        greenhouse_factor,
        "Average",
    )
    dataPlot(globe_day, time_label, latitude_deg_lookup, 0, "Daytime,K")
    dataPlot(globe_day, time_label, latitude_deg_lookup, -273.15, "Daytime,C")
    dataPlot(globe_night, time_label, latitude_deg_lookup, 0, "Average,K")
    dataPlot(globe_night, time_label, latitude_deg_lookup, -273.15, "Average,C")
    dataPlot(globe_illumi, time_label, latitude_deg_lookup, 0, "Day Length")


def modelClimate(
    land_fract,
    equiv_infall,
    resolution,
    time_res,
    axial_tilt,
    diffusion_factor,
    greenhouse_factor,
):
    global F
    F = diffusion_factor
    globe_day, globe_illumi, time_label, latitude_deg_lookup = solve_globe(
        equiv_infall,
        land_fract,
        axial_tilt,
        resolution,
        time_res,
        greenhouse_factor,
        "Day",
    )
    globe_night, globe_illumi, time_label, latitude_deg_lookup = solve_globe(
        equiv_infall,
        land_fract,
        axial_tilt,
        resolution,
        time_res,
        greenhouse_factor,
        "Average",
    )
    dataPlot(globe_day, time_label, latitude_deg_lookup, 0, "Daytime,K")
    dataPlot(globe_night, time_label, latitude_deg_lookup, 0, "Average,K")
    globe_illumi_percentage = []
    for slice_x in globe_illumi:
        illumi_percentage = []
        for datapoint in slice_x:
            illumi_percentage.append(datapoint * 100)
        globe_illumi_percentage.append(illumi_percentage)

    dataPlot(globe_illumi_percentage, time_label, latitude_deg_lookup, 0, "Day Length")


if __name__ == "__main__":
    main()
