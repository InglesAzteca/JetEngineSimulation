def compressor_work(specific_heat, compressor_exit_temperature, compressor_inlet_temperature):
    work = specific_heat * (compressor_exit_temperature - compressor_inlet_temperature)
    return work

def turbine_work(specific_heat, turbine_inlet_temperature, turbine_exit_temperature):
    work = specific_heat * (turbine_inlet_temperature - turbine_exit_temperature)
    return work

def heat_added(specific_heat, turbine_inlet_temperature, compressor_exit_temperature):
    energy = specific_heat * (turbine_inlet_temperature - compressor_exit_temperature)
    return energy

