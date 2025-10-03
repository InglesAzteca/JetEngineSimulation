import customtkinter as ctk
from tkinter import messagebox
from gui.plotting import plot_P_vs_T, plot_T_vs_s, plot_efficiency_vs_rp, plot_net_work_vs_rp
from simulation.brayton_cycle import BraytonCycle
from tkinter import filedialog
import math

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JetEngineApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Brayton Cycle Simulator")
        self.geometry("600x500")
        self.resizable(True, True)
        self.current_figure = None
        self.presets = {
                        "Standard Jet": {
                            "T1": 288,
                            "P1": 101325,
                            "rp": 10,
                            "Tmax": 1600,
                            "eta_c": 0.85,
                            "eta_t": 0.88,
                        },
                        "High Efficiency": {
                            "T1": 288,
                            "P1": 101325,
                            "rp": 30,
                            "Tmax": 1900,
                            "eta_c": 0.9,
                            "eta_t": 0.93,
                        },
                        "Low Bypass (Test)": {
                            "T1": 273,
                            "P1": 95000,
                            "rp": 15,
                            "Tmax": 1700,
                            "eta_c": 0.82,
                            "eta_t": 0.85,
                        }
                    }
        self.input_bounds = {
                            "T1": (200, 400),             # Kelvin
                            "P1": (50000, 500000),        # Pascals
                            "rp": (1.5, 40),              # Pressure ratio
                            "Tmax": (1200, 2000),         # Max turbine temp
                            "eta_c": (0.7, 0.95),         # Compressor efficiency
                            "eta_t": (0.7, 0.95),         # Turbine efficiency
}
        self.plot_type_dropdown = None
        self.sliders = {}
        self.create_widgets()

    def build_left_frame(self, frame):
        page_dropdown = ctk.CTkComboBox(frame, values=["Theoretical", "Practical"], width=140, state="readonly")
        page_dropdown.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0), columnspan=2)
        page_dropdown.set("Theoretical")

        input_frame = ctk.CTkFrame(master=frame)
        input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.preset_selector = ctk.CTkComboBox(input_frame,
                                            values=list(self.presets.keys()),
                                            command=self.load_preset,
                                            width=180,
                                            state="readonly")
        self.preset_selector.set("Select Preset")
        self.preset_selector.grid(row=0, column=0, sticky="w", columnspan=2, padx=10, pady=(10, 10))

        self.entries = {}

        fields = [
            ("Inlet Temperature (T1) [K]", "T1"),
            ("Inlet Pressure (P1) [Pa]", "P1"),
            ("Pressure Ratio (rp)", "rp"),
            ("Maximum Temp (Tmax) [K]", "Tmax"),
            ("Compressor Efficiency (η_c)", "eta_c"),
            ("Turbine Efficiency (η_t)", "eta_t"),
        ]

        row = 1
        for label_text, key in fields:
            label = ctk.CTkLabel(input_frame, text=label_text)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            entry = ctk.CTkEntry(input_frame, width=120)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[key] = entry

            # Add slider for pressure ratio
            if key in ("rp", "Tmax", "eta_c", "eta_t"):
                if key == "rp":
                    preset = 10
                    steps = 77
                    minimum = 1.5
                    maximum = 40
                    decimal_points = 1
                elif key == "Tmax":
                    preset = 1600
                    steps = 28
                    minimum = 1200
                    maximum = 2000
                    decimal_points = 0
                elif key == "eta_c":
                    preset = 0.85
                    steps = 25
                    minimum = 0.7
                    maximum = 0.95
                    decimal_points = 2
                else:
                    preset = 0.88
                    steps = 25
                    minimum = 0.7
                    maximum = 0.95
                    decimal_points = 2

                row += 1
                slider = ctk.CTkSlider(input_frame, from_=minimum, to=maximum, number_of_steps=steps)
                slider.set(preset)
                slider.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
                self.sliders[key] = slider

                # Define sync: Slider → Entry
                def update_entry(val, e=entry):  # Binds the specific entry for this iteration
                    rounded = round(float(val), decimal_points)
                    e.delete(0, "end")
                    e.insert(0, f"{rounded}")

                # Define sync: Entry → Slider
                def update_slider(event, s=slider, e=entry):
                    try:
                        value = float(e.get())
                        value = min(max(value, minimum), maximum)  # Clamp within range
                        s.set(value)
                    except ValueError:
                        pass  # Ignore invalid input

                # Bind and configure
                slider.configure(command=update_entry)
                entry.bind("<KeyRelease>", update_slider)

            row+=1

        # Run and Reset Buttons (side-by-side)
        run_button = ctk.CTkButton(master=frame, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")

        reset_button = ctk.CTkButton(master=frame, text="Reset", command=self.reset)
        reset_button.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="w")

        # # Output box
        # self.output_box = ctk.CTkTextbox(master=frame, width=340, height=200)
        # self.output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        # self.output_box.insert("0.0", "Output will appear here...\n")

    def build_right_frame(self, frame):
        # Dropdown top left
        self.plot_type_dropdown = ctk.CTkComboBox(frame, 
                                                  values=[
                                                      "P vs T", 
                                                      "T vs s", 
                                                      "Efficiency vs Pressure Ratio", 
                                                      "Net Work vs Pressure Ratio"], 
                                                  width=180, 
                                                  state="readonly",
                                                  command=self.update_plot)
        self.plot_type_dropdown.set("P vs T")
        self.plot_type_dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))
        
        # Output box
        self.output_box = ctk.CTkTextbox(master=frame, width=180)
        self.output_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.output_box.insert("0.0", "Output will appear here...\n")

        # Graph Canvas
        self.graph_canvas = ctk.CTkFrame(frame, fg_color="black")
        self.graph_canvas.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Save Button
        save_btn = ctk.CTkButton(frame, text="Save Graph", command=self.save_graph)
        save_btn.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="e")

        # Allow graph canvas to expand
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        frame.grid_rowconfigure(1, weight=1)

    def create_widgets(self):
        # Tab structure
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        tab_name_1 = "tab 1"
        tab_name_2 = "tab 2"

        tabview.add(tab_name_1)
        tabview.add(tab_name_2)

        tab1 = tabview.tab(tab_name_1)
        tab2 = tabview.tab(tab_name_2)

        # Grid layout in tab1
        tab1.grid_rowconfigure(0, weight=1)
        tab1.grid_columnconfigure(1, weight=1)

        # Left panel (narrow)
        left_frame = ctk.CTkFrame(master=tab1, width=350)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Right panel (larger graph area)
        right_frame = ctk.CTkFrame(master=tab1)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.build_left_frame(left_frame)
        self.build_right_frame(right_frame)
    
    def load_preset(self, preset_name):
        preset = self.presets.get(preset_name)
        if not preset:
            return

        for key, value in preset.items():
            if key in self.entries:
                self.entries[key].delete(0, "end")
                self.entries[key].insert(0, str(value))

                # Sync rp slider if present
            if key in ("rp", "Tmax", "eta_c", "eta_t"): # add and hasattr(self, "rp_slider") if needed
                try:
                    self.sliders[key].set(float(value))
                except ValueError:
                    pass
    
    def update_plot(self, _=None):
        self.run_simulation()

    def reset(self):
        # Clear all input entries
        for entry in self.entries.values():
            entry.delete(0, "end")

        # Clear output textbox
        self.output_box.delete("0.0", "end")
        self.output_box.insert("0.0", "Output will appear here...\n")

        # Clear graph canvas (plot area)
        for widget in self.graph_canvas.winfo_children():
            widget.destroy()

    def run_simulation(self):
        if not self.validate_inputs():
            print("Invalid input detected.")
            return

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

            result_text = f"Simulation Results:\n"

            for key, value in results.items():
                result_text += f"{key}: {value:.2f}\n"

            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", result_text)

            # Plot setup
            T2 = results["T2"]
            T3 = results["T3"]
            T4 = results["T4"]
            T_vals = [T1, T2, T3, T4, T1]

            P2 = P1 * rp
            P3 = P2
            P4 = P1
            P_vals = [P1, P2, P3, P4, P1]


            plot_type = self.plot_type_dropdown.get()

            if plot_type == "P vs T":
                self.current_figure = plot_P_vs_T(self.graph_canvas, T_vals, P_vals)
            elif plot_type == "T vs s":
                cp = 1005 # J/kg·K (ideal air)
                gamma = 1.4
                R = cp * (1 - 1 / gamma)

                s1 = 0
                s2 = s1 + (cp * math.log(T2 / T1) - R * math.log(P2 / P1)) / 1000
                s3 = s2 + (cp * math.log(T3 / T2)) / 1000
                s4 = s3 + (cp * math.log(T4 / T3) - R * math.log(P1 / P2)) / 1000
                s1_closure = s4 + (cp * math.log(T1 / T4)) / 1000

                s_vals = [s1, s2, s3, s4, s1_closure]

                self.current_figure = plot_T_vs_s(self.graph_canvas, s_vals, T_vals)
            elif plot_type == "Efficiency vs Pressure Ratio":
                self.current_figure = plot_efficiency_vs_rp(self.graph_canvas)
            elif plot_type == "Net Work vs Pressure Ratio":
                T1 = float(self.entries["T1"].get())
                Tmax = float(self.entries["Tmax"].get())
                eta_c = float(self.entries["eta_c"].get())
                eta_t = float(self.entries["eta_t"].get())

                self.current_figure = plot_net_work_vs_rp(
                    self.graph_canvas, T1, Tmax, eta_c, eta_t
                )


        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def validate_inputs(self):
        for key, entry in self.entries.items():
            val = entry.get()
            try:
                num = float(val)
                min_val, max_val = self.input_bounds[key]
                if not (min_val <= num <= max_val):
                    entry.configure(border_color="red")
                    return False
                else:
                    entry.configure(border_color="gray")  # reset color if valid
            except ValueError:
                entry.configure(border_color="red")
                return False
        return True


    def save_graph(self):
        if self.current_figure is None:
            messagebox.showwarning("No Plot", "There is no graph to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG Image", "*.png"),
                                                            ("PDF File", "*.pdf"),
                                                            ("All Files", "*.*")],
                                                title="Save Plot As")
        if file_path:
            self.current_figure.savefig(file_path)
            messagebox.showinfo("Success", f"Graph saved to:\n{file_path}")

