def ideal_efficiency(pressure_ratio, heat_capacity_ratio):
    efficiency =  1 - (1 / pressure_ratio**((heat_capacity_ratio - 1) / heat_capacity_ratio))
    return efficiency
