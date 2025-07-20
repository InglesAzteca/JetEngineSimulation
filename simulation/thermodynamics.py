def compressor_exit_temperature(compressor_inlet_temperature, pressure_ratio, heat_capacity_ratio):
    temperature = compressor_inlet_temperature * (pressure_ratio)**((heat_capacity_ratio - 1)/heat_capacity_ratio)
    return temperature

def compressor_exit_pressure(compressor_inlet_pressure, pressure_ratio):
    pressure = compressor_inlet_pressure * pressure_ratio
    return pressure

def turbine_exit_temperature(turbine_inlet_temperature, pressure_ratio, heat_capacity_ratio):
    temperature = turbine_inlet_temperature * (1 / pressure_ratio)**((heat_capacity_ratio - 1)/heat_capacity_ratio)
    return temperature

def compressor_work(specific_heat, compressor_exit_temperature, compressor_inlet_temperature):
    work = specific_heat * (compressor_exit_temperature - compressor_inlet_temperature)
    return work

def turbine_work(specific_heat, turbine_inlet_temperature, turbine_exit_temperature):
    work = specific_heat * (turbine_inlet_temperature - turbine_exit_temperature)
    return work

def heat_added(specific_heat, turbine_inlet_temperature, compressor_exit_temperature):
    energy = specific_heat * (turbine_inlet_temperature - compressor_exit_temperature)
    return energy

def ideal_efficiency(pressure_ratio, heat_capacity_ratio):
    efficiency =  1 - (1 / pressure_ratio**((heat_capacity_ratio - 1) / heat_capacity_ratio))
    return efficiency
