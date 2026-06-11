import tkinter as tk
from tkinter import messagebox
import random
import math

# --- LOGIKA PROGRAMU ---

punkty = 0
seria = 0
aktualna_liczba1 = 0
aktualna_liczba2 = 0

def losuj_liczby():
    global aktualna_liczba1, aktualna_liczba2
    # Losowanie par z zakresu 100 - 1000
    aktualna_liczba1 = random.randint(100, 1000)
    aktualna_liczba2 = random.randint(100, 1000)
    
    # Aktualizacja napisów w GUI
    label_liczby.config(text=f"Liczby: {aktualna_liczba1} oraz {aktualna_liczba2}")
    
    # Czyszczenie pól tekstowych przed nową rundą
    entry_nwd.delete(0, tk.END)
    entry_nww.delete(0, tk.END)
    label_wynik.config(text="", fg="black")
    btn_sprawdz.config(text="Sprawdź", command=sprawdz_odpowiedz)

def sprawdz_odpowiedz():
    global punkty, seria
    
    # Pobranie odpowiedzi od użytkownika i obsługa błędu (np. gdy pole jest puste)
    try:
        user_nwd = int(entry_nwd.get().strip())
        user_nww = int(entry_nww.get().strip())
    except ValueError:
        label_wynik.config(text="Wpisz poprawne liczby w oba pola!", fg="orange")
        return

    # Obliczenie poprawnych odpowiedzi przez komputer
    poprawne_nwd = math.gcd(aktualna_liczba1, aktualna_liczba2)
    poprawne_nww = math.lcm(aktualna_liczba1, aktualna_liczba2)

    # Sprawdzenie warunku: czy użytkownik podał dobre wyniki
    if user_nwd == poprawne_nwd and user_nww == poprawne_nww:
        punkty += 1
        seria += 1
        label_wynik.config(text="Genialnie! Obie odpowiedzi są poprawne. +1 pkt", fg="#2ecc71")
    else:
        seria = 0  # Reset serii po błędzie
        label_wynik.config(
            text=f"Źle! Poprawne wyniki to:\nNWD = {poprawne_nwd} | NWW = {poprawne_nww}", 
            fg="#e74c3c"
        )
    
    # Aktualizacja licznika punktów na ekranie
    label_punkty.config(text=f"Punkty: {punkty}  |  Seria: {seria}")
    
    # Zmiana działania przycisku na losowanie kolejnej pary liczb
    btn_sprawdz.config(text="Następne liczby", command=losuj_liczby)


# --- TWORZENIE GUI ---

root = tk.Tk()
root.title("Trener Matmy: NWD i NWW")
root.geometry("420x380")
root.configure(padx=20, pady=20)

# Licznik punktów
label_punkty = tk.Label(root, text="Punkty: 0  |  Seria: 0", font=("Arial", 12, "bold"))
label_punkty.grid(row=0, column=0, columnspan=2, pady=10)

# Wylosowane liczby
label_liczby = tk.Label(root, text="Liczby: ...", font=("Arial", 16, "bold"), fg="#2c3e50")
label_liczby.grid(row=1, column=0, columnspan=2, pady=15)

# Pole NWD
tk.Label(root, text="Podaj NWD:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=5)
entry_nwd = tk.Entry(root, font=("Arial", 11), width=12)
entry_nwd.grid(row=2, column=1, sticky="w", pady=5)

# Pole NWW
tk.Label(root, text="Podaj NWW:", font=("Arial", 11)).grid(row=3, column=0, sticky="e", pady=5)
entry_nww = tk.Entry(root, font=("Arial", 11), width=12)
entry_nww.grid(row=3, column=1, sticky="w", pady=5)

# Przycisk akcji (Sprawdź / Następne)
btn_sprawdz = tk.Button(root, text="Sprawdź", font=("Arial", 11, "bold"), width=20, command=sprawdz_odpowiedz)
btn_sprawdz.grid(row=4, column=0, columnspan=2, pady=15)

# Komunikat o wyniku (zielony przy sukcesie, czerwony przy błędzie)
label_wynik = tk.Label(root, text="", font=("Arial", 11, "bold"), justify="center")
label_wynik.grid(row=5, column=0, columnspan=2, pady=5)

# Pierwsze automatyczne losowanie przy starcie programu
losuj_liczby()

root.mainloop()