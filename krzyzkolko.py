import tkinter as tk

# --- 1. ZMIENNE GRY ---
# Zaczyna gracz "X"
aktualny_gracz = "X"

# Licznik ruchów – jeśli dojdzie do 9 i nikt nie wygra, mamy remis!
ruchy = 0

# Lista, w której będziemy trzymać nasze 9 przycisków, żeby mieć do nich dostęp
przyciski = []


# --- 2. LOGIKA GRY ---

def sprawdz_wygrana():
    """Funkcja sprawdza wszystkie 8 możliwych kombinacji wygranej"""
    # Pobieramy teksty z przycisków (od 0 do 8)
    t = [p.cget("text") for p in przyciski]
    
    # Wszystkie linie zwycięstwa (poziomo, pionowo, skosy)
    kombinacje = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Poziomo
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Pionowo
        [0, 4, 8], [2, 4, 6]             # Skosy
    ]
    
    for kombinacja in kombinacje:
        # Jeśli trzy przyciski w linii mają ten sam znak i nie są puste
        if t[kombinacja[0]] == t[kombinacja[1]] == t[kombinacja[2]] != "":
            return True
    return False


def klikniecie(indeks):
    global aktualny_gracz, ruchy
    
    # Pobieramy przycisk, który został kliknięty
    przycisk = przyciski[indeks]
    
    # Jeśli przycisk jest już zajęty, nic nie rób
    if przycisk.cget("text") != "":
        return
        
    # Wpisujemy znak gracza i zmieniamy mu kolor dla lepszego wyglądu
    przycisk.config(text=aktualny_gracz)
    if aktualny_gracz == "X":
        przycisk.config(fg="blue")
    else:
        przycisk.config(fg="red")
        
    ruchy += 1
    
    # 1. Sprawdzamy czy ten ruch przyniósł wygraną
    if sprawdz_wygrana():
        etykieta_status.config(text=f"Wygrywa gracz: {aktualny_gracz}! 🎉", fg="green")
        zablokuj_plansze()
        return
        
    # 2. Sprawdzamy czy jest remis
    if ruchy == 9:
        etykieta_status.config(text="Remis! 🤝", fg="orange")
        return
        
    # 3. Zmiana gracza na następną turę
    if aktualny_gracz == "X":
        aktualny_gracz = "O"
    else:
        aktualny_gracz = "X"
        
    etykieta_status.config(text=f"Tura gracza: {aktualny_gracz}", fg="black")


def zablokuj_plansze():
    """Wyłącza wszystkie przyciski po zakończeniu gry"""
    for p in przyciski:
        p.config(state="disabled")


def resetuj_gre():
    global aktualny_gracz, ruchy
    aktualny_gracz = "X"
    ruchy = 0
    etykieta_status.config(text="Tura gracza: X", fg="black")
    for p in przyciski:
        p.config(text="", state="normal", bg="lightgray")


# --- 3. TWORZENIE INTERFEJSU (GUI) ---

root = tk.Tk()
root.title("Kółko i Krzyżyk")
root.geometry("320x420")

# Pasek statusu na samej górze
etykieta_status = tk.Label(root, text="Tura gracza: X", font=("Arial", 14, "bold"))
etykieta_status.pack(pady=10)

# Ramka (Frame), która będzie trzymać naszą siatkę 3x3
ramka_planszy = tk.Frame(root)
ramka_planszy.pack()

# Pętla, która automatycznie tworzy 9 przycisków i układa je w siatce .grid()
for i in range(9):
    # Tworzymy przycisk. Zwróć uwagę na command=lambda! Pozwala ona przekazać numer przycisku do funkcji.
    p = tk.Button(ramka_planszy, text="", font=("Arial", 20, "bold"), width=5, height=2, bg="lightgray",
                  command=lambda idx=i: klikniecie(idx))
    
    # Obliczamy wiersz (row) i kolumnę (column) na podstawie numeru od 0 do 8
    wiersz = i // 3
    kolumna = i % 3
    
    # Umieszczamy przycisk w ramce
    p.grid(row=wiersz, column=kolumna, padx=3, pady=3)
    
    # Dodajemy przycisk do naszej listy, żeby móc potem czytać jego tekst
    przyciski.append(p)

# Przycisk restartu na samym dole
przycisk_reset = tk.Button(root, text="Zagraj ponowie", font=("Arial", 10, "bold"), bg="#e0e0e0", command=resetuj_gre)
przycisk_reset.pack(pady=15)

root.mainloop()