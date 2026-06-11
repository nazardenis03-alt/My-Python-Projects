import tkinter as tk
import random

wylosowany_kolor = random.choice(['czerwony', 'zielony', 'bialy', 'rozowy'])


proby = 5

root = tk.Tk()
root.title("Zgadywanie kolorów z licznikiem")
root.geometry("300x280")

etykieta_opcje = tk.Label(root, text="Dostępne kolory:\nczerwony, zielony, bialy, rozowy", font=("Arial", 10, "italic"), fg="gray")
etykieta_opcje.pack(pady=10)

pole_wypisywania = tk.Entry(root)
pole_wypisywania.pack(pady=5)

def sprawdz_strzal():
    
    global proby
    
    if proby <= 0:
        return

    strzal = pole_wypisywania.get().lower()
    
    if strzal == wylosowany_kolor:
        etykieta_informacja.config(text="TRAFIŁEŚ! Wygrałeś!", fg="green")
        
        proby = 0 
    else:
        
        proby -= 1
        
        if proby > 0:
            etykieta_informacja.config(text=f"NIE TRAFIŁEŚ!", fg="red")
            etykieta_licznik.config(text=f"Zostało prób: {proby}")
        else:
            etykieta_informacja.config(text=f"PRZEGRAŁEŚ! Kolor to: {wylosowany_kolor}", fg="darkred")
            etykieta_licznik.config(text="Koniec prób!")

przycisk = tk.Button(root, text="Sprawdź", command=sprawdz_strzal)
przycisk.pack(pady=5)

etykieta_informacja = tk.Label(root, text="Zgadnij kolor!", font=("Arial", 12))
etykieta_informacja.pack(pady=5)

etykieta_licznik = tk.Label(root, text=f"Zostało prób: {proby}", font=("Arial", 10, "bold"), fg="blue")
etykieta_licznik.pack(pady=5)

root.mainloop()


    
