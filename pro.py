import json
import threading
import urllib.request
import urllib.error
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AIAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ultra AI Studio")
        self.geometry("1000x700")
        self.minsize(800, 550)

        # ======================================================================
        # Zostawiamy puste – użytkownik wpisuje swój klucz z Groq w aplikacji
        # lub bezpośrednio w tej zmiennej przed uruchomieniem
        # ======================================================================
        self.api_key = ""

        # Domyślny tryb pracy
        self.current_mode = "Czat Ogólny"
        
        # Konfiguracja promptów dla trybów
        self.mode_prompts = {
            "Czat Ogólny": "Jesteś pomocnym, inteligentnym asystentem AI. Odpowiadasz zwięźle, precyzyjnie i po polsku.",
            "Programowanie": "Jesteś ekspertem programowania (Python, C++, JS itp.). Twój kod jest czysty, dobrze udokumentowany i gotowy do uruchomienia. Zawsze wyjaśniasz krótkimi punktami, jak działa dany kod.",
            "Matematyka": "Jesteś nauczycielem matematyki i logiki. Rozwiązujesz zadania krok po kroku, jasno tłumacząc każde przekształcenie i wzór.",
            "Tłumacz / Korekta": "Jesteś profesjonalnym tłumaczem językowym. Tłumaczysz teksty zachowując naturalny styl oraz poprawiasz błędy gramatyczne i ortograficzne."
        }

        self.reset_conversation()
        self._build_ui()

    def reset_conversation(self):
        """Resetuje historię rozmowy na podstawie wybranego trybu."""
        system_instruction = self.mode_prompts.get(self.current_mode, self.mode_prompts["Czat Ogólny"])
        self.conversation_history = [
            {"role": "system", "content": system_instruction}
        ]

    def _build_ui(self):
        # Układ dwukolumnowy: Panel Boczny + Główny Czat
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------- PANEL BOCZNY (Sidebar) -------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="⚡ AI Studio", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Pole na klucz API w interfejsie
        self.key_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Klucz Groq API:", 
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w"
        )
        self.key_label.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="w")

        self.key_entry = ctk.CTkEntry(
            self.sidebar_frame, 
            placeholder_text="gsk_...", 
            show="*"
        )
        self.key_entry.grid(row=2, column=0, padx=20, pady=(2, 10), sticky="ew")

        # Wybór trybu pracy
        self.mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Tryb Pracy:", 
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w"
        )
        self.mode_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.mode_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Czat Ogólny", "Programowanie", "Matematyka", "Tłumacz / Korekta"],
            command=self._change_mode_event
        )
        self.mode_optionmenu.grid(row=4, column=0, padx=20, pady=(2, 20))

        self.clear_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="🧹 Nowa Rozmowa", 
            fg_color="#334155", 
            hover_color="#475569",
            command=self.clear_chat
        )
        self.clear_btn.grid(row=5, column=0, padx=20, pady=10)

        # ------------------- OBSZAR CZATU -------------------
        self.chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # Pole tekstowe czatu
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame, 
            font=ctk.CTkFont(size=14), 
            wrap="word",
            state="disabled",
            corner_radius=12
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # Dolny panel wprowadzania tekstu
        self.bottom_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.bottom_frame.grid(row=1, column=0, sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.entry_message = ctk.CTkTextbox(
            self.bottom_frame, 
            font=ctk.CTkFont(size=14),
            height=60,
            corner_radius=10
        )
        self.entry_message.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_message.bind("<Return>", self._on_enter_press)

        self.send_btn = ctk.CTkButton(
            self.bottom_frame, 
            text="Wyślij 🚀", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            width=110,
            corner_radius=10,
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1)

        self._append_system_message(f"Witaj! Wybrany tryb: {self.current_mode}.\nWklej swój klucz Groq w panelu po lewej stronie, aby rozpocząć.")

    def _get_active_api_key(self) -> str:
        """Pobiera klucz z pola tekstowego lub zmiennej klasy."""
        entry_key = self.key_entry.get().strip()
        if entry_key:
            return entry_key
        return self.api_key.strip()

    def _change_mode_event(self, new_mode: str):
        self.current_mode = new_mode
        self.reset_conversation()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self._append_system_message(f"Zmieniono tryb na: {self.current_mode}. Rozpoczęto nową sesję.")

    def _append_system_message(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"⚙️ SYSTEM:\n{text}\n\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def _append_user_message(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"👤 TY:\n{text}\n\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def _append_bot_message(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"🤖 AI ({self.current_mode}):\n{text}\n\n" + "─"*50 + "\n\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def clear_chat(self):
        self.reset_conversation()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self._append_system_message("Wyczyszczono historię rozmowy.")

    def _on_enter_press(self, event):
        # Enter wysyła wiadomość, Shift+Enter robi nową linijkę
        if not event.state & 0x1:
            self.send_message()
            return "break"

    def send_message(self):
        user_text = self.entry_message.get("1.0", "end").strip()
        if not user_text:
            return

        active_key = self._get_active_api_key()
        if not active_key:
            self._append_system_message("❌ Podaj klucz API Groq w panelu bocznym po lewej stronie!")
            return

        self._append_user_message(user_text)
        self.entry_message.delete("1.0", "end")

        self.conversation_history.append({"role": "user", "content": user_text})
        self.send_btn.configure(state="disabled", text="Myśli...")

        threading.Thread(target=self._call_groq_api, args=(active_key,), daemon=True).start()

    def _call_groq_api(self, api_key: str):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": self.conversation_history,
            "temperature": 0.6
        }

        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(data).encode("utf-8"), 
                headers=headers, 
                method="POST"
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                bot_reply = result["choices"][0]["message"]["content"]
                
                self.conversation_history.append({"role": "assistant", "content": bot_reply})
                self.after(0, lambda: self._handle_success(bot_reply))

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            self.after(0, lambda: self._handle_error(f"Błąd HTTP {e.code}: {err_body}"))
        except Exception as e:
            self.after(0, lambda: self._handle_error(f"Błąd połączenia: {e}"))

    def _handle_success(self, reply: str):
        self._append_bot_message(reply)
        self.send_btn.configure(state="normal", text="Wyślij 🚀")

    def _handle_error(self, error_msg: str):
        self._append_system_message(f"Błąd: {error_msg}")
        self.send_btn.configure(state="normal", text="Wyślij 🚀")


if __name__ == "__main__":
    app = AIAssistantApp()
    app.mainloop()