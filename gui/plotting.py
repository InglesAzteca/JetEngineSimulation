from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

def plot_P_vs_T(parent_frame, T_vals, P_vals):
    # Clear previous plot
    for widget in parent_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(T_vals, P_vals, marker="o")

    labels = ["1 (Inlet)", "2 (Post-Comp)", "3 (Max T)", "4 (Post-Turb)"]
    offset = [(0, -10), (0, 10), (0, 10), (0, -10)]

    for i, (T, P) in enumerate(zip(T_vals[:-1], P_vals[:-1])):
        label = labels[i]
        ax.annotate(label, (T, P),
                    textcoords="offset points", 
                    xytext=offset[i], 
                    ha='center', fontsize=8, color="gray", fontweight="bold")


    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Pressure (kPa)")
    ax.set_title("Brayton Cycle - P vs T")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig

def plot_T_vs_s(parent_frame, s_vals, T_vals):
    # Clear previous plot
    for widget in parent_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(s_vals, T_vals, marker="o")

    labels = ["1 (Inlet)", "2 (Post-Comp)", "3 (Max T)", "4 (Post-Turb)"]
    offset = [(0, -10), (0, 10), (0, 10), (0, -10)]

    for i, (s, T) in enumerate(zip(s_vals[:-1], T_vals[:-1])):
        label = labels[i]
        ax.annotate(label, (s, T),
                    textcoords="offset points", 
                    xytext=offset[i], 
                    ha='center', fontsize=8, color="gray", fontweight="bold")

    ax.set_xlabel("Entropy (arb. units)")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Brayton Cycle - T vs s")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig

def plot_efficiency_vs_rp(parent_frame, gamma=1.4):
    # Clear previous plot
    for widget in parent_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Pressure ratio range
    rp_vals = [x / 10 for x in range(15, 401)]  # From 1.5 to 40 in 0.1 steps
    eta_vals = [1 - (1 / (rp ** ((gamma - 1) / gamma))) for rp in rp_vals]

    ax.plot(rp_vals, eta_vals, color="blue", linewidth=2)
    ax.set_xlabel("Pressure Ratio (rp)")
    ax.set_ylabel("Thermal Efficiency (η)")
    ax.set_title("Thermal Efficiency vs Pressure Ratio")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig

def plot_net_work_vs_rp(parent_frame, T1, Tmax, eta_c, eta_t, gamma=1.4, cp=1005):
    # Clear previous plot
    for widget in parent_frame.winfo_children():
        widget.destroy()


    rp_range = np.linspace(1.5, 40, 100)
    net_work = []

    for rp in rp_range:
        T2 = T1 * (rp ** ((gamma - 1) / gamma / eta_c))
        T4 = Tmax * (1 / rp) ** ((gamma - 1) / gamma * eta_t)

        W_in = cp * (T2 - T1)
        W_out = cp * (Tmax - T4)
        W_net = W_out - W_in
        net_work.append(W_net)

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(rp_range, net_work, color="green")

    ax.set_title("Net Work Output vs Pressure Ratio")
    ax.set_xlabel("Pressure Ratio (rp)")
    ax.set_ylabel("Net Work Output (J/kg)")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig

def plot_efficiency_vs_Tmax(parent_frame, T1, rp, gamma):
    import numpy as np

    # Clear previous plot
    for widget in parent_frame.winfo_children():
        widget.destroy()

    cp = 1005  # J/kg·K
    T2 = T1 * (rp ** ((gamma - 1) / gamma))
    Tmax_range = np.linspace(T2 + 50, 1500, 100)
    efficiencies = []

    for T3 in Tmax_range:
        T4 = T3 * (1 / rp) ** ((gamma - 1) / gamma)
        print(f"T4: {T4}")

        work_comp = cp * (T2 - T1)
        work_turb = cp * (T3 - T4)
        q_in = cp * (T3 - T2)

        eta = (work_turb - work_comp) / q_in
        print(eta)
        efficiencies.append(eta)

    # Plot
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(Tmax_range, efficiencies, color='orange')
    ax.set_xlabel("Maximum Temperature (Tmax) [K]")
    ax.set_ylabel("Thermal Efficiency (η)")
    ax.set_title("Thermal Efficiency vs Tmax")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig
