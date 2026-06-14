import tkinter as tk
from tkinter import messagebox

class ZwierzakApp:
    def __init__(self, okno):
        self.root = okno
        self.root.title("Tamagotchi PRO - Obiektowo")
        self.root.geometry("320x480")
        self.root.configure(bg="#f5f6fa")

        # --- STATYSTYKI ZWIERZAKA ---
        self.glod = 30
        self.nuda = 30
        self.energia = 100  # Nowość: startujemy z pełną energią
        
        # --- STATYSTYKI GRACZA (POZIOMY) ---
        self.xp = 0
        self.poziom = 1
        
        # --- FLAGA STATUSU ---
        self.czy_spi = False  # Sprawdza, czy lisek aktualnie śpi

        # Odpalamy wygląd i pętlę czasu
        self.stworz_interfejs()
        self.aktualizuj_czas()

    def stworz_interfejs(self):
        # Główny status i emotka zwierzaka
        self.label_status = tk.Label(self.root, text="🦊\nTwój zwierzak żyje!", font=("Arial", 14, "bold"), bg="#f5f6fa", fg="#2c3e50")
        self.label_status.pack(pady=15)
        
        # Pasek poziomu i XP
        self.label_level = tk.Label(self.root, text=f"Poziom: {self.poziom} (XP: {self.xp}/5)", font=("Arial", 10, "bold"), bg="#f5f6fa", fg="#8e44ad")
        self.label_level.pack(pady=5)
        
        # Statystyki na ekranie
        self.label_glod = tk.Label(self.root, text=f"Głód: {self.glod}/100", font=("Arial", 11), bg="#f5f6fa")
        self.label_glod.pack(pady=2)
        
        self.label_nuda = tk.Label(self.root, text=f"Nuda: {self.nuda}/100", font=("Arial", 11), bg="#f5f6fa")
        self.label_nuda.pack(pady=2)
        
        self.label_energia = tk.Label(self.root, text=f"Energia: {self.energia}/100", font=("Arial", 11), bg="#f5f6fa")
        self.label_energia.pack(pady=2)
        
        # --- PRZYCISKI ---
        self.btn_karm = tk.Button(self.root, text="🍖 Karm (-10 Głodu)", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", width=20, command=self.karm)
        self.btn_karm.pack(pady=5)
        
        self.btn_baw = tk.Button(self.root, text="🎮 Baw się (-10 Nudy)", font=("Arial", 11, "bold"), bg="#3498db", fg="white", width=20, command=self.baw_sie)
        self.btn_baw.pack(pady=5)
        
        # Nowy przycisk snu
        self.btn_sen = tk.Button(self.root, text="😴 Idź spać (+100 Energii)", font=("Arial", 11, "bold"), bg="#f1c40f", fg="black", width=20, command=self.idz_spac)
        self.btn_sen.pack(pady=5)

    # --- PĘTLA CZASU (CO 10 SEKUND) ---
    def aktualizuj_czas(self):
        # Jeśli zwierzak śpi, czas płynie inaczej (nie nudzi się i nie głoduje tak szybko)
        if not self.czy_spi:
            if self.glod < 100: self.glod += 10
            if self.nuda < 100: self.nuda += 10
            if self.energia > 0: self.energia -= 15  # Życie zużywa energię
            
            # Dodawanie doświadczenia za przeżycie kolejnych 10 sekund!
            self.xp += 1
            if self.xp >= 5:
                self.poziom += 1
                self.xp = 0
                messagebox.showinfo("LEVEL UP!", f"Brawo! Twój lisek awansował na {self.poziom} poziom! 🎉")
        
        self.odswiez_wyswietlacz()
        self.sprawdz_stan_zwierzaka()
        
        # Ponowne odliczenie 10 sekund (jeśli zwierzak żyje)
        if self.glod < 100 and self.nuda < 100 and self.energia > 0:
            self.root.after(10000, self.aktualizuj_czas)

    def sprawdz_stan_zwierzaka(self):
        # 1. Warunek śmierci
        if self.glod >= 100 or self.nuda >= 100 or self.energia <= 0:
            self.label_status.config(text="💀\nTWÓJ ZWIERZAK ZGINĄŁ!", fg="#c0392b")
            
            powod = ""
            if self.glod >= 100: powod = "z głodu"
            elif self.nuda >= 100: powod = "z nudów"
            else: powod = "z wycieńczenia (brak energii)"
            
            messagebox.showerror("Koniec Gry", f"Lisek zginął {powod}.\nOsiągnięty poziom: {self.poziom}!")
            self.root.destroy()
            return

        # 2. Zmiana emoji i napisów w zależności od stanu
        if self.czy_spi:
            self.label_status.config(text="😴\nChrrrr... lisek śpi...", fg="#f1c40f")
        elif self.glod >= 60 or self.nuda >= 60 or self.energia <= 30:
            self.label_status.config(text="🥺\nOSTRZEŻENIE: Pomóż mi!", fg="#e74c3c")
        else:
            self.label_status.config(text="🦊\nTwój lisek jest szczęśliwy!", fg="#2c3e50")

    def odswiez_wyswietlacz(self):
        self.label_glod.config(text=f"Głód: {self.glod}/100")
        self.label_nuda.config(text=f"Nuda: {self.nuda}/100")
        self.label_energia.config(text=f"Energia: {self.energia}/100")
        self.label_level.config(text=f"Poziom: {self.poziom} (XP: {self.xp}/5)")

    # --- INTERAKCJE GRACZA ---
    def karm(self):
        if self.czy_spi: return  # Śpiącego liska nie karmimy!
        
        if self.glod >= 10: self.glod -= 10
        else: self.glod = 0
            
        self.odswiez_wyswietlacz()
        self.sprawdz_stan_zwierzaka()
        
    def baw_sie(self):
        if self.czy_spi: return  # Śpiący lisek się nie bawi!
        
        if self.nuda >= 10: self.nuda -= 10
        else: self.nuda = 0
        
        # Zabawa dodatkowo męczy (-5 energii)
        if self.energia >= 5: self.energia -= 5
            
        self.odswiez_wyswietlacz()
        self.sprawdz_stan_zwierzaka()

    def idz_spac(self):
        if self.czy_spi: return
        
        self.czy_spi = True
        self.sprawdz_stan_zwierzaka()
        
        # Blokujemy przyciski na czas snu
        self.btn_karm.config(state="disabled")
        self.btn_baw.config(state="disabled")
        
        # Wywołujemy pobudke po 3000 milisekundach (3 sekundy snu)
        self.root.after(3000, self.obudz_sie)

    def obudz_sie(self):
        self.czy_spi = False
        self.energia = 100  # Energia naładowana!
        
        # Odblokowujemy przyciski
        self.btn_karm.config(state="normal")
        self.btn_baw.config(state="normal")
        
        self.odswiez_wyswietlacz()
        self.sprawdz_stan_zwierzaka()
        messagebox.showinfo("Tamagotchi", "Lisek się wyspał i ma mnóstwo energii! ☀️")

# Uruchomienie programu
if __name__ == "__main__":
    glowne_okno = tk.Tk()
    app = ZwierzakApp(glowne_okno)
    glowne_okno.mainloop()