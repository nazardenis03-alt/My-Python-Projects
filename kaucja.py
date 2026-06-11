import tkinter as tk
from tkinter import messagebox

# --- LOGIKA BUTELKOMATU ---
CENA_PLASTIK = 0.50
CENA_SZKLO = 1.00
CENA_PUSZKA = 0.50
MAX_POJEMNOSC = 65

sztuk_plastik = 0
sztuk_szklo = 0
sztuk_puszka = 0
suma_kaucji = 0.0

# --- LOGIKA SKLEPU ---
# Lista 10 produktów: (Nazwa, Cena)
PRODUKTY = [
    ("Chleb", 4.50), ("Mleko", 3.20), ("Czekolada", 5.00), 
    ("Sok pomarańczowy", 6.00), ("Woda mineralna", 2.00),
    ("Chipsy", 5.50), ("Batonik", 2.50), ("Ser żółty", 8.00),
    ("Jabłko (1kg)", 4.00), ("Lody", 3.50)
]
zakupione_produkty = []

def dodaj_opakowanie(rodzaj):
    global sztuk_plastik, sztuk_szklo, sztuk_puszka, suma_kaucji
    
    # Sprawdzenie limitu 65 butelek
    lacznie_butelek = sztuk_plastik + sztuk_szklo + sztuk_puszka
    if lacznie_butelek >= MAX_POJEMNOSC:
        messagebox.showwarning("Automat Pełny", "Osiągnięto maksymalną pojemność (65 sztuk)! Wydrukuj paragon.")
        return
    
    if rodzaj == "plastik":
        sztuk_plastik += 1
        suma_kaucji += CENA_PLASTIK
    elif rodzaj == "szklo":
        sztuk_szklo += 1
        suma_kaucji += CENA_SZKLO
    elif rodzaj == "puszka":
        sztuk_puszka += 1
        suma_kaucji += CENA_PUSZKA
        
    odswiez_ekran()

def odswiez_ekran():
    lacznie = sztuk_plastik + sztuk_szklo + sztuk_puszka
    label_plastik.config(text=f"Plastikowe: {sztuk_plastik} szt.")
    label_szklo.config(text=f"Szklane: {sztuk_szklo} szt.")
    label_puszka.config(text=f"Puszki: {sztuk_puszka} szt.")
    label_suma.config(text=f"{suma_kaucji:.2f} PLN")
    label_pojemnosc.config(text=f"Pojemność: {lacznie}/{MAX_POJEMNOSC}")

def drukuj_paragon():
    global suma_kaucji
    if suma_kaucji == 0:
        messagebox.showinfo("Butelkomat", "Automat jest pusty! Wrzuć coś najpierw.")
        return
        
    tekst_paragonu = (
        "=== PARAGON KAUCYJNY ===\n\n"
        f"Butelki plastikowe: {sztuk_plastik}\n"
        f"Butelki szklane: {sztuk_szklo}\n"
        f"Puszki aluminiowe: {sztuk_puszka}\n"
        "-----------------------\n"
        f"RAZEM DO WYKORZYSTANIA: {suma_kaucji:.2f} PLN\n\n"
        "Zapraszamy do kasy!"
    )
    messagebox.showinfo("Wydruk paragonu", tekst_paragonu)
    
    # Zamykamy okno butelkomatu i otwieramy okno Kasy
    root.destroy()
    otworz_kase(suma_kaucji)

# --- OKNO KASY SKLEPOWEJ ---
def otworz_kase(pieniadze_z_kaucji):
    global kasa_root, stan_konta, label_portfel
    stan_konta = pieniadze_z_kaucji

    kasa_root = tk.Tk()
    kasa_root.title("Kasa Sklepowa")
    kasa_root.geometry("500x400")
    kasa_root.configure(bg="#ecf0f1", padx=20, pady=20)

    tk.Label(kasa_root, text="KASA - Wybierz co chcesz zrobić", font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=10)
    
    label_portfel = tk.Label(kasa_root, text=f"Środki z kaucji: {stan_konta:.2f} PLN", font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#e74c3c")
    label_portfel.pack(pady=5)

    # Główne opcje kasy
    btn_wyplata = tk.Button(kasa_root, text="💵 WYPŁAĆ GOTÓWKĘ", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", width=25, height=2, command=wyplac_gotowke)
    btn_wyplata.pack(pady=10)

    btn_zakupy = tk.Button(kasa_root, text="🛒 KUP PRODUKTY (10 do wyboru)", font=("Arial", 11, "bold"), bg="#3498db", fg="white", width=25, height=2, command=pokaz_produkty)
    btn_zakupy.pack(pady=10)

def wyplac_gotowke():
    global stan_konta
    podsumowanie = (
        "=== PODSUMOWANIE TRANSAKCJI ===\n\n"
        f"Pobrano gotówkę: {stan_konta:.2f} PLN\n"
        f"Kupione produkty: {', '.join(zakupione_produkty) if zakupione_produkty else 'Brak'}\n\n"
        "Dziękujemy za skorzystanie z EkoMatu!"
    )
    messagebox.showinfo("Koniec", podsumowanie)
    kasa_root.destroy()

# --- OKNO ZAKUPÓW (10 PRODUKTÓW) ---
def pokaz_produkty():
    okno_sklep = tk.Toplevel(kasa_root)
    okno_sklep.title("Wybierz produkty")
    okno_sklep.geometry("400x500")
    okno_sklep.configure(bg="#ffffff", padx=10, pady=10)

    tk.Label(okno_sklep, text="Kliknij produkt, aby go kupić:", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=10)

    # Generowanie przycisku dla każdego z 10 produktów
    for nazwa, cena in PRODUKTY:
        btn_prod = tk.Button(
            okno_sklep, 
            text=f"{nazwa} - {cena:.2f} zł", 
            font=("Arial", 10),
            bg="#f1f2f6",
            anchor="w",
            padx=10,
            command=lambda n=nazwa, c=cena: kup_produkt(n, c)
        )
        btn_prod.pack(fill="x", pady=2)

    # Przycisk powrotu
    tk.Button(okno_sklep, text="Powrót do menu kasy", bg="#7f8c8d", fg="white", command=okno_sklep.destroy).pack(pady=15)

def kup_produkt(nazwa, cena):
    global stan_konta
    if stan_konta >= cena:
        stan_konta -= cena
        zakupione_produkty.append(nazwa)  # Poprawione dodawanie do listy
        label_portfel.config(text=f"Środki z kaucji: {stan_konta:.2f} PLN")
        messagebox.showinfo("Koszyk", f"Kupiono: {nazwa}! Zostało: {stan_konta:.2f} PLN")
    else:
        messagebox.showerror("Brak środków", f"Masz za mało pieniędzy na: {nazwa}!")


# --- INICJALIZACJA INTERFEJSU BUTELKOMATU ---
root = tk.Tk()
root.title("EkoMat - Butelkomat")
root.geometry("500x380")
root.configure(bg="#f0f3f4", padx=20, pady=20)

label_tytul = tk.Label(root, text="Zwróć opakowania, odbierz kaucję!", font=("Arial", 14, "bold"), bg="#f0f3f4", fg="#27ae60")
label_tytul.grid(row=0, column=0, columnspan=2, pady=10)

frame_przyciski = tk.LabelFrame(root, text=" Wrzuć opakowanie ", font=("Arial", 10, "bold"), padx=10, pady=10, bg="#f0f3f4")
frame_przyciski.grid(row=1, column=0, sticky="ns", padx=10)

btn_plastik = tk.Button(frame_przyciski, text="♴ Butelka Plastik (50 gr)", width=22, bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=lambda: dodaj_opakowanie("plastik"))
btn_plastik.pack(pady=5)

btn_szklo = tk.Button(frame_przyciski, text="🍾 Butelka Szkło (1 zł)", width=22, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=lambda: dodaj_opakowanie("szklo"))
btn_szklo.pack(pady=5)

btn_puszka = tk.Button(frame_przyciski, text="🥫 Puszka (50 gr)", width=22, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), command=lambda: dodaj_opakowanie("puszka"))
btn_puszka.pack(pady=5)

frame_ekran = tk.LabelFrame(root, text=" Status sesji ", font=("Arial", 10, "bold"), padx=15, pady=10, bg="#2c3e50", fg="white")
frame_ekran.grid(row=1, column=1, sticky="nsew", padx=10)

label_plastik = tk.Label(frame_ekran, text="Plastikowe: 0 szt.", font=("Arial", 11), bg="#2c3e50", fg="white")
label_plastik.pack(anchor="w", pady=2)

label_szklo = tk.Label(frame_ekran, text="Szklane: 0 szt.", font=("Arial", 11), bg="#2c3e50", fg="white")
label_szklo.pack(anchor="w", pady=2)

label_puszka = tk.Label(frame_ekran, text="Puszki: 0 szt.", font=("Arial", 11), bg="#2c3e50", fg="white")
label_puszka.pack(anchor="w", pady=2)

label_pojemnosc = tk.Label(frame_ekran, text="Pojemność: 0/65", font=("Arial", 10, "italic"), bg="#2c3e50", fg="#bdc3c7")
label_pojemnosc.pack(anchor="w", pady=5)

tk.Label(frame_ekran, text="DO WYPŁATY:", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#2ecc71").pack(pady=(5, 0))
label_suma = tk.Label(frame_ekran, text="0.00 PLN", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#2ecc71")
label_suma.pack()

btn_koniec = tk.Button(root, text="🔴 KONIEC / DRUKUJ PARAGON", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", command=drukuj_paragon)
btn_koniec.grid(row=2, column=0, columnspan=2, pady=20, sticky="we")

root.grid_columnconfigure(1, weight=1)
root.mainloop()