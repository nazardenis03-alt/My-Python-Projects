import tkinter as tk
import random 

# --- 1. USTAWIENIA POCZĄTKOWE GRY ---
wyslosowana_liczba = random.randint(1, 30)
money = 500
proby = 0 
max_proby = 5

# --- 2. LOGIKA GRY ---
def sprawdz_strzal():
    global proby, money

    # Zabezpieczenie przed klikaniem po końcu gry
    if proby >= max_proby or money == 0 or etykieta_informacja.cget("text").startswith("Brawo"):
        return

    try:
        strzal = int(pole_wpisywania.get())

        # Warunek 1: Trafienie
        if strzal == wyslosowana_liczba:
            money *= 2
            etykieta_informacja.config(text="Brawo! Zgadłeś!", fg="green")
            etykieta_pieniadze.config(text=f"Stan konta: {money} zł", fg="green")
            return

        # Jeśli pudło, dodajemy próbę
        proby += 1

        # Warunek 2: Przegrana (koniec prób)
        if proby >= max_proby:
            money = 0
            etykieta_informacja.config(text=f"Przegrałeś! Liczba to: {wyslosowana_liczba}", fg="darkred")
            etykieta_licznik.config(text="Koniec prób!")
            etykieta_pieniadze.config(text=f"Stan konta: {money} zł", fg="red")
            return

        # Warunek 3: Podpowiedź za dużo / za mało
        if strzal < wyslosowana_liczba:
            etykieta_informacja.config(text="Za mało!", fg="orange")
        else:
            etykieta_informacja.config(text="Za dużo!", fg="orange")

        # Aktualizacja licznika prób na ekranie
        etykieta_licznik.config(text=f"Zostało prób: {max_proby - proby}")

    except ValueError:
        etykieta_informacja.config(text="Wpisz poprawną liczbę cyframi!", fg="red")


# --- 3. TWORZENIE OKNA GUI ---
root = tk.Tk()
root.title("Sklepik z grami 2.0")
root.geometry("350x320")

napis_powitalny = tk.Label(root, text="Witaj w sklepie z grami!", font=("Arial", 12, "bold"))
napis_powitalny.pack(pady=5)

napis_zasady = tk.Label(root, text="Zgadnij liczbę od 1 do 30.\nMasz 5 prób albo tracisz kasę!", font=("Arial", 9), fg="gray")
napis_zasady.pack(pady=5)

etykieta_pieniadze = tk.Label(root, text=f"Stan konta: {money} zł", font=("Arial", 11, "bold"), fg="blue")
etykieta_pieniadze.pack(pady=10)

pole_wpisywania = tk.Entry(root, font=("Arial", 12), justify="center", width=10)
pole_wpisywania.pack(pady=5)

przycisk_sprawdz = tk.Button(root, text="Obstawiam!", font=("Arial", 10, "bold"), command=sprawdz_strzal)
przycisk_sprawdz.pack(pady=5)

etykieta_informacja = tk.Label(root, text="Powodzenia!", font=("Arial", 11, "bold"))
etykieta_informacja.pack(pady=10)

etykieta_licznik = tk.Label(root, text=f"Zostało prób: {max_proby}", font=("Arial", 10))
etykieta_licznik.pack(pady=5)

root.mainloop()