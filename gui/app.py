import customtkinter as ctk
from tkinter import messagebox

# Later we'll import Brayton logic like this:
from simulation.brayton_cycle import BraytonCycle

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JetEngineApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Brayton Cycle Simulator")
        self.geometry("600x500")
        self.resizable(True, True)
        self.create_widgets()

    def create_widgets(self):
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20, fill="x")

        self.entries = {}

        fields = [
            ("Inlet Temperature (T1) [K]", "T1"),
            ("Inlet Pressure (P1) [kPa]", "P1"),
            ("Pressure Ratio (rp)", "rp"),
            ("Maximum Temp (Tmax) [K]", "Tmax"),
            ("Compressor Efficiency (η_c)", "eta_c"),
            ("Turbine Efficiency (η_t)", "eta_t"),
        ]

        for i, (label_text, key) in enumerate(fields):
            label = ctk.CTkLabel(input_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            entry = ctk.CTkEntry(input_frame, width=120)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = entry

        run_button = ctk.CTkButton(self, text="Run Simulation", command=self.run_simulation)
        run_button.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=540, height=150, corner_radius=10)
        self.output_box.pack(pady=10)
        self.output_box.insert("0.0", "Output will appear here...\n")

    def run_simulation(self):
        try:
            T1 = float(self.entries["T1"].get())
            P1 = float(self.entries["P1"].get())
            rp = float(self.entries["rp"].get())
            Tmax = float(self.entries["Tmax"].get())
            eta_c = float(self.entries["eta_c"].get())
            eta_t = float(self.entries["eta_t"].get())

            brayton_cycle_instance = BraytonCycle(T1, P1, rp, Tmax)
            brayton_cycle_instance.run()
            results = brayton_cycle_instance.get_results()

            result_text = f"""Inputs received:
T1 = {T1} K
P1 = {P1} kPa
rp = {rp}
Tmax = {Tmax} K
η_c = {eta_c}
η_t = {eta_t}
Simulation Results:\n
"""

            for key, value in results.items():
                result_text += f"{key}: {value:.2f}\n"

            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", result_text)


        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

