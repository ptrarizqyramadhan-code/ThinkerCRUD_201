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
