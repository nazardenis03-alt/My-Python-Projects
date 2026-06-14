import tkinter as tk
from tkinter import messagebox
import random

# 1. SZABLON (KLASA) DLA POJEDYNCZEGO PIŁKARZA
class Pilkarz:
    def __init__(self, nazwisko, pozycja, ovr):
        self.nazwisko = nazwisko
        self.pozycja = pozycja.lower() # Zapisujemy małymi literami dla ułatwienia logiki
        self.ovr = int(ovr)
        self.energia = 100

    def trenuj(self):
        if self.energia >= 20:
            self.ovr += 1
            self.energia -= 20
            return True
        return False

    def odpocznij(self):
        if self.energia < 100:
            self.energia = 100
            return True
        return False


# 2. KLASA GŁÓWNA INTERFEJSU
class ManagerApp:
    def __init__(self, okno):
        self.root = okno
        self.root.title("Skaut Manager Pro - Match Day")
        self.root.geometry("450x530") # Powiększone okno na sekcję meczową
        self.root.configure(bg="#f1f2f6")

        self.lista_pilkarzy = []
        self.stworz_interfejs()

    def stworz_interfejs(self):
        # PANEL DODAWANIA
        frame_dodaj = tk.LabelFrame(self.root, text=" Dodaj nowego zawodnika ", font=("Arial", 10, "bold"), bg="#f1f2f6", padx=10, pady=5)
        frame_dodaj.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_dodaj, text="Nazwisko:", bg="#f1f2f6").grid(row=0, column=0, sticky="w")
        self.entry_nazwisko = tk.Entry(frame_dodaj)
        self.entry_nazwisko.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_dodaj, text="Pozycja (napastnik/pomocnik/obronca/bramkarz):", font=("Arial", 8), bg="#f1f2f6").grid(row=1, column=0, sticky="w")
        self.entry_pozycja = tk.Entry(frame_dodaj)
        self.entry_pozycja.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_dodaj, text="OVR (60-99):", bg="#f1f2f6").grid(row=2, column=0, sticky="w")
        self.entry_ovr = tk.Entry(frame_dodaj, width=5)
        self.entry_ovr.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        btn_dodaj = tk.Button(frame_dodaj, text="➕ Dodaj do bazy", bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), command=self.stworz_pilkarza)
        btn_dodaj.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")

        # PANEL DRUŻYNY
        frame_lista = tk.LabelFrame(self.root, text=" Twoja Drużyna ", font=("Arial", 10, "bold"), bg="#f1f2f6", padx=10, pady=5)
        frame_lista.pack(fill="both", expand=True, padx=15, pady=5)

        self.listbox_sklad = tk.Listbox(frame_lista, height=5)
        self.listbox_sklad.pack(side="left", fill="both", expand=True)

        frame_akcje = tk.Frame(frame_lista, bg="#f1f2f6")
        frame_akcje.pack(side="right", padx=10)

        tk.Button(frame_akcje, text="🏃 Trenuj", width=12, bg="#3498db", fg="white", command=self.trenuj_wybranego).pack(pady=3)
        tk.Button(frame_akcje, text="💤 Odpoczynek", width=12, bg="#e67e22", fg="white", command=self.odpocznij_wybranego).pack(pady=3)
        tk.Button(frame_akcje, text="📊 Szczegóły", width=12, bg="#9b59b6", fg="white", command=self.pokaz_szczegoly).pack(pady=3)

        # --- SEKCJA MECZOWA (NOWOŚĆ!) ---
        self.frame_mecz = tk.LabelFrame(self.root, text=" Dzień Meczowy ", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white", padx=10, pady=10)
        self.frame_mecz.pack(fill="x", padx=15, pady=10)

        self.label_status_meczu = tk.Label(self.frame_mecz, text="Oczekiwanie na decyzję managera...", font=("Arial", 10, "italic"), bg="#2c3e50", fg="#bdc3c7")
        self.label_status_meczu.pack(pady=2)

        self.btn_mecz = tk.Button(self.frame_mecz, text="⚽ ROZGRAJ MECZ (10s)", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", command=self.rozpocznij_mecz)
        self.btn_mecz.pack(fill="x", pady=5)

    # --- LOGIKA APLIKACJI ---

    def stworz_pilkarza(self):
        nazw = self.entry_nazwisko.get()
        poz = self.entry_pozycja.get()
        moc = self.entry_ovr.get()

        if nazw and poz and moc:
            nowy_zawodnik = Pilkarz(nazw, poz, moc)
            self.lista_pilkarzy.append(nowy_zawodnik)
            self.listbox_sklad.insert(tk.END, f"{nowy_zawodnik.nazwisko} ({nowy_zawodnik.pozycja.capitalize()})")
            
            self.entry_nazwisko.delete(0, tk.END)
            self.entry_pozycja.delete(0, tk.END)
            self.entry_ovr.delete(0, tk.END)
        else:
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola!")

    def pobierz_indeks(self):
        zaznaczenie = self.listbox_sklad.curselection()
        if zaznaczenie:
            return zaznaczenie[0]
        messagebox.showinfo("Wybór", "Zaznacz najpierw piłkarza na liście!")
        return None

    def pokaz_szczegoly(self):
        idx = self.pobierz_indeks()
        if idx is not None:
            p = self.lista_pilkarzy[idx]
            messagebox.showinfo(
                f"Profil: {p.nazwisko}",
                f"Pozycja: {p.pozycja.capitalize()}\n"
                f"Umiejętności (OVR): {p.ovr}/99\n"
                f"Energia: {p.energia}/100%"
            )

    def trenuj_wybranego(self):
        idx = self.pobierz_indeks()
        if idx is not None:
            p = self.lista_pilkarzy[idx]
            if p.trenuj():
                messagebox.showinfo("Trening", f"{p.nazwisko} odbył trening!\nOVR: {p.ovr}\nEnergia: {p.energia}%")
            else:
                messagebox.showwarning("Zmęczenie", f"{p.nazwisko} jest zbyt zmęczony! Wyślij go na odpoczynek.")

    def odpocznij_wybranego(self):
        idx = self.pobierz_indeks()
        if idx is not None:
            p = self.lista_pilkarzy[idx]
            if p.odpocznij():
                messagebox.showinfo("Odpoczynek", f"{p.nazwisko} odpoczął! Energia naładowana do 100%.")
            else:
                messagebox.showinfo("Odpoczynek", f"{p.nazwisko} jest w pełni sił.")

    # --- NOWOŚĆ: SYSTEM SYMULACJI MECZU CO 10 SEKUND ---

    def rozpocznij_mecz(self):
        # Sprawdzamy, czy w ogóle mamy jakichś piłkarzy w bazie
        if not self.lista_pilkarzy:
            messagebox.showwarning("Brak składu", "Nie masz żadnych piłkarzy w drużynie! Dodaj kogoś przed meczem.")
            return

        # Sprawdzamy, czy piłkarze mają siłę grać (min. 30 energii)
        for p in self.lista_pilkarzy:
            if p.energia < 30:
                messagebox.showwarning("Brak energii", f"Zawodnik {p.nazwisko} jest zbyt wycieńczony ({p.energia}% energii), by wyjść na boisko!")
                return

        # Blokujemy przycisk meczu, żeby gracz nie kliknął go kilka razy
        self.btn_mecz.config(state="disabled", bg="#7f8c8d")
        self.label_status_meczu.config(text="⏱️ Trwa mecz... Sędzia gwizdał po raz pierwszy! (Czekaj 10s)", fg="#f1c40f")

        # Kluczowe: po 10000 ms (10 sekundach) wywołujemy koniec meczu
        self.root.after(10000, self.zakoncz_mecz)

    def zakoncz_mecz(self):
        raport_meczu = "📊 STATYSTYKI TWOICH ZAWODNIKÓW:\n\n"
        
        # Przechodzimy pętlą przez KAŻDEGO piłkarza w naszej drużynie
        for p in self.lista_pilkarzy:
            p.energia -= 30  # Mecz kosztuje 30% energii
            
            # Losujemy akcje na podstawie pozycji zawodnika i jego OVR
            szansa_sukcesu = random.randint(1, 100) + (p.ovr // 5)
            
            if "napastnik" in p.pozycja:
                if szansa_sukcesu > 75:
                    akcja = "Strzelił kapitalną bramkę w okienko! ⚽"
                elif szansa_sukcesu > 45:
                    akcja = "Zaliczył asystę i oddał dwa groźne strzały. 👟"
                else:
                    akcja = "Był całkowicie odcięty od podań, słaby występ. 🥶"
                    
            elif "pomocnik" in p.pozycja:
                if szansa_sukcesu > 70:
                    akcja = "Rządził w środku pola i zaliczył asystę roku! 🪄"
                elif szansa_sukcesu > 40:
                    akcja = "Zanotował kilka celnych podań i napędzał akcje."
                else:
                    akcja = "Zaliczył sporo strat i dostał żółtą kartkę. 🟨"
                    
            elif "obronca" in p.pozycja or "obrońca" in p.pozycja:
                if szansa_sukcesu > 65:
                    akcja = "Zablokował kluczowy strzał rywala, czyste konto! 🛡️"
                else:
                    akcja = "Dał się raz dryblować, ale ogólnie poprawny mecz."
                    
            elif "bramkarz" in p.pozycja:
                if szansa_sukcesu > 70:
                    akcja = "Obronił rzut karny w 90. minucie! Klasa światowa! 🧤"
                else:
                    akcja = "Wpuścił jedną bramkę, ale zaliczył dwie dobre interwencje."
            else:
                akcja = "Biegał chaotycznie po boisku (nieznana pozycja)."

            raport_meczu += f"• {p.nazwisko} ({p.pozycja.capitalize()}): {akcja}\n"

        # Wyświetlamy wielkie podsumowanie w messageboxie
        messagebox.showinfo("Koniec Meczu!", raport_meczu)

        # Odblokowujemy przycisk meczu dla kolejnych spotkań
        self.btn_mecz.config(state="normal", bg="#e74c3c")
        self.label_status_meczu.config(text="Mecz zakończony! Zawodnicy wrócili zmęczeni.", fg="#2ecc71")


if __name__ == "__main__":
    okno = tk.Tk()
    app = ManagerApp(okno)
    okno.mainloop()