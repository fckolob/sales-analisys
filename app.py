import pandas as pd
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Global data
df = None
chart_canvas = None


# -------------------------
# Load dataset
# -------------------------
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        try:
            df = pd.read_csv(file_path)
            df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
            df.dropna(subset=['Sales'], inplace=True)

            output.delete("1.0", "end")
            output.insert("end", "✅ Dataset loaded successfully!\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# -------------------------
# Clear previous chart
# -------------------------
def clear_chart():
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
        chart_canvas = None


# -------------------------
# CATEGORY ANALYSIS
# -------------------------
def analyze_category():
    global chart_canvas

    if df is None:
        messagebox.showwarning("Warning", "Load dataset first!")
        return

    result = df.groupby('Category')['Sales'].sum() \
               .sort_values(ascending=False) \
               .head(10)

    output.delete("1.0", "end")
    output.insert("end", "📊 Top 10 Categories by Sales\n\n")
    output.insert("end", result.to_string())
    output.insert("end", f"\n\n🏆 Highest: {result.idxmax()} ({result.max()})")

    clear_chart()
    fig, ax = plt.subplots(figsize=(10, 6))

    result.plot(kind='barh', ax=ax)

    ax.set_title("Top 10 Categories by Sales")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Category")
    ax.tick_params(axis='both', labelsize=9)

    plt.tight_layout()

    draw_chart(fig)


# -------------------------
# COLOR ANALYSIS.
# -------------------------
def analyze_color():
    global chart_canvas

    if df is None:
        messagebox.showwarning("Warning", "Load dataset first!")
        return

    full = df.groupby('Color')['Sales'].sum().sort_values(ascending=False)

    top10 = full.head(10)
    others = full.iloc[10:].sum()

    if others > 0:
        top10['Others'] = others

    result = top10

    output.delete("1.0", "end")
    output.insert("end", "🎨 Top Colors by Sales\n\n")
    output.insert("end", result.to_string())
    output.insert("end", f"\n\n⚠️ Lowest: {result.idxmin()} ({result.min()})")

    clear_chart()
    fig, ax = plt.subplots(figsize=(10, 6))

    result.plot(kind='barh', ax=ax)

    ax.set_title("Top Colors by Sales")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Color")
    ax.tick_params(axis='both', labelsize=9)

    plt.tight_layout()

    draw_chart(fig)


# -------------------------
# SIZE ANALYSIS
# -------------------------
def show_size_chart():
    global chart_canvas

    if df is None:
        messagebox.showwarning("Warning", "Load dataset first!")
        return

    result = df.groupby('Size')['Sales'].sum().sort_values()

    output.delete("1.0", "end")
    output.insert("end", "📈 Sales by Size\n\n")
    output.insert("end", result.to_string())

    clear_chart()
    fig, ax = plt.subplots(figsize=(10, 5))

    result.plot(kind='bar', ax=ax)

    ax.set_title("Sales Distribution by Size")
    ax.set_xlabel("Size")
    ax.set_ylabel("Sales")

    plt.xticks(rotation=0)
    ax.tick_params(axis='both', labelsize=9)

    plt.tight_layout()

    draw_chart(fig)


# -------------------------
# DRAW CHART FUNCTION
# -------------------------
def draw_chart(fig):
    global chart_canvas
    chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(fill="both", expand=True)


# -------------------------
# UI SETUP
# -------------------------
app = tb.Window(themename="darkly")
app.title("Inventory Dashboard Pro")
app.geometry("1000x600")

# Layout
sidebar = tb.Frame(app)
sidebar.pack(side="left", fill="y")

main = tb.Frame(app)
main.pack(side="right", expand=True, fill="both")

# Sidebar
tb.Label(sidebar, text="📦 Dashboard", font=("Segoe UI", 16, "bold")).pack(pady=20)

tb.Button(sidebar, text="Load Dataset", bootstyle="info", width=20, command=load_file).pack(pady=10)
tb.Button(sidebar, text="Category Analysis", bootstyle="primary", width=20, command=analyze_category).pack(pady=10)
tb.Button(sidebar, text="Color Analysis", bootstyle="warning", width=20, command=analyze_color).pack(pady=10)
tb.Button(sidebar, text="Size Distribution", bootstyle="success", width=20, command=show_size_chart).pack(pady=10)

# Output panel
output = tb.Text(main, height=10, font=("Consolas", 10))
output.pack(fill="x", padx=10, pady=10)

# Chart area
chart_frame = tb.Frame(main)
chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Run app
app.mainloop()