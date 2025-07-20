def display_temperature(compressor_exit_temperature, turbine_inlet_temperature, turbine_exit_temperature):
    print(f"--- Temperature Analysis ---")
    print(f"Compressor Exit Temperature (T2): {compressor_exit_temperature:.2f} K")
    print(f"Turbine Inlet Temperature (T3): {turbine_inlet_temperature:.2f} K")
    print(f"Turbine Exit Temperature (T4): {turbine_exit_temperature:.2f} K")

def display_work(compressor_work, turbine_work, heat_added, net_work):
    print(f"--- Energy Analysis ---")
    print(f"Compressor Work Input: {compressor_work:.2f} J/kg")
    print(f"Turbine Work Output: {turbine_work:.2f} J/kg")
    print(f"Heat Added in Combustion Chamber: {heat_added:.2f} J/kg")
    print(f"Net Work Output: {net_work:.2f} J/kg")

def display_efficiency(ideal_efficiency, actual_efficiency):
    print(f"--- Efficieny Analysis ---")
    print(f"Ideal Thermal Efficiency: {ideal_efficiency * 100:.2f}%")
    print(f"Actual (calculated) Efficiency: {actual_efficiency * 100:.2f}%")
