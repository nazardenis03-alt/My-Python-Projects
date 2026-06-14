import tkinter as tk
from tkinter import messagebox

# Tworzymy KLASĘ, czyli szablon dla naszego programu
class ButelkomatApp:
    
    # Konstruktor - to tu definiujemy "startowe" dane obiektu. 
    # self oznacza: "mój własny, konkretny obiekt"
    def __init__(self, okno_glowne):
        self.root = okno_glowne
        self.root.title("EkoMat - Butelkomat Obiektowy")
        self.root.geometry("500x380")
        self.root.configure(bg="#f0f3f4", padx=20, pady=20)
        
        # --- CENY I LIMITY (teraz są własnością obiektu) ---
        self.CENA_PLASTIK = 0.50
        self.CENA_SZKLO = 1.00
        self.CENA_PUSZKA = 0.50
        self.MAX_POJEMNOSC = 65
        
        # --- LICZNIKI (zamiast zmiennych globalnych!) ---
        self.sztuk_plastik = 0
        self.sztuk_szklo = 0
        self.sztuk_puszka = 0
        self.suma_kaucji = 0.0
        
        # Przy uruchomieniu od razu budujemy interfejs
        self.stworz_interfejs()

    def stworz_interfejs(self):
        # Nagłówek
        label_tytul = tk.Label(self.root, text="Zwróć opakowania, odbierz kaucję!", font=("Arial", 14, "bold"), bg="#f0f3f4", fg="#27ae60")
        label_tytul.grid(row=0, column=0, columnspan=2, pady=10)

        # Panel przycisków (lewa strona)
        frame_przyciski = tk.LabelFrame(self.root, text=" Wrzuć opakowanie ", font=("Arial", 10, "bold"), padx=10, pady=10, bg="#f0f3f4")
        frame_przyciski.grid(row=1, column=0, sticky="ns", padx=10)

        # W klasie funkcje wywołujemy przez self.nazwa_funkcji
        tk.Button(frame_przyciski, text="♴ Butelka Plastik (50 gr)", width=22, bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                  command=lambda: self.dodaj_opakowanie("plastik")).pack(pady=5)

        tk.Button(frame_przyciski, text="🍾 Butelka Szkło (1 zł)", width=22, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                  command=lambda: self.dodaj_opakowanie("szklo")).pack(pady=5)

        tk.Button(frame_przyciski, text="🥫 Puszka (50 gr)", width=22, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), 
                  command=lambda: self.dodaj_opakowanie("puszka")).pack(pady=5)

        # Panel statusu (prawa strona)
        frame_ekran = tk.LabelFrame(self.root, text=" Status sesji ", font=("Arial", 10, "bold"), padx=15, pady=10, bg="#2c3e50", fg="white")
        frame_ekran.grid(row=1, column=1, sticky="nsew", padx=10)

        # Zapisujemy napisy jako zmienne obiektu (self.), żeby inne funkcje miały do nich dostęp
        self.label_plastik = tk.Label(frame_ekran, text="Plastikowe: 0 szt.", font=("Arial", 11), bg="#2c3e50", fg="white")
        self.label_plastik.pack(anchor="w", pady=2)

        self.label_szklo = tk.Label(frame_ekran, text="Szklane: 0 szt.", font=("Arial", 11), bg="#2c3e50", fg="white")
        self.label_szklo.pack(anchor="w", pady=2)

        self.label_puszka = tk.Label(frame_ekran, text="Puszki: 0 szt.", font=("Arial", 11), bg="#2c3e50", fg="white")
        self.label_puszka.pack(anchor="w", pady=2)

        self.label_pojemnosc = tk.Label(frame_ekran, text="Pojemność: 0/65", font=("Arial", 10, "italic"), bg="#2c3e50", fg="#bdc3c7")
        self.label_pojemnosc.pack(anchor="w", pady=5)

        tk.Label(frame_ekran, text="DO WYPŁATY:", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#2ecc71").pack(pady=(5, 0))
        self.label_suma = tk.Label(frame_ekran, text="0.00 PLN", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#2ecc71")
        self.label_suma.pack()

        # Przycisk dolny
        btn_koniec = tk.Button(self.root, text="🔴 KONIEC / DRUKUJ PARAGON", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", command=self.drukuj_paragon)
        btn_koniec.grid(row=2, column=0, columnspan=2, pady=20, sticky="we")

        self.root.grid_columnconfigure(1, weight=1)

    def dodaj_opakowanie(self, rodzaj):
        lacznie_butelek = self.sztuk_plastik + self.sztuk_szklo + self.sztuk_puszka
        if lacznie_butelek >= self.MAX_POJEMNOSC:
            messagebox.showwarning("Automat Pełny", "Osiągnięto maksymalną pojemność (65 sztuk)!")
            return
        
        if rodzaj == "plastik":
            self.sztuk_plastik += 1
            self.suma_kaucji += self.CENA_PLASTIK
        elif rodzaj == "szklo":
            self.sztuk_szklo += 1
            self.suma_kaucji += self.CENA_SZKLO
        elif rodzaj == "puszka":
            self.sztuk_puszka += 1
            self.suma_kaucji += self.CENA_PUSZKA
            
        self.odswiez_ekran()

    def odswiez_ekran(self):
        lacznie = self.sztuk_plastik + self.sztuk_szklo + self.sztuk_puszka
        self.label_plastik.config(text=f"Plastikowe: {self.sztuk_plastik} szt.")
        self.label_szklo.config(text=f"Szklane: {self.sztuk_szklo} szt.")
        self.label_puszka.config(text=f"Puszki: {self.sztuk_puszka} szt.")
        self.label_suma.config(text=f"{self.suma_kaucji:.2f} PLN")
        self.label_pojemnosc.config(text=f"Pojemność: {lacznie}/{self.MAX_POJEMNOSC}")

    def drukuj_paragon(self):
        if self.suma_kaucji == 0:
            messagebox.showinfo("Butelkomat", "Automat jest pusty!")
            return
            
        messagebox.showinfo("Wydruk paragonu", f"Twój zwrot: {self.suma_kaucji:.2f} PLN\nKoniec sesji.")
        self.root.destroy()


# --- URUCHOMIENIE PROGRAMU ---
# Tutaj tworzymy standardowe okno Tkintera, ale przekazujemy je do naszej klasy!
if __name__ == "__main__":
    okno = tk.Tk()
    app = ButelkomatApp(okno) # Tworzymy obiekt na podstawie naszej klasy
    okno.mainloop()