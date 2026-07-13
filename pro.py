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

        self.title("Ultra AI Studio 2026")
        self.geometry("1000x700")
        self.minsize(800, 550)

        # ======================================================================
        # TUTAJ WKLEJ SWÓJ KLUCZ Z GROQ (zaczyna się od gsk_...):
        # ======================================================================
        self.api_key = "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"

        # Domyślny tryb
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
        # Główny podział okna na Sidebar i Chat Frame
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------- SIDEBAR (Panel boczny) -------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="⚡ AI Studio", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Tryb Pracy:", 
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.mode_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.mode_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Czat Ogólny", "Programowanie", "Matematyka", "Tłumacz / Korekta"],
            command=self._change_mode_event
        )
        self.mode_optionmenu.grid(row=2, column=0, padx=20, pady=(5, 20))

        self.clear_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="🧹 Nowa Rozmowa", 
            fg_color="#334155", 
            hover_color="#475569",
            command=self.clear_chat
        )
        self.clear_btn.grid(row=3, column=0, padx=20, pady=10)

        # Status połączenia
        status_text = "🟢 API Gotowe" if self.api_key and "TUTAJ" not in self.api_key else "🔴 Brak Klucza API"
        self.status_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=status_text, 
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8"
        )
        self.status_label.grid(row=7, column=0, padx=20, pady=20)

        # ------------------- OBSZAR CZATU -------------------
        self.chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # Okno dymków wiadomości
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame, 
            font=ctk.CTkFont(size=14), 
            wrap="word",
            state="disabled",
            corner_radius=12
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # Panel dolny (Wprowadzanie tekstu)
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

        self._append_system_message(f"Witaj! Przełączono na tryb: {self.current_mode}.")

    def _change_mode_event(self, new_mode: str):
        self.current_mode = new_mode
        self.reset_conversation()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self._append_system_message(f"Zmieniono tryb na: {self.current_mode}. Rozpoczęto nową sesję.")

    def _append_system_message(self, text: str):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"⚙️ SYSTEM: {text}\n\n")
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
        # Wysyłanie wiadomości po kliknięciu Enter (Shift+Enter robi nową linijkę)
        if not event.state & 0x1:
            self.send_message()
            return "break"

    def send_message(self):
        user_text = self.entry_message.get("1.0", "end").strip()
        if not user_text:
            return

        if not self.api_key or "TUTAJ" in self.api_key:
            self._append_system_message("❌ Proszę wkleić klucz z Groq do zmiennej self.api_key!")
            return

        self._append_user_message(user_text)
        self.entry_message.delete("1.0", "end")

        self.conversation_history.append({"role": "user", "content": user_text})
        self.send_btn.configure(state="disabled", text="Myśli...")

        threading.Thread(target=self._call_groq_api, daemon=True).start()

    def _call_groq_api(self):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key.strip()}",
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