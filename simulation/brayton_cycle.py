from simulation.thermodynamics import (
    compressor_exit_temperature,
    compressor_exit_pressure,
    turbine_exit_temperature,
    compressor_work,
    turbine_work,
    heat_added,
    ideal_efficiency
)

class BraytonCycle:
    def __init__(self, T1, P1, pressure_ratio, T_max, cp=1005, gamma=1.4):
        self.T1 = T1                            # Ambient temperature [K]
        self.P1 = P1                            # Ambient pressure [Pa]
        self.pressure_ratio = pressure_ratio    # Compressor pressure ratio (P2/P1)
        self.T_max = T_max                      # Maximum temperature after combustion [K]
        self.cp = cp                            # Specific heat of air at constant pressure [J/kg·K]
        self.gamma = gamma                      # Heat capacity ratio for air

        # Output values (to be calculated)
        self.T2 = None
        self.P2 = None
        self.T3 = None
        self.P3 = None
        self.T4 = None
        self.P4 = None
        self.w_compressor = None
        self.w_turbine = None
        self.w_net = None
        self.q_in = None
        self.eta_ideal = None
        self.eta_actual = None

    def run(self):
        # Stage 1 → 2: Isentropic Compression
        self.T2 = compressor_exit_temperature(self.T1, self.pressure_ratio, self.gamma)
        self.P2 = compressor_exit_pressure(self.P1, self.pressure_ratio)

        # Stage 2 → 3: Heat Addition (constant pressure)
        self.T3 = self.T_max
        self.P3 = self.P2

        # Stage 3 → 4: Isentropic Expansion
        self.T4 = turbine_exit_temperature(self.T3, self.pressure_ratio, self.gamma)
        self.P4 = self.P1

        # Work & Heat Calculations
        self.w_compressor = compressor_work(self.cp, self.T2, self.T1)
        self.w_turbine = turbine_work(self.cp, self.T3, self.T4)
        self.q_in = heat_added(self.cp, self.T3, self.T2)
        self.w_net = self.w_turbine - self.w_compressor

        # Efficiencies
        self.eta_ideal = ideal_efficiency(self.pressure_ratio, self.gamma)
        self.eta_actual = self.w_net / self.q_in if self.q_in != 0 else 0

    def get_results(self):
        return {
            "T2": self.T2,
            "T3": self.T3,
            "T4": self.T4,
            "w_compressor": self.w_compressor,
            "w_turbine": self.w_turbine,
            "q_in": self.q_in,
            "w_net": self.w_net,
            "eta_ideal": self.eta_ideal,
            "eta_actual": self.eta_actual
        }
