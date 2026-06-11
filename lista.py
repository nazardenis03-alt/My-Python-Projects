import tkinter as tk

lista = []

try:
    with open("plik.txt", "r", encoding="utf-8") as plik:
        for linia in plik:
            lista.append(linia.strip())
except FileNotFoundError:
    pass


def odswiez_okno_listy():
    """Pomocnicza funkcja, która czyści widget Listbox i wpisuje do niego zadania na nowo"""
    okno_listy.delete(0, tk.END)  
    for zadanie in lista:
        okno_listy.insert(tk.END, zadanie)  


def dodaj_zadanie():
    zadanie = pole_wpisywania.get().strip()
    
    if zadanie != "":  
        lista.append(zadanie)
        
        with open("plik.txt", "a", encoding="utf-8") as plik:
            plik.write(zadanie + "\n")
            
        pole_wpisywania.delete(0, tk.END)  
        odswiez_okno_listy()  
        etykieta_status.config(text="Dodano zadanie!", fg="green")
    else:
        etykieta_status.config(text="BŁĄD: Zadanie nie może być puste!", fg="orange")


def usun_zadanie():
    try:
        
        zaznaczony_indeks = okno_listy.curselection()[0]
        
        lista.pop(zaznaczony_indeks)
        
        with open("plik.txt", "w", encoding="utf-8") as plik:
            for zadanie in lista:
                plik.write(zadanie + "\n")
                
        odswiez_okno_listy()  
        etykieta_status.config(text="Usunięto zadanie!", fg="red")
        
    except IndexError:
        
        etykieta_status.config(text="BŁĄD: Zaznacz zadanie z listy, aby je usunąć!", fg="orange")



root = tk.Tk()
root.title("Moja Lista Zadań GUI")
root.geometry("400x450")

instrukcja = tk.Label(root, text="Wpisz nowe zadanie:", font=("Arial", 11))
instrukcja.pack(pady=5)

pole_wpisywania = tk.Entry(root, font=("Arial", 12), width=35)
pole_wpisywania.pack(pady=5)

przycisk_dodaj = tk.Button(root, text="Dodaj zadanie", font=("Arial", 10, "bold"), bg="lightgreen", command=dodaj_zadanie)
przycisk_dodaj.pack(pady=5)

etykieta_twoje_zadania = tk.Label(root, text="Twoje zadania (kliknij zadanie, aby je wybrać):", font=("Arial", 11))
etykieta_twoje_zadania.pack(pady=10)

okno_listy = tk.Listbox(root, font=("Arial", 11), width=35, height=10)
okno_listy.pack(pady=5)

przycisk_usun = tk.Button(root, text="Usuń zaznaczone zadanie", font=("Arial", 10, "bold"), bg="salmon", command=usun_zadanie)
przycisk_usun.pack(pady=5)

etykieta_status = tk.Label(root, text="Program gotowy", font=("Arial", 10, "italic"), fg="gray")
etykieta_status.pack(pady=10)

odswiez_okno_listy()

root.mainloop()