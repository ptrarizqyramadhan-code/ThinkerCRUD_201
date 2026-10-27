import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "nilai_siswa.db"

# ---------- DATABASE ----------
def buat_tabel():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi REAL NOT NULL,
            fisika REAL NOT NULL,
            inggris REAL NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def simpan_ke_db(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
        "VALUES (?, ?, ?, ?, ?)",
        (nama, biologi, fisika, inggris, prediksi),
    )
    conn.commit()
    conn.close()

def ambil_semua_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas "
        "FROM nilai_siswa ORDER BY id DESC"
    )
    hasil = cur.fetchall()
    conn.close()
    return hasil

# ---------- LOGIKA PREDIKSI ----------
def tentukan_prediksi(biologi, fisika, inggris):
    nilai_tertinggi = max(biologi, fisika, inggris)
    hasil = []
    if biologi == nilai_tertinggi:
        hasil.append("Kedokteran")
    if fisika == nilai_tertinggi:
        hasil.append("Teknik")
    if inggris == nilai_tertinggi:
        hasil.append("Bahasa")
    # Jika ada nilai tertinggi yang sama, tampilkan semuanya
    return " / ".join(hasil)

# ---------- GUI ----------
def submit_nilai():
    nama = entry_nama.get().strip()

    if not nama:
        messagebox.showwarning("Peringatan", "Nama siswa harus diisi!")
        return

    try:
        biologi = float(entry_biologi.get())
        fisika = float(entry_fisika.get())
        inggris = float(entry_inggris.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    for n in (biologi, fisika, inggris):
        if n < 0 or n > 100:
            messagebox.showerror("Error", "Nilai harus antara 0 sampai 100!")
            return

    prediksi = tentukan_prediksi(biologi, fisika, inggris)
    simpan_ke_db(nama, biologi, fisika, inggris, prediksi)

    label_hasil.config(text=f"Prediksi Fakultas: {prediksi}")
    messagebox.showinfo("Berhasil", f"Data {nama} tersimpan.\nPrediksi: {prediksi}")

    for e in (entry_nama, entry_biologi, entry_fisika, entry_inggris):
        e.delete(0, tk.END)
    entry_nama.focus()
    muat_tabel()

def muat_tabel():
    for item in tree.get_children():
        tree.delete(item)
    for baris in ambil_semua_data():
        tree.insert("", tk.END, values=baris)

buat_tabel()

root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("620x520")

frame_input = tk.Frame(root, padx=15, pady=15)
frame_input.pack(fill="x")

tk.Label(frame_input, text="Nama Siswa").grid(row=0, column=0, sticky="w", pady=4)
entry_nama = tk.Entry(frame_input, width=30)
entry_nama.grid(row=0, column=1, pady=4)

tk.Label(frame_input, text="Nilai Biologi").grid(row=1, column=0, sticky="w", pady=4)
entry_biologi = tk.Entry(frame_input, width=30)
entry_biologi.grid(row=1, column=1, pady=4)

tk.Label(frame_input, text="Nilai Fisika").grid(row=2, column=0, sticky="w", pady=4)
entry_fisika = tk.Entry(frame_input, width=30)
entry_fisika.grid(row=2, column=1, pady=4)

tk.Label(frame_input, text="Nilai Inggris").grid(row=3, column=0, sticky="w", pady=4)
entry_inggris = tk.Entry(frame_input, width=30)
entry_inggris.grid(row=3, column=1, pady=4)

btn_submit = tk.Button(frame_input, text="Submit Nilai", command=submit_nilai,
  bg="#2e7d32", fg="white", width=20)
btn_submit.grid(row=4, column=0, columnspan=2, pady=12)

label_hasil = tk.Label(root, text="Prediksi Fakultas: -", font=("Arial", 12, "bold"))
label_hasil.pack(pady=5)

# Tabel data tersimpan
kolom = ("Nama", "Biologi", "Fisika", "Inggris", "Prediksi")
tree = ttk.Treeview(root, columns=kolom, show="headings", height=10)
for k in kolom:
    tree.heading(k, text=k)
    tree.column(k, width=110, anchor="center")
tree.pack(padx=15, pady=10, fill="both", expand=True)

muat_tabel()
root.mainloop()