

def conv_ocean_proximity(ocean_proximity):
    if (ocean_proximity == "<1H OCEAN"):
        return 1, 0, 0, 0, 0
    elif (ocean_proximity == "INLAND"):
        return 0, 1, 0, 0, 0
    elif (ocean_proximity == "ISLAND"):
        return 0, 0, 1, 0, 0
    elif (ocean_proximity == "NEAR BAY"):
        return 0, 0, 0, 1, 0
    elif (ocean_proximity == "NEAR OCEAN"):
        return 0, 0, 0, 0, 1