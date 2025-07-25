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
