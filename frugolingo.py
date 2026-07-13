import datetime
import math
import random
import sqlite3
import subprocess
import threading
from typing import List, Dict, Tuple

import customtkinter as ctk

# ==============================================================================
# 1. BAZA DANYCH & ALGORYTM SPACED REPETITION (SM-2)
# ==============================================================================

class DatabaseManager:
    """Zarządza bazą SQLite, przechowuje słownictwo oraz postęp SM-2."""

    def __init__(self, db_path: str = "frugolingo_advanced.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_en TEXT NOT NULL,
                    word_pl TEXT NOT NULL,
                    category TEXT NOT NULL,
                    easiness_factor REAL DEFAULT 2.5,
                    interval INTEGER DEFAULT 0,
                    repetitions INTEGER DEFAULT 0,
                    next_review DATE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    id INTEGER PRIMARY KEY,
                    xp INTEGER DEFAULT 0,
                    streak INTEGER DEFAULT 0
                )
            """)
            cursor.execute("INSERT OR IGNORE INTO user_stats (id, xp, streak) VALUES (1, 0, 1)")
            conn.commit()
            self._seed_initial_data(cursor, conn)

    def _seed_initial_data(self, cursor, conn):
        cursor.execute("SELECT COUNT(*) FROM cards")
        if cursor.fetchone()[0] == 0:
            today = datetime.date.today().isoformat()
            sample_cards = [
                ("Artificial Intelligence", "Sztuczna inteligencja", "Tech"),
                ("Machine Learning", "Uczenie maszynowe", "Tech"),
                ("Concurrency", "Wielowątkowość", "Programming"),
                ("Algorithm", "Algorytm", "Programming"),
                ("Database", "Baza danych", "Tech"),
                ("Asynchronous", "Asynchroniczny", "Programming"),
                ("Automation", "Automatyzacja", "Tech"),
                ("Repository", "Repozytorium", "Programming"),
                ("Scalability", "Skalowalność", "Architecture"),
                ("Optimization", "Optymalizacja", "Programming")
            ]
            for en, pl, cat in sample_cards:
                cursor.execute("""
                    INSERT INTO cards (word_en, word_pl, category, next_review)
                    VALUES (?, ?, ?, ?)
                """, (en, pl, cat, today))
            conn.commit()

    def get_due_cards(self, limit: int = 10) -> List[Dict]:
        today = datetime.date.today().isoformat()
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM cards WHERE next_review <= ? ORDER BY RANDOM() LIMIT ?
            """, (today, limit))
            results = [dict(row) for row in cursor.fetchall()]

            # Jeśli brak kart do powtórki na dziś, pobierz dowolne do nauki
            if not results:
                cursor.execute("SELECT * FROM cards ORDER BY RANDOM() LIMIT ?", (limit,))
                results = [dict(row) for row in cursor.fetchall()]

            return results

    def reset_all_reviews(self):
        """Resetuje daty powtórek dla celów testowych/treningowych."""
        today = datetime.date.today().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE cards SET next_review = ?", (today,))
            conn.commit()

    def update_card_sm2(self, card_id: int, quality: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT easiness_factor, interval, repetitions FROM cards WHERE id = ?", (card_id,))
            ef, interval, reps = cursor.fetchone()

            ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            if ef < 1.3:
                ef = 1.3

            if quality < 3:
                reps = 0
                interval = 1
            else:
                if reps == 0:
                    interval = 1
                elif reps == 1:
                    interval = 6
                else:
                    interval = math.ceil(interval * ef)
                reps += 1

            next_date = (datetime.date.today() + datetime.timedelta(days=interval)).isoformat()
            cursor.execute("""
                UPDATE cards 
                SET easiness_factor = ?, interval = ?, repetitions = ?, next_review = ?
                WHERE id = ?
            """, (ef, interval, reps, next_date, card_id))
            conn.commit()

    def get_user_stats(self) -> Tuple[int, int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT xp, streak FROM user_stats WHERE id = 1")
            return cursor.fetchone()

    def add_xp(self, amount: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_stats SET xp = xp + ? WHERE id = 1", (amount,))
            conn.commit()


# ==============================================================================
# 2. AUDIO SYNTHESIS ENGINE (Natywny Lektor Windows SAPI)
# ==============================================================================

class TTSEngine:
    @staticmethod
    def speak(text: str):
        def _play():
            try:
                ps_cmd = f'$speak = New-Object -ComObject SAPI.SpVoice; $speak.Speak("{text}")'
                subprocess.run(
                    ["powershell", "-Command", ps_cmd],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
                )
            except Exception as e:
                print(f"[TTS Error]: {e}")

        threading.Thread(target=_play, daemon=True).start()


# ==============================================================================
# 3. INTERFEJS GRAFICZNY (CustomTkinter)
# ==============================================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FrugolingoApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Frugolingo Multi-Mode Engine")
        self.geometry("950x680")
        self.minsize(850, 600)

        self.db = DatabaseManager()
        self.tts = TTSEngine()

        self.current_mode = "Classic Quiz"
        self.current_cards: List[Dict] = []
        self.current_index: int = 0
        self.correct_answer: str = ""
        self.tf_is_correct: bool = True

        self._build_top_bar()
        self._build_mode_selector()
        self._build_main_container()

        self.load_session()

    def _build_top_bar(self):
        self.top_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.top_frame.pack(side="top", fill="x", padx=0, pady=0)

        self.title_label = ctk.CTkLabel(
            self.top_frame, text="🦉 FRUGOLINGO ULTRA", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(side="left", padx=20)

        xp, streak = self.db.get_user_stats()
        self.streak_label = ctk.CTkLabel(
            self.top_frame, text=f"🔥 Streak: {streak} dni", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FF9500"
        )
        self.streak_label.pack(side="right", padx=15)

        self.xp_label = ctk.CTkLabel(
            self.top_frame, text=f"⚡ {xp} XP", font=ctk.CTkFont(size=14, weight="bold"), text_color="#30D158"
        )
        self.xp_label.pack(side="right", padx=15)

    def _build_mode_selector(self):
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(fill="x", padx=30, pady=(15, 0))

        modes = ["Classic Quiz", "Type Translation", "True / False", "Listening Test"]
        self.mode_buttons = {}

        for m in modes:
            btn = ctk.CTkButton(
                self.mode_frame,
                text=m,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#1D4ED8" if m == self.current_mode else "#334155",
                command=lambda mode_name=m: self.change_mode(mode_name)
            )
            btn.pack(side="left", expand=True, fill="x", padx=5)
            self.mode_buttons[m] = btn

    def change_mode(self, new_mode: str):
        self.current_mode = new_mode
        for m, btn in self.mode_buttons.items():
            btn.configure(fg_color="#1D4ED8" if m == new_mode else "#334155")
        self.load_session()

    def _build_main_container(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=12)
        self.progress_bar.pack(fill="x", padx=30, pady=(20, 10))
        self.progress_bar.set(0.0)

        self.card_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.card_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.word_label = ctk.CTkLabel(
            self.card_frame, text="Ładowanie...", font=ctk.CTkFont(size=30, weight="bold")
        )
        self.word_label.pack(pady=(15, 5))

        self.audio_btn = ctk.CTkButton(
            self.card_frame, text="🔊 Posłuchaj wymowy", width=140, height=30, command=self._play_audio
        )
        self.audio_btn.pack(pady=(0, 15))

        # --- RAMKI DLA RÓŻNYCH TRYBÓW ---

        # 1. Option Grid (Classic / Listening)
        self.options_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.option_buttons: List[ctk.CTkButton] = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.options_frame,
                text="",
                font=ctk.CTkFont(size=15),
                height=48,
                corner_radius=10,
                command=lambda idx=i: self.check_quiz_answer(idx)
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            self.option_buttons.append(btn)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # 2. Type Frame (PISANIE)
        self.type_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.input_entry = ctk.CTkEntry(
            self.type_frame, placeholder_text="Wpisz tłumaczenie po polsku...", font=ctk.CTkFont(size=16), width=350, height=45
        )
        self.input_entry.pack(side="left", padx=10)
        self.input_entry.bind("<Return>", lambda event: self.check_type_answer())

        self.submit_btn = ctk.CTkButton(
            self.type_frame, text="Sprawdź", font=ctk.CTkFont(size=15, weight="bold"), height=45, command=self.check_type_answer
        )
        self.submit_btn.pack(side="left", padx=10)

        # 3. True / False Frame
        self.tf_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.tf_word_sub = ctk.CTkLabel(self.tf_frame, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color="#60A5FA")
        self.tf_word_sub.pack(pady=(0, 15))

        self.tf_true_btn = ctk.CTkButton(
            self.tf_frame, text="✅ PRAWDA", fg_color="#10B981", hover_color="#059669", font=ctk.CTkFont(size=16, weight="bold"), width=150, height=50, command=lambda: self.check_tf_answer(True)
        )
        self.tf_true_btn.pack(side="left", padx=20)

        self.tf_false_btn = ctk.CTkButton(
            self.tf_frame, text="❌ FAŁSZ", fg_color="#EF4444", hover_color="#DC2626", font=ctk.CTkFont(size=16, weight="bold"), width=150, height=50, command=lambda: self.check_tf_answer(False)
        )
        self.tf_false_btn.pack(side="left", padx=20)

        # Przycisk restartu sesji
        self.reset_btn = ctk.CTkButton(
            self.card_frame, text="🔄 Rozpocznij nową sesję", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#F59E0B", hover_color="#D97706", command=self.reset_session
        )

        self.status_label = ctk.CTkLabel(
            self.main_frame, text="", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(pady=10)

    def load_session(self):
        self.current_cards = self.db.get_due_cards(limit=10)
        self.current_index = 0
        self.reset_btn.pack_forget()

        if not self.current_cards:
            self.word_label.configure(text="🎉 Powtórki ukończone!")
            self._hide_all_mode_frames()
            self.reset_btn.pack(pady=20)
            return

        self._render_card()

    def reset_session(self):
        self.db.reset_all_reviews()
        self.load_session()

    def _hide_all_mode_frames(self):
        self.options_frame.pack_forget()
        self.type_frame.pack_forget()
        self.tf_frame.pack_forget()

    def _render_card(self):
        if self.current_index >= len(self.current_cards):
            self._finish_session()
            return

        card = self.current_cards[self.current_index]
        self.correct_answer = card["word_pl"]
        self.status_label.configure(text="")
        self._hide_all_mode_frames()

        if self.current_mode == "Classic Quiz":
            self.word_label.configure(text=card["word_en"])
            self.audio_btn.pack(pady=(0, 15))
            self.tts.speak(card["word_en"])
            self._setup_quiz_options()
            self.options_frame.pack(fill="x", padx=40, pady=10)

        elif self.current_mode == "Type Translation":
            self.word_label.configure(text=card["word_en"])
            self.audio_btn.pack(pady=(0, 15))
            self.tts.speak(card["word_en"])
            self.input_entry.delete(0, 'end')
            self.type_frame.pack(pady=20)

        elif self.current_mode == "True / False":
            self.word_label.configure(text=card["word_en"])
            self.audio_btn.pack(pady=(0, 15))
            self.tts.speak(card["word_en"])
            
            self.tf_is_correct = random.choice([True, False])
            if self.tf_is_correct:
                display_pl = self.correct_answer
            else:
                other_words = [c["word_pl"] for c in self.current_cards if c["word_pl"] != self.correct_answer]
                display_pl = random.choice(other_words) if other_words else "Inne słowo"
            
            self.tf_word_sub.configure(text=f"Czy to oznacza: '{display_pl}'?")
            self.tf_frame.pack(pady=20)

        elif self.current_mode == "Listening Test":
            self.word_label.configure(text="🎧 Posłuchaj i wybierz!")
            self.audio_btn.pack(pady=(0, 15))
            self.tts.speak(card["word_en"])
            self._setup_quiz_options()
            self.options_frame.pack(fill="x", padx=40, pady=10)

        progress = self.current_index / len(self.current_cards)
        self.progress_bar.set(progress)

    def _setup_quiz_options(self):
        all_pl_words = [c["word_pl"] for c in self.current_cards if c["word_pl"] != self.correct_answer]
        fillers = random.sample(all_pl_words, min(3, len(all_pl_words)))
        while len(fillers) < 3:
            fillers.append("Inne tłumaczenie")

        self.options = fillers + [self.correct_answer]
        random.shuffle(self.options)

        for i, btn in enumerate(self.option_buttons):
            btn.configure(text=self.options[i], state="normal", fg_color=("#3B82F6", "#1D4ED8"))

    def _play_audio(self):
        if self.current_cards and self.current_index < len(self.current_cards):
            self.tts.speak(self.current_cards[self.current_index]["word_en"])

    def check_quiz_answer(self, option_index: int):
        selected = self.options[option_index]
        for btn in self.option_buttons:
            btn.configure(state="disabled")

        if selected == self.correct_answer:
            self.option_buttons[option_index].configure(fg_color="#10B981")
            self._handle_correct()
        else:
            self.option_buttons[option_index].configure(fg_color="#EF4444")
            self._handle_wrong()

    def check_type_answer(self):
        user_input = self.input_entry.get().strip().lower()
        if user_input == self.correct_answer.lower():
            self._handle_correct()
        else:
            self._handle_wrong()

    def check_tf_answer(self, user_choice: bool):
        if user_choice == self.tf_is_correct:
            self._handle_correct()
        else:
            self._handle_wrong()

    def _handle_correct(self):
        card = self.current_cards[self.current_index]
        self.status_label.configure(text="✨ Doskonale! (+15 XP)", text_color="#10B981")
        self.db.update_card_sm2(card["id"], quality=5)
        self.db.add_xp(15)
        self._update_top_bar()
        self.after(1300, self._next_question)

    def _handle_wrong(self):
        card = self.current_cards[self.current_index]
        self.status_label.configure(text=f"❌ Poprawnie: {self.correct_answer}", text_color="#EF4444")
        self.db.update_card_sm2(card["id"], quality=1)
        self.after(1800, self._next_question)

    def _update_top_bar(self):
        xp, streak = self.db.get_user_stats()
        self.xp_label.configure(text=f"⚡ {xp} XP")

    def _next_question(self):
        self.current_index += 1
        self._render_card()

    def _finish_session(self):
        self.progress_bar.set(1.0)
        self.word_label.configure(text="🏆 Sesja Ukończona!")
        self.audio_btn.pack_forget()
        self._hide_all_mode_frames()
        self.reset_btn.pack(pady=20)
        self.status_label.configure(text="Świetny trening! Kliknij przycisk poniżej, aby rozpocząć nową sesję.", text_color="#30D158")


if __name__ == "__main__":
    app = FrugolingoApp()
    app.mainloop()
