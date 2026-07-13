import customtkinter as ctk
import threading
import time
import random
import pandas as pd
from typing import List, Dict

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DataScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("E-Commerce Data Scraper & Exporter Pro")
        self.geometry("850x550")
        
        self.scraped_data: List[Dict[str, str]] = []

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_controls()
        self._build_table_view()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        self.lbl_title = ctk.CTkLabel(
            self.header_frame, 
            text="🕷️ Web Data Extractor", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_title.pack(anchor="w")

    def _build_controls(self):
        self.control_card = ctk.CTkFrame(self)
        self.control_card.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.entry_url = ctk.CTkEntry(
            self.control_card, 
            placeholder_text="Wklej URL sklepu/strony...",
            width=400
        )
        self.entry_url.pack(side="left", padx=15, pady=15)

        self.btn_start = ctk.CTkButton(
            self.control_card, 
            text="Pobierz Dane", 
            command=self._start_scraping
        )
        self.btn_start.pack(side="left", padx=5, pady=15)

        self.btn_export = ctk.CTkButton(
            self.control_card, 
            text="Eksportuj do Excela", 
            fg_color="#27ae60", 
            hover_color="#219150",
            state="disabled",
            command=self._export_to_excel
        )
        self.btn_export.pack(side="left", padx=10, pady=15)

    def _build_table_view(self):
        self.logs_textbox = ctk.CTkTextbox(self, width=800, height=300)
        self.logs_textbox.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.logs_textbox.insert("1.0", "[SYSTEM] Gotowy do pracy. Wpisz URL i kliknij 'Pobierz Dane'.\n")

    def _start_scraping(self):
        url = self.entry_url.get().strip()
        if not url:
            self.logs_textbox.insert("end", "[BŁĄD] Wprowadź poprawny adres URL!\n")
            return

        self.btn_start.configure(state="disabled")
        self.btn_export.configure(state="disabled")
        self.logs_textbox.insert("end", f"\n[START] Łączenie z URL: {url}...\n")

        threading.Thread(target=self._run_scraper_logic, daemon=True).start()

    def _run_scraper_logic(self):
        # Symulacja ekstraktora (np. BeautifulSoup / Selenium / Playwright)
        fake_products = ["Klawiatura Mechaniczna", "Mysz Bezprzewodowa", "Monitor 4K", "Słuchawki Pro", "Podkładka XXL"]
        self.scraped_data.clear()

        for i in range(1, 6):
            time.sleep(0.8) # Odstęp czasowy
            item = {
                "ID": f"PROD-{i:03d}",
                "Nazwa": fake_products[i-1],
                "Cena": f"{random.randint(50, 600)} PLN",
                "Dostępność": random.choice(["Dostępny", "Brak w magazynie"])
            }
            self.scraped_data.append(item)
            
            # Aktualizacja UI
            log_text = f"[POBRANO] {item['ID']} | {item['Nazwa']} | Cena: {item['Cena']}\n"
            self.after(0, lambda t=log_text: self.logs_textbox.insert("end", t))

        self.after(0, self._finish_scraping)

    def _finish_scraping(self):
        self.logs_textbox.insert("end", "[SUKCES] Zakończono pobieranie danych!\n")
        self.btn_start.configure(state="normal")
        self.btn_export.configure(state="normal")

    def _export_to_excel(self):
        if not self.scraped_data:
            return
        
        # Zapis do Pandas i Excela
        df = pd.DataFrame(self.scraped_data)
        file_name = "pobrane_produkty.xlsx"
        df.to_excel(file_name, index=False)
        self.logs_textbox.insert("end", f"\n[ZAPISANO] Dane zostały zapisane do pliku: {file_name}\n")

if __name__ == "__main__":
    app = DataScraperApp()
    app.mainloop()