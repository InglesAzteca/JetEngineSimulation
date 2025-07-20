def turbine_exit_temperature(turbine_inlet_temperature, pressure_ratio, heat_capacity_ratio):
    temperature = turbine_inlet_temperature * (1 / pressure_ratio)**((heat_capacity_ratio - 1)/heat_capacity_ratio)
    return temperature

