import tkinter as tk
import random
from collections import Counter

# --- 1. ZMIENNE GRY ---
money = 1000
koszt_rzutu = 100

# --- 2. LOGIKA SPRAWDZANIA UKŁADÓW ---

def sprawdz_uklad(kosci):
    """Funkcja analizuje 5 wylosowanych kości i zwraca nazwę układu oraz mnożnik wygranej"""
    licznik = Counter(kosci)  # Liczy ile razy wypadła każda cyfra (np. {6: 3, 2: 2})
    wartosci = sorted(licznik.values(), reverse=True) # Pobiera same ilości (np. [3, 2])
    unikalne = sorted(list(set(kosci))) # Potrzebne do sprawdzenia strita

    # 1. Poker (5 takich samych) -> Mnożnik x10
    if wartosci == [5]:
        return "POKER (5 takich samych!)", 10

    # 2. Kareta (4 takie same) -> Mnożnik x5
    if wartosci == [4, 1]:
        return "KARETA (4 takie same)", 5

    # 3. Full (3 takie same + para) -> Mnożnik x4
    if wartosci == [3, 2]:
        return "FULL (Trójka + Para)", 4

    # 4. Strit (5 kolejnych liczb, np. 1,2,3,4,5 lub 2,3,4,5,6) -> Mnożnik x3
    if unikalne == [1, 2, 3, 4, 5] or unikalne == [2, 3, 4, 5, 6]:
        return "STRIT (Ciąg liczb)", 3

    # 5. Trójka (3 takie same) -> Mnożnik x2
    if wartosci[0] == 3:
        return "TRÓJKA", 2

    # 6. Dwie pary -> Mnożnik x1.5
    if wartosci == [2, 2, 1]:
        return "DWIE PARY", 1.5

    # 7. Para -> Zwrot kosztów x1
    if wartosci[0] == 2:
        return "PARA (Zwrot stawki)", 1

    # 8. Nic -> Mnożnik 0
    return "Nic (Brak układu)", 0


def rzuc_koscmi():
    global money
    
    # Sprawdzamy, czy gracz ma kasę na rzut
    if money < koszt_rzutu:
        etykieta_status.config(text="BRAK ŚRODKÓW! Jesteś bankrutem.", fg="darkred")
        return

    # Pobieramy zakład
    money -= koszt_rzutu
    
    # LOSOWANIE: Losujemy 5 kości (każda od 1 do 6)
    wyniki = [random.randint(1, 6) for _ in range(5)]
    
    # Wyświetlamy wylosowane kości na ekranie
    etykieta_kosci.config(text=f"🎲  {wyniki[0]}  |  {wyniki[1]}  |  {wyniki[2]}  |  {wyniki[3]}  |  {wyniki[4]}  🎲")
    
    # Sprawdzamy co wypadło
    nazwa_ukladu, mnoznik = sprawdz_uklad(wyniki)
    
    # Obliczamy wygraną
    wygrana = int(koszt_rzutu * mnoznik)
    money += wygrana
    
    # Aktualizacja interfejsu
    etykieta_pieniadze.config(text=f"Stan konta: {money} zł")
    
    if wygrana > 0:
        etykieta_status.config(text=f"Trafiłeś: {nazwa_ukladu}!\nWygrana: +{wygrana} zł!", fg="green")
    else:
        etykieta_status.config(text=f"Trafiłeś: {nazwa_ukladu}.\nTracisz {koszt_rzutu} zł.", fg="red")


# --- 3. TWORZENIE OKNA GUI ---

root = tk.Tk()
root.title("Kościany Poker - Kasyno")
root.geometry("400x380")

# Stan konta
etykieta_pieniadze = tk.Label(root, text=f"Stan konta: {money} zł", font=("Arial", 14, "bold"), fg="blue")
etykieta_pieniadze.pack(pady=15)

# Koszt gry
etykieta_info = tk.Label(root, text=f"Koszt jednego rzutu: {koszt_rzutu} zł", font=("Arial", 10, "italic"), fg="gray")
etykieta_info.pack()

# WIELKI WYŚWIETLACZ KOŚCI
etykieta_kosci = tk.Label(root, text="🎲  ?  |  ?  |  ?  |  ?  |  ?  🎲", font=("Arial", 22, "bold"), bg="#e0e0e0", width=20, bd=3, relief="sunken")
etykieta_kosci.pack(pady=25)

# Przycisk rzutu
przycisk_rzut = tk.Button(root, text="RZUĆ KOŚĆMI!", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=18, height=2, command=rzuc_koscmi)
przycisk_rzut.pack(pady=10)

# Status wyniku
etykieta_status = tk.Label(root, text="Zagraj, aby sprawdzić swoje szczęście!", font=("Arial", 11, "bold"), justify="center")
etykieta_status.pack(pady=15)

root.mainloop()     