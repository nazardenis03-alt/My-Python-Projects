import customtkinter as ctk
import threading
import asyncio
import time
import random
from typing import Callable, Optional

# --- KONFIGURACJA SYSTEMOWA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ==========================================
# 1. WARSTWA LOGIKI BIZNESOWEJ (BACKEND / API)
# ==========================================
class AIService:
    """
    Profesjonalna usługa do obsługi zapytań AI.
    Wykorzystuje asyncio do wykonywania operacji I/O.
    """

    def __init__(self, api_key: str = "demo_key"):
        self.api_key = api_key

    async def generate_summary_async(self, text: str, mode: str) -> str:
        """Asynchroniczne przetwarzanie tekstu symulujące rzeczywisty czas odpowiedzi API."""
        if not text.strip():
            raise ValueError("Tekst wejściowy nie może być pusty.")

        # Symulacja czasu opóźnienia sieciowego (I/O bound)
        await asyncio.sleep(2.0)

        # Symulacja rzucenia błędu przy losowym scenariuszu (np. błąd sieci)
        if "error" in text.lower():
            raise ConnectionError("Nie udało się połączyć z serwerem AI. Spróbuj ponownie.")

        # Logika przetwarzania zależna od wybranego trybu
        words_count = len(text.split())
        if mode == "Streszczenie":
            return f"📌 [STRESZCZENIE AI]\nAnaliza tekstu ({words_count} słów):\nGłówne założenie tekstu sprowadza się do automatyzacji procesów biznesowych oraz zwiększenia wydajności pracy za pomocą modeli językowych."
        elif mode == "Punkty kluczowe":
            return f"💡 [KLUCZOWE WNIOSKI]\n1. Wyryte wzorce w tekście wskazują na potencjał skrótu czasu pracy o 40%.\n2. Zidentyfikowano {words_count} wyrazów kluczowych.\n3. Zalecane wdrożenie modułu asynchronicznego."
        else:
            return f"✍️ [POPRAWIONY TEKST]\n{text.strip().capitalize()} (Zweryfikowano pod kątem poprawności gramatycznej i stylistycznej)."


# ==========================================
# 2. WARSTWA INTERFEJSU UŻYTKOWNIKA (FRONTEND / GUI)
# ==========================================
class AsyncAppBridge:
    """Helper do uruchamiania async pętli zdarzeń w dedykowanym wątku tła."""

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def submit_task(self, coro, callback_success: Callable, callback_error: Callable):
        """Przesyła zadanie asynchroniczne do pętli i przypisuje reakcję po zakończeniu."""

        async def wrapper():
            try:
                result = await coro
                callback_success(result)
            except Exception as e:
                callback_error(str(e))

        asyncio.run_coroutine_threadsafe(wrapper(), self.loop)


class EnterpriseAIStudio(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Inicjalizacja usług
        self.ai_service = AIService()
        self.async_bridge = AsyncAppBridge()

        # Konfiguracja okna
        self.title("Enterprise AI Processing Suite v2.4")
        self.geometry("900x600")
        self.minsize(800, 550)

        # Układ siatki
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_area()

    def _build_sidebar(self):
        """Tworzy panel boczny z opcjami."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.lbl_title = ctk.CTkLabel(
            self.sidebar,
            text="AI Studio Pro",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_title.pack(pady=(20, 20), padx=20)

        # Wybór trybu
        self.lbl_mode = ctk.CTkLabel(
            self.sidebar, text="Tryb Przetwarzania:", anchor="w"
        )
        self.lbl_mode.pack(fill="x", padx=20, pady=(10, 0))

        self.option_mode = ctk.CTkOptionMenu(
            self.sidebar, values=["Streszczenie", "Punkty kluczowe", "Korekta Stylu"]
        )
        self.option_mode.pack(fill="x", padx=20, pady=(5, 20))

        # Wskaźnik stanu
        self.lbl_status_heading = ctk.CTkLabel(
            self.sidebar, text="Stan Połączenia:", anchor="w"
        )
        self.lbl_status_heading.pack(fill="x", padx=20, pady=(20, 0))

        self.status_badge = ctk.CTkLabel(
            self.sidebar,
            text="● Gotowy",
            text_color="#2ecc71",
            font=ctk.CTkFont(weight="bold"),
        )
        self.status_badge.pack(anchor="w", padx=20)

    def _build_main_area(self):
        """Tworzy główną przestrzeń roboczą."""
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(
            row=0, column=1, sticky="nsew", padx=25, pady=25
        )
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(3, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Sekcja 1: Input
        self.lbl_input = ctk.CTkLabel(
            self.main_container,
            text="Dane Wejściowe (Wklej tekst do analizy):",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_input.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.txt_input = ctk.CTkTextbox(self.main_container, height=120)
        self.txt_input.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        self.txt_input.insert(
            "1.0",
            "Sztuczna inteligencja zyskuje ogromną popularność w biznesie. "
            "Automatyzacja procesów pozwala zaoszczędzić setki godzin pracy ręcznej.",
        )

        # Przycisk i Pasek Postępu
        self.btn_process = ctk.CTkButton(
            self.main_container,
            text="Uruchom Analizę AI",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_process_click,
        )
        self.btn_process.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        self.progress_bar = ctk.CTkProgressBar(self.main_container)
        self.progress_bar.grid(row=2, column=0, sticky="ew", pady=(45, 0))
        self.progress_bar.set(0)

        # Sekcja 2: Output
        self.lbl_output = ctk.CTkLabel(
            self.main_container,
            text="Wynik Analizy AI:",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_output.grid(row=3, column=0, sticky="nw", pady=(15, 5))

        self.txt_output = ctk.CTkTextbox(self.main_container)
        self.txt_output.grid(row=4, column=0, sticky="nsew")

    def _on_process_click(self):
        """Obsługa kliknięcia - przygotowanie GUI i wysłanie zadania asynchronicznego."""
        input_text = self.txt_input.get("1.0", "end-1c")
        selected_mode = self.option_mode.get()

        # Blokada UI na czas przetwarzania
        self.btn_process.configure(state="disabled", text="Przetwarzanie...")
        self.status_badge.configure(text="● Przetwarzanie...", text_color="#f39c12")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        # Zlecenie zadania do pętli zdarzeń asyncio
        coro = self.ai_service.generate_summary_async(input_text, selected_mode)
        self.async_bridge.submit_task(
            coro,
            callback_success=lambda res: self.after(0, self._handle_success, res),
            callback_error=lambda err: self.after(0, self._handle_error, err),
        )

    def _handle_success(self, result: str):
        """Obsługa sukcesu (wywoływana w wątku głównym GUI)."""
        self._reset_ui_state()
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", result)
        self.status_badge.configure(text="● Gotowy", text_color="#2ecc71")

    def _handle_error(self, error_message: str):
        """Obsługa błędów (wywoływana w wątku głównym GUI)."""
        self._reset_ui_state()
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", f"❌ BŁĄD SYSTEMU:\n{error_message}")
        self.status_badge.configure(text="● Błąd", text_color="#e74c3c")

    def _reset_ui_state(self):
        """Przywraca standardowy stan przycisków i paska postępu."""
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.btn_process.configure(state="normal", text="Uruchom Analizę AI")


# ==========================================
# 3. PUNKT WEJŚCIA (ENTRY POINT)
# ==========================================
if __name__ == "__main__":
    app = EnterpriseAIStudio()
    app.mainloop()