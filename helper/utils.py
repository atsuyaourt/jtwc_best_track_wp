def knots_to_cat(wind_speed):
    """Converts wind speed in knots to equivalent tropical cyclone category
    based on Saffir-Simpson scale

    Input:
    wind_speed (int) -- wind speed in knots

    Output:
    cat (str) -- TC category
    """
    cat = ''
    if wind_speed < 20:
        cat = ''
    elif wind_speed <= 34:
        cat = 'TD'
    elif wind_speed <= 63:
        cat = 'TS'
    elif wind_speed <= 82:
        cat = 'Cat1'
    elif wind_speed <= 95:
        cat = 'Cat2'
    elif wind_speed <= 113:
        cat = 'Cat3'
    elif wind_speed <= 135:
        cat = 'Cat4'
    else:
        cat = 'Cat5'
    return cat
