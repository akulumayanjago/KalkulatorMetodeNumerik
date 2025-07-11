import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk

# Fungsi dinamis dari input user
def fungsi(x):
    try:
        return eval(entry_fx.get(), {"x": x, "np": np})
    except Exception as e:
        raise ValueError(f"f(x) error: {e}")

def dfung(x):
    try:
        return eval(entry_dfx.get(), {"x": x, "np": np})
    except Exception as e:
        raise ValueError(f"f'(x) error: {e}")

def g(x):
    try:
        return eval(entry_gx.get(), {"x": x, "np": np})
    except Exception as e:
        raise ValueError(f"g(x) error: {e}")

# Metode numerik (tidak berubah)
def secant(x0, x1, tol):
    i = 0
    x_temp = x0
    hasil = []
    while abs(fungsi(x_temp)) > tol:
        i += 1
        if fungsi(x1) - fungsi(x0) == 0:
            return hasil, x1
        x_temp = x1 - (fungsi(x1) * (x1 - x0)) / (fungsi(x1) - fungsi(x0))
        hasil.append(f"Iterasi {i}: x0={x0:.6f}, x1={x1:.6f}, x_temp={x_temp:.6f}, f(x1)={fungsi(x1):.6f}")
        x0 = x1
        x1 = x_temp
    return hasil, x1

def newtonraphson(x0, tol):
    i = 0
    delta = abs(fungsi(x0))
    hasil = []
    while delta >= tol:
        fx = fungsi(x0)
        dfx = dfung(x0)
        x_temp = fx / dfx
        x0 = x0 - x_temp
        delta = abs(fungsi(x0))
        i += 1
        hasil.append(f"Iterasi {i}: x0={x0:.6f}, f(x0)={fungsi(x0):.6f}, f'(x0)={dfung(x0):.6f}, x_temp={x_temp:.6f}")
    return hasil, x0

def metode_bisection(a, b, tol):
    i = 0
    hasil = []
    if fungsi(a) * fungsi(b) > 0:
        return ["Fungsi tidak memiliki akar dalam interval [a,b]."], None
    while abs(b - a) > tol:
        x = (a + b) / 2.0
        i += 1
        hasil.append(f"Iterasi {i}: a={a:.6f}, b={b:.6f}, x={x:.6f}, f(a)={fungsi(a):.6f}, f(b)={fungsi(b):.6f}, f(x)={fungsi(x):.6f}")
        if fungsi(x) == 0:
            return hasil, x
        elif fungsi(a) * fungsi(x) < 0:
            b = x
        else:
            a = x
    return hasil, x

def regulafalsi(a, b, tol):
    hasil = []
    if fungsi(a) * fungsi(b) > 0:
        return ["Input tidak memenuhi syarat metode Regula Falsi."], None
    i = 1
    x = a
    while abs(fungsi(x)) > tol:
        x = (a * fungsi(b) - b * fungsi(a)) / (fungsi(b) - fungsi(a))
        hasil.append(f"Iterasi {i}: a={a:.6f}, b={b:.6f}, x={x:.6f}, f(a)={fungsi(a):.6f}, f(b)={fungsi(b):.6f}, f(x)={fungsi(x):.6f}")
        if fungsi(x) == 0:
            break
        elif fungsi(x) * fungsi(a) < 0:
            b = x
        else:
            a = x
        i += 1
    return hasil, x

def fixed_point_iteration(x0, tol, max_iter=100):
    i = 0
    x1 = g(x0)
    hasil = []
    while abs(x1 - x0) > tol and i < max_iter:
        hasil.append(f"Iterasi {i+1}: x0={x0:.6f}, x1={x1:.6f}, |x1-x0|={abs(x1-x0):.6f}")
        x0 = x1
        x1 = g(x0)
        i += 1
    if i == max_iter:
        hasil.append("Iterasi maksimum tercapai tanpa konvergen.")
        return hasil, None
    return hasil, x1

# GUI Tkinter
def tampilkan_hasil_tabel(header, rows, akar):
    output.config(state='normal')
    output.delete(1.0, tk.END)
    output.insert(tk.END, header + "\n")
    output.insert(tk.END, "-" * len(header) + "\n")
    for row in rows:
        output.insert(tk.END, row + "\n")
    output.insert(tk.END, "-" * len(header) + "\n")
    if akar is not None:
        output.insert(tk.END, f"\nAkar: {akar:.6f}\n")
    output.config(state='disabled')

def run_secant():
    try:
        x0 = float(entry_x0.get())
        x1 = float(entry_x1.get())
        tol = float(entry_tol.get())
        hasil, akar = secant(x0, x1, tol)
        header = "{:>4} {:>12} {:>12} {:>12} {:>12}".format("Iter", "x0", "x1", "x_temp", "f(x1)")
        rows = []
        for i, h in enumerate(hasil):
            # Parsing string hasil menjadi list
            vals = [v.split("=")[-1] for v in h.replace("Iterasi ", "").replace(":", "").split(",")]
            rows.append("{:>4} {:>12} {:>12} {:>12} {:>12}".format(i+1, *vals))
        tampilkan_hasil_tabel(header, rows, akar)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_newton():
    try:
        x0 = float(entry_x0.get())
        tol = float(entry_tol.get())
        hasil, akar = newtonraphson(x0, tol)
        header = "{:>4} {:>12} {:>12} {:>12} {:>12}".format("Iter", "x0", "f(x0)", "f'(x0)", "x_temp")
        rows = []
        for i, h in enumerate(hasil):
            vals = [v.split("=")[-1] for v in h.replace("Iterasi ", "").replace(":", "").split(",")]
            rows.append("{:>4} {:>12} {:>12} {:>12} {:>12}".format(i+1, *vals))
        tampilkan_hasil_tabel(header, rows, akar)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_bisection():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        tol = float(entry_tol.get())
        hasil, akar = metode_bisection(a, b, tol)
        header = "{:>4} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format("Iter", "a", "b", "x", "f(a)", "f(b)", "f(x)")
        rows = []
        for i, h in enumerate(hasil):
            if "Fungsi tidak memiliki akar" in h:
                rows.append(h)
            else:
                vals = [v.split("=")[-1] for v in h.replace("Iterasi ", "").replace(":", "").split(",")]
                rows.append("{:>4} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(i+1, *vals))
        tampilkan_hasil_tabel(header, rows, akar)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_regulafalsi():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        tol = float(entry_tol.get())
        hasil, akar = regulafalsi(a, b, tol)
        header = "{:>4} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format("Iter", "a", "b", "x", "f(a)", "f(b)", "f(x)")
        rows = []
        for i, h in enumerate(hasil):
            if "Input tidak memenuhi syarat" in h:
                rows.append(h)
            else:
                vals = [v.split("=")[-1] for v in h.replace("Iterasi ", "").replace(":", "").split(",")]
                rows.append("{:>4} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(i+1, *vals))
        tampilkan_hasil_tabel(header, rows, akar)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_fixedpoint():
    try:
        x0 = float(entry_x0.get())
        tol = float(entry_tol.get())
        hasil, akar = fixed_point_iteration(x0, tol)
        header = "{:>4} {:>12} {:>12} {:>12}".format("Iter", "x0", "x1", "|x1-x0|")
        rows = []
        for i, h in enumerate(hasil):
            if "Iterasi maksimum" in h:
                rows.append(h)
            else:
                vals = [v.split("=")[-1] for v in h.replace("Iterasi ", "").replace(":", "").split(",")]
                rows.append("{:>4} {:>12} {:>12} {:>12}".format(i+1, *vals))
        tampilkan_hasil_tabel(header, rows, akar)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Kalkulator Metode Numerik")
root.configure(bg="#f6f6fa")

# Judul dan deskripsi
judul = tk.Label(root, text="Kalkulator Metode Numerik", font=("Segoe UI", 18, "bold"), bg="#f6f6fa", fg="#273c75")
judul.pack(pady=(15, 0))
deskripsi = tk.Label(root, text="Masukkan fungsi dan parameter yang diperlukan, lalu klik metode yang diinginkan.",
                    font=("Segoe UI", 10), bg="#f6f6fa", fg="#353b48")
deskripsi.pack(pady=(0, 10))

main_frame = tk.Frame(root, bg="#f6f6fa", bd=2, relief="groove")
main_frame.pack(padx=15, pady=5, fill="x")

# Input Fungsi Frame
fungsi_frame = tk.LabelFrame(main_frame, text="Input Fungsi", font=("Segoe UI", 10, "bold"), bg="#f6f6fa", fg="#222f3e", padx=10, pady=8)
fungsi_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5, columnspan=2)

tk.Label(fungsi_frame, text="f(x):", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=0, column=0, sticky="e")
entry_fx = tk.Entry(fungsi_frame, width=35, font=("Consolas", 10))
entry_fx.insert(0, "np.exp(x) - 5*x**2")
entry_fx.grid(row=0, column=1, padx=5, pady=2)

tk.Label(fungsi_frame, text="f'(x):", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=1, column=0, sticky="e")
entry_dfx = tk.Entry(fungsi_frame, width=35, font=("Consolas", 10))
entry_dfx.insert(0, "np.exp(x) - 10*x")
entry_dfx.grid(row=1, column=1, padx=5, pady=2)

tk.Label(fungsi_frame, text="g(x):", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=2, column=0, sticky="e")
entry_gx = tk.Entry(fungsi_frame, width=35, font=("Consolas", 10))
entry_gx.insert(0, "np.sqrt(2*x + 3)")
entry_gx.grid(row=2, column=1, padx=5, pady=2)

# Input Parameter Frame
input_frame = tk.LabelFrame(main_frame, text="Input Parameter", font=("Segoe UI", 10, "bold"), bg="#f6f6fa", fg="#222f3e", padx=10, pady=8)
input_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)

tk.Label(input_frame, text="x0:", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=0, column=0, sticky="e", pady=2)
entry_x0 = tk.Entry(input_frame, width=10, font=("Segoe UI", 10))
entry_x0.grid(row=0, column=1, pady=2, padx=(0, 10))

tk.Label(input_frame, text="x1:", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=0, column=2, sticky="e", pady=2)
entry_x1 = tk.Entry(input_frame, width=10, font=("Segoe UI", 10))
entry_x1.grid(row=0, column=3, pady=2, padx=(0, 10))

tk.Label(input_frame, text="a:", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=1, column=0, sticky="e", pady=2)
entry_a = tk.Entry(input_frame, width=10, font=("Segoe UI", 10))
entry_a.grid(row=1, column=1, pady=2, padx=(0, 10))

tk.Label(input_frame, text="b:", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=1, column=2, sticky="e", pady=2)
entry_b = tk.Entry(input_frame, width=10, font=("Segoe UI", 10))
entry_b.grid(row=1, column=3, pady=2, padx=(0, 10))

tk.Label(input_frame, text="Toleransi:", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=2, column=0, sticky="e", pady=2)
entry_tol = tk.Entry(input_frame, width=10, font=("Segoe UI", 10))
entry_tol.grid(row=2, column=1, pady=2, padx=(0, 10))

# Separator
ttk.Separator(main_frame, orient="horizontal").grid(row=2, column=0, sticky="ew", padx=10, pady=8, columnspan=2)

# Tombol Metode
button_frame = tk.Frame(main_frame, bg="#f6f6fa")
button_frame.grid(row=3, column=0, pady=5, columnspan=2)

tk.Button(button_frame, text="Secant", command=run_secant, width=16, bg="#00b894", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5, pady=4)
tk.Button(button_frame, text="Newton-Raphson", command=run_newton, width=16, bg="#0984e3", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5, pady=4)
tk.Button(button_frame, text="Bisection", command=run_bisection, width=16, bg="#fdcb6e", fg="#2d3436", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5, pady=4)
tk.Button(button_frame, text="Regula Falsi", command=run_regulafalsi, width=16, bg="#e17055", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=3, padx=5, pady=4)
tk.Button(button_frame, text="Fixed-Point", command=run_fixedpoint, width=16, bg="#6c5ce7", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, padx=5, pady=4)
def reset_input():
    entry_fx.delete(0, tk.END)
    entry_dfx.delete(0, tk.END)
    entry_gx.delete(0, tk.END)
    entry_x0.delete(0, tk.END)
    entry_x1.delete(0, tk.END)
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_tol.delete(0, tk.END)
    output.config(state='normal')
    output.delete(1.0, tk.END)
    output.config(state='disabled')

tk.Button(button_frame, text="Reset", command=reset_input, width=16, bg="#636e72", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=5, padx=5, pady=4)

# Daftar soal (bisa ditambah sesuai kebutuhan)
soal_list = [
    {
        "nama": "Soal 1: f(x) = exp(x) - 5x^2",
        "fx": "np.exp(x) - 5*x**2",
        "dfx": "np.exp(x) - 10*x",
        "gx": "np.sqrt(2*x + 3)",
        "x0": "0.5", "x1": "1", "a": "0", "b": "1", "tol": "1e-5"
    },
    {
        "nama": "Soal 2: f(x) = x^3 - x - 2",
        "fx": "x**3 - x - 2",
        "dfx": "3*x**2 - 1",
        "gx": "(x + 2)**(1/3)",
        "x0": "1", "x1": "2", "a": "1", "b": "2", "tol": "1e-5"
    },
    {
        "nama": "Soal 3: f(x) = x^2 - 4",
        "fx": "x**2 - 4",
        "dfx": "2*x",
        "gx": "np.sqrt(4)",
        "x0": "1", "x1": "3", "a": "1", "b": "3", "tol": "1e-5"
    }
]

def pilih_soal(event=None):
    idx = soal_combobox.current()
    if idx >= 0:
        entry_fx.delete(0, tk.END)
        entry_fx.insert(0, soal_list[idx]["fx"])
        entry_dfx.delete(0, tk.END)
        entry_dfx.insert(0, soal_list[idx]["dfx"])
        entry_gx.delete(0, tk.END)
        entry_gx.insert(0, soal_list[idx]["gx"])
        # Set parameter input otomatis
        entry_x0.delete(0, tk.END)
        entry_x0.insert(0, soal_list[idx]["x0"])
        entry_x1.delete(0, tk.END)
        entry_x1.insert(0, soal_list[idx]["x1"])
        entry_a.delete(0, tk.END)
        entry_a.insert(0, soal_list[idx]["a"])
        entry_b.delete(0, tk.END)
        entry_b.insert(0, soal_list[idx]["b"])
        entry_tol.delete(0, tk.END)
        entry_tol.insert(0, soal_list[idx]["tol"])

# Tambahkan Combobox untuk memilih soal
tk.Label(fungsi_frame, text="Pilih Soal:", font=("Segoe UI", 10), bg="#f6f6fa").grid(row=0, column=2, sticky="e", padx=(20,2))
soal_combobox = ttk.Combobox(fungsi_frame, values=[s["nama"] for s in soal_list], state="readonly", width=30, font=("Segoe UI", 10))
soal_combobox.grid(row=0, column=3, padx=5, pady=2)
soal_combobox.bind("<<ComboboxSelected>>", pilih_soal)
soal_combobox.current(0)
pilih_soal()

# Output Frame
output_frame = tk.Frame(root, bg="#f6f6fa")
output_frame.pack(padx=15, pady=(0, 15), fill="both", expand=True)

tk.Label(output_frame, text="Hasil Iterasi dan Akar:", font=("Segoe UI", 11, "bold"), bg="#f6f6fa", fg="#222f3e").pack(anchor="w", padx=2, pady=(5, 0))
output = tk.Text(output_frame, width=80, height=18, font=("Consolas", 10), bg="#f8f9fa", fg="#222f3e", borderwidth=2, relief="groove")
output.pack(padx=2, pady=5, fill="both", expand=True)
output.config(state='disabled')

root.mainloop()