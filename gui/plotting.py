from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plot_cycle(parent_frame, T_vals, P_vals):
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
