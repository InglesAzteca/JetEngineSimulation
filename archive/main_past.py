# Jet Engine Simulation – Brayton Cycle (Ideal)
import numpy as np
import matplotlib.pyplot as plt
from archive.isentropic_expansion import turbine_exit_temperature
from archive.isentropic_compression import compressor_exit_temperature, compressor_exit_pressure
from archive.thermal_efficiency import ideal_efficiency
from archive.work_and_heat import compressor_work, turbine_work, heat_added
from display_results import display_temperature, display_work, display_efficiency

# Constants
gamma = 1.4          # Heat capacity ratio for air
cp = 1005            # Specific heat of air at constant pressure [J/kg·K]
T1 = 288             # Ambient temperature [K]
P1 = 101325          # Ambient pressure [Pa]

# User Inputs
pressure_ratio = 10         # Compressor pressure ratio (P2/P1)
T_max = 1400                # Maximum temperature after combustion [K]

# Stage 1 → 2: Isentropic Compression
T2 = compressor_exit_temperature(T1, pressure_ratio, gamma)
P2 = compressor_exit_pressure(P1, pressure_ratio)

# Stage 2 → 3: Constant Pressure Heat Addition
T3 = T_max
P3 = P2

# Stage 3 → 4: Isentropic Expansion
T4 = turbine_exit_temperature(T3, pressure_ratio, gamma)
P4 = P1

# Thermal Efficiency (Ideal Brayton Cycle)
eta_ideal = ideal_efficiency(pressure_ratio, gamma)

# Work and Heat Calculations [J/kg]
w_compressor = compressor_work(cp, T2, T1)
w_turbine = turbine_work(cp, T3, T4)
q_in = heat_added(cp, T3, T2)
w_net = w_turbine - w_compressor
eta_actual = w_net / q_in

# Output Results
print("---- Jet Engine Simulation (Ideal Brayton Cycle) ----\n")
display_temperature(T2, T3, T4)
display_work(w_compressor, w_turbine, q_in, w_net)
display_efficiency(eta_ideal, eta_actual)

# ---------- Step 2: T-s Diagram (Qualitative) ----------
s1, s2, s3, s4 = 1.0, 1.0, 1.5, 1.5  # Entropy in arbitrary units
T_s = [T1, T2, T3, T4, T1]
s_vals = [s1, s2, s3, s4, s1]

plt.figure()
plt.plot(s_vals, T_s, marker='o')
plt.title("Ideal Brayton Cycle (T-s Diagram)")
plt.xlabel("Entropy [arbitrary units]")
plt.ylabel("Temperature [K]")
plt.grid(True)
for i, (s, T) in enumerate(zip(s_vals[:4], T_s[:4])):
    plt.text(s, T + 20, f"{i+1}", ha='center')
plt.show()

# ---------- Step 3: Parametric Study ----------
pr_range = np.linspace(2, 30, 100)
eta_range = 1 - (1 / pr_range**((gamma - 1) / gamma))

# Optional: Net work output vs pressure ratio (assume T1, T_max are fixed)
T2_range = T1 * pr_range**((gamma - 1)/gamma)
T4_range = T_max * (1 / pr_range)**((gamma - 1)/gamma)
w_net_range = cp * ((T_max - T4_range) - (T2_range - T1))

# Plot Efficiency
plt.figure()
plt.plot(pr_range, eta_range * 100)
plt.title("Brayton Cycle Efficiency vs Pressure Ratio")
plt.xlabel("Pressure Ratio")
plt.ylabel("Thermal Efficiency [%]")
plt.grid(True)
plt.show()

# Plot Net Work Output
plt.figure()
plt.plot(pr_range, w_net_range)
plt.title("Net Work Output vs Pressure Ratio")
plt.xlabel("Pressure Ratio")
plt.ylabel("Net Work Output [J/kg]")
plt.grid(True)
plt.show()
