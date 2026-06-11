import tkinter as tk

# --- 1. ZMIENNE GRY ---
monety = 0
monety_per_klik = 1  # Ile dostajemy za jedno kliknięcie

cena_boosta_1 = 50   # Koszt pierwszego ulepszenia (+1 do kliknięcia)
cena_boosta_2 = 200  # Koszt drugiego ulepszenia (+5 do kliknięcia)


# --- 2. LOGIKA I FUNKCJE ---

def kliknij():
    global monety
    # Dodajemy do naszego konta tyle, ile wynosi aktualna siła kliknięcia
    monety += monety_per_klik
    # Aktualizujemy stan konta na ekranie
    etykieta_monety.config(text=f"Monety: {monety}")
    etykieta_status.config(text="Klik! +Kasa", fg="green")


def kup_boost_1():
    global monety, monety_per_klik, cena_boosta_1
    
    if monety >= cena_boosta_1:
        monety -= cena_boosta_1       # Zabieramy monety
        monety_per_klik += 1          # Zwiększamy siłę kliknięcia o 1
        cena_boosta_1 = int(cena_boosta_1 * 1.5)  # Następny boost jest droższy!
        
        # Aktualizujemy wszystko na ekranie
        etykieta_monety.config(text=f"Monety: {monety}")
        przycisk_boost1.config(text=f"Drobny Wydatek (+1/klik)\nKoszt: {cena_boosta_1} monet")
        etykieta_status.config(text="Kupiono ulepszenie +1!", fg="blue")
    else:
        etykieta_status.config(text="Masz za mało monet!", fg="red")


def kup_boost_2():
    global monety, monety_per_klik, cena_boosta_2
    
    if monety >= cena_boosta_2:
        monety -= cena_boosta_2       # Zabieramy monety
        monety_per_klik += 5          # Zwiększamy siłę kliknięcia aż o 5!
        cena_boosta_2 = int(cena_boosta_2 * 1.6)  # Zwiększamy cenę
        
        # Aktualizujemy ekran
        etykieta_monety.config(text=f"Monety: {monety}")
        przycisk_boost2.config(text=f"Super Inwestycja (+5/klik)\nKoszt: {cena_boosta_2} monet")
        etykieta_status.config(text="Kupiono super ulepszenie +5!", fg="purple")
    else:
        etykieta_status.config(text="Masz za mało monet!", fg="red")


# --- 3. TWORZENIE OKNA GUI ---

root = tk.Tk()
root.title("Mój Clicker")
root.geometry("350x450")
root.config(bg="#FFFFFF") # Jasnoszare tło okna

# Wyświetlacz monet
etykieta_monety = tk.Label(root, text=f"Monety: {monety}", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333")
etykieta_monety.pack(pady=20)

# GŁÓWNY PRZYCISK DO KLIKANIA
przycisk_klik = tk.Button(root, text="KLIKAJ TUTAJ!", font=("Arial", 14, "bold"), width=18, height=3, bg="#4CAF50", fg="white", activebackground="#45a049", command=kliknij)
przycisk_klik.pack(pady=10)

# Pasek statusu
etykieta_status = tk.Label(root, text="Zacznij klikać!", font=("Arial", 11, "italic"), bg="#f0f0f0", fg="gray")
etykieta_status.pack(pady=10)

# Sekcja ulepszeń (Sklep)
etykieta_sklep = tk.Label(root, text="--- SKLEP Z ULEPSZENIAMI ---", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="gray")
etykieta_sklep.pack(pady=15)

# Przycisk Boosta 1
przycisk_boost1 = tk.Button(root, text=f"Drobny Wydatek (+1/klik)\nKoszt: {cena_boosta_1} monet", font=("Arial", 10), width=28, bg="#e0e0e0", command=kup_boost_1)
przycisk_boost1.pack(pady=5)

# Przycisk Boosta 2
przycisk_boost2 = tk.Button(root, text=f"Super Inwestycja (+5/klik)\nKoszt: {cena_boosta_2} monet", font=("Arial", 10), width=28, bg="#e0e0e0", command=kup_boost_2)
przycisk_boost2.pack(pady=5)

root.mainloop()