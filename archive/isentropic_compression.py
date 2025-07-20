def compressor_exit_temperature(compressor_inlet_temperature, pressure_ratio, heat_capacity_ratio):
    temperature = compressor_inlet_temperature * (pressure_ratio)**((heat_capacity_ratio - 1)/heat_capacity_ratio)
    return temperature

def compressor_exit_pressure(compressor_inlet_pressure, pressure_ratio):
    pressure = compressor_inlet_pressure * pressure_ratio
    return pressure

