import tkinter as tk
import random


wylosowana_liczba = random.randint(1, 50)

def sprawdz_strzal():
    
    tekst_uzytkownika = pole_wpisywania.get()
    
    try:
        
        strzal = int(tekst_uzytkownika)
        
        if strzal == wylosowana_liczba:
            etykieta_informacja.config(text="GRATULACJE! Trafiłeś!", fg="green")
        elif strzal > wylosowana_liczba:
            etykieta_informacja.config(text="ZA DUŻO!", fg="red")
        else:
            etykieta_informacja.config(text="ZA MAŁO!", fg="red")
            
    except ValueError:
        
        etykieta_informacja.config(text="BŁĄD: Wpisz liczbę cyframi!", fg="orange")




okno = tk.Tk()
okno.title("MEGA ZGADYWANKA 2.0 - GUI")
okno.geometry("400x250")

instrukcja = tk.Label(okno, text="Podaj liczbę od 1 do 50:", font=("Arial", 12))

instrukcja.pack(pady=10)
pole_wpisywania = tk.Entry(okno, font=("Arial", 14), justify="center")
pole_wpisywania.pack(pady=10)

przycisk = tk.Button(okno, text="Sprawdź!", font=("Arial", 12), command=sprawdz_strzal)
przycisk.pack(pady=10)

etykieta_informacja = tk.Label(okno, text="Powodzenia!", font=("Arial", 12, "bold"))
etykieta_informacja.pack(pady=15)

okno.mainloop()
        
        
        
        
    


