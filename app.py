import customtkinter as ctk
import threading
import time
import random

# Ustawienia motywu
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProfessionalDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfiguracja okna głównego
        self.title("AI Data Processing Hub")
        self.geometry("800x500")
        self.resizable(False, False)

        # Układ siatki (Grid layout)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PANEL BOCZNY (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="AI Studio Studio", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=(20, 30), padx=20)

        self.btn_status = ctk.CTkButton(
            self.sidebar_frame, 
            text="Stan Systemu", 
            fg_color="transparent", 
            anchor="w"
        )
        self.btn_status.pack(fill="x", padx=10, pady=5)

        # --- PANEL GŁÓWNY (MAIN CONTENT) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.header = ctk.CTkLabel(
            self.main_frame, 
            text="Generowanie i Analiza Raportów", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.header.pack(anchor="w", pady=(0, 20))

        # Sekcja sterowania
        self.control_card = ctk.CTkFrame(self.main_frame)
        self.control_card.pack(fill="x", pady=(0, 20), ipadx=10, ipady=10)

        self.info_label = ctk.CTkLabel(
            self.control_card, 
            text="Kliknij poniżej, aby uruchomić zadanie asynchroniczne symulujące zapytanie do AI:",
            anchor="w"
        )
        self.info_label.pack(anchor="w", padx=15, pady=(10, 10))

        self.start_btn = ctk.CTkButton(
            self.control_card, 
            text="Uruchom Analizę AI", 
            command=self.start_async_task
        )
        self.start_btn.pack(anchor="w", padx=15, pady=(0, 10))

        # Pasek postępu
        self.progress_bar = ctk.CTkProgressBar(self.control_card)
        self.progress_bar.pack(fill="x", padx=15, pady=(5, 10))
        self.progress_bar.set(0)

        # Console Output / Logi
        self.log_label = ctk.CTkLabel(
            self.main_frame, 
            text="Konsola wyjściowa:", 
            font=ctk.CTkFont(weight="bold")
        )
        self.log_label.pack(anchor="w", pady=(0, 5))

        self.log_textbox = ctk.CTkTextbox(self.main_frame, width=500, height=200)
        self.log_textbox.pack(fill="both", expand=True)
        self.log_textbox.insert("0.0", "[INFO] System gotowy do pracy.\n")

    def log(self, text: str):
        """Pomocnicza funkcja do bezpiecznego dodawania logów."""
        self.log_textbox.insert("end", f"{text}\n")
        self.log_textbox.see("end")

    def start_async_task(self):
        """Uruchamia operację w osobnym wątku, aby nie blokować GUI."""
        self.start_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.log("[START] Rozpoczynanie przetwarzania...")

        # Tworzenie i uruchomienie wątku tła (Threading)
        threading.Thread(target=self._run_ai_simulation, daemon=True).start()

    def _run_ai_simulation(self):
        """Symulacja ciężkiego zadania (np. wywołania API AI)."""
        steps = ["Łączenie z modelem...", "Analiza danych...", "Generowanie odpowiedzi...", "Finalizacja..."]
        
        for i, step in enumerate(steps, start=1):
            time.sleep(1.2)  # Symulacja opóźnienia sieciowego/obliczeń
            progress = i / len(steps)
            
            # Aktualizacja interfejsu w sposób bezpieczny
            self.after(0, self._update_ui, progress, f"[PROCES] {step}")

        metrics = f"Wynik wygenerowany poprawnie (Zaufanie: {random.randint(90, 99)}%)"
        self.after(0, self._finish_task, metrics)

    def _update_ui(self, progress: float, log_text: str):
        """Aktualizacja paska postępu i konsoli z poziomu głównego wątku GUI."""
        self.progress_bar.set(progress)
        self.log(log_text)

    def _finish_task(self, result_text: str):
        """Zakończenie zadania i odblokowanie przycisku."""
        self.log(f"[SUKCES] {result_text}")
        self.start_btn.configure(state="normal")

if __name__ == "__main__":
    app = ProfessionalDashboard()
    app.mainloop()