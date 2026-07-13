import customtkinter as ctk
import random
from typing import Dict, List, TypedDict

# Ustawienia wyglądu
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class Question(TypedDict):
    question: str
    options: List[str]
    answer: str
    explanation: str


# ==========================================
# 1. BAZA DANYCH / LOGIKA NAUKI (BACKEND)
# ==========================================
LESSON_DATA: Dict[str, List[Question]] = {
    "Angielski 🇬🇧": [
        {
            "question": "Jak powiesz 'Dzień dobry' w oficjalny sposób?",
            "options": ["Good morning", "Bye bye", "Good night", "See ya"],
            "answer": "Good morning",
            "explanation": "'Good morning' to formalne powitanie stosowane do południa.",
        },
        {
            "question": "Wybierz poprawne tłumaczenie słowa 'Apple':",
            "options": ["Gruszka", "Jabłko", "Śliwka", "Banan"],
            "answer": "Jabłko",
            "explanation": "'Apple' oznacza jabłko.",
        },
        {
            "question": "Uzupełnij zdanie: 'She ___ a student.'",
            "options": ["are", "am", "is", "be"],
            "answer": "is",
            "explanation": "Dla 3. osoby liczby pojedynczej (she/he/it) używamy 'is'.",
        },
    ],
    "Niemiecki 🇩🇪": [
        {
            "question": "Jak powiesz 'Dziękuję bardzo' po niemiecku?",
            "options": [
                "Vielen Dank",
                "Guten Tag",
                "Auf Wiedersehen",
                "Entschuldigung",
            ],
            "answer": "Vielen Dank",
            "explanation": "'Vielen Dank' oznacza 'Dziękuję bardzo'.",
        },
        {
            "question": "Jaki rodzajnik ma słowo 'Mädchen' (dziewczynka)?",
            "options": ["Der", "Die", "Das", "Den"],
            "answer": "Das",
            "explanation": "Wszystkie zdrobnienia kończące się na '-chen' mają rodzajnik 'das'.",
        },
    ],
    "Francuski 🇫🇷": [
        {
            "question": "Co oznacza słynne zwrot 'Bonjour'?",
            "options": ["Dobranoc", "Dzień dobry", "Do widzenia", "Przepraszam"],
            "answer": "Dzień dobry",
            "explanation": "'Bonjour' to podstawowe francuskie powitanie.",
        },
        {
            "question": "Jak powiesz 'Dziękuję' po francusku?",
            "options": ["Merci", "S'il vous plaît", "Oui", "Non"],
            "answer": "Merci",
            "explanation": "'Merci' oznacza 'Dziękuję'.",
        },
    ],
}


# ==========================================
# 2. INTERFEJS UŻYTKOWNIKA (FRONTEND / GUI)
# ==========================================
class FrugolingoApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Frugolingo - Naucz się języków z AI")
        self.geometry("850x600")
        self.resizable(False, False)

        # Statystyki gracza
        self.xp_points = 0
        self.streak = 1
        self.current_language = "Angielski 🇬🇧"
        self.questions: List[Question] = []
        self.current_q_idx = 0
        self.selected_option: str | None = None

        # Siatka główna
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_area()
        self._load_language_data(self.current_language)

    def _create_sidebar(self):
        """Panel boczny do nawigacji i statystyk."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🦉 Frugolingo",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.logo_label.pack(pady=(20, 10), padx=20)

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Twój asystent językowy",
            font=ctk.CTkFont(size=12, slant="italic"),
        )
        self.subtitle.pack(pady=(0, 20))

        # Statystyki
        self.stats_card = ctk.CTkFrame(self.sidebar)
        self.stats_card.pack(fill="x", padx=15, pady=10)

        self.lbl_streak = ctk.CTkLabel(
            self.stats_card,
            text=f"🔥 Seria: {self.streak} dni",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_streak.pack(pady=(10, 5))

        self.lbl_xp = ctk.CTkLabel(
            self.stats_card,
            text=f"⚡ Punkty XP: {self.xp_points}",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_xp.pack(pady=(5, 10))

        # Wybór Języka
        self.lbl_lang = ctk.CTkLabel(
            self.sidebar, text="Wybierz język:", font=ctk.CTkFont(weight="bold")
        )
        self.lbl_lang.pack(anchor="w", padx=20, pady=(20, 5))

        self.lang_option = ctk.CTkOptionMenu(
            self.sidebar,
            values=list(LESSON_DATA.keys()),
            command=self._on_language_change,
        )
        self.lang_option.pack(fill="x", padx=20, pady=(0, 20))

    def _create_main_area(self):
        """Główna przestrzeń lekcyjna."""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)

        # Pasek postępu lekcji
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=12)
        self.progress_bar.pack(fill="x", pady=(0, 20))
        self.progress_bar.set(0)

        # Karta Pytania
        self.question_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.question_card.pack(fill="x", ipady=15, pady=(0, 20))

        self.lbl_question = ctk.CTkLabel(
            self.question_card,
            text="Treść pytania...",
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=500,
        )
        self.lbl_question.pack(pady=20, padx=20)

        # Kontener na przyciski odpowiedzi
        self.options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", pady=(0, 20))

        self.option_buttons: List[ctk.CTkButton] = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.options_frame,
                text="",
                font=ctk.CTkFont(size=15),
                height=45,
                fg_color="#2b2b2b",
                hover_color="#3b3b3b",
                command=lambda idx=i: self._select_option(idx),
            )
            btn.pack(fill="x", pady=5)
            self.option_buttons.append(btn)

        # Feedback / Wyjaśnienie
        self.lbl_feedback = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=500,
        )
        self.lbl_feedback.pack(pady=(0, 10))

        # Przycisk Akcji (Sprawdź / Następne)
        self.btn_action = ctk.CTkButton(
            self.main_frame,
            text="Sprawdź",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27ae60",
            hover_color="#219150",
            command=self._check_or_next,
        )
        self.btn_action.pack(fill="x")

    def _load_language_data(self, lang: str):
        """Ładuje zestaw pytań dla wybranego języka."""
        self.current_language = lang
        self.questions = LESSON_DATA[lang].copy()
        random.shuffle(self.questions)
        self.current_q_idx = 0
        self._display_question()

    def _on_language_change(self, selected_lang: str):
        self._load_language_data(selected_lang)

    def _display_question(self):
        """Wyświetla aktualne pytanie i resetuje stan przycisków."""
        self.selected_option = None
        self.lbl_feedback.configure(text="")
        self.btn_action.configure(
            text="Sprawdź", state="normal", fg_color="#27ae60"
        )

        q_data = self.questions[self.current_q_idx]

        # Aktualizacja paska postępu
        progress = (self.current_q_idx) / len(self.questions)
        self.progress_bar.set(progress)

        self.lbl_question.configure(text=q_data["question"])

        # Reset wyglądu opcji
        for i, opt in enumerate(q_data["options"]):
            btn = self.option_buttons[i]
            btn.configure(
                text=opt,
                state="normal",
                fg_color="#2b2b2b",
                border_width=0,
            )

    def _select_option(self, idx: int):
        """Zaznacza wybraną odpowiedź."""
        self.selected_option = self.option_buttons[idx].cget("text")
        for i, btn in enumerate(self.option_buttons):
            if i == idx:
                btn.configure(fg_color="#2980b9")  # Niebieski akcent
            else:
                btn.configure(fg_color="#2b2b2b")

    def _check_or_next(self):
        """Obsługuje weryfikację odpowiedzi lub przejście do kolejnego pytania."""
        if self.btn_action.cget("text") == "Sprawdź":
            if not self.selected_option:
                self.lbl_feedback.configure(
                    text="⚠️ Wybierz odpowiedź!", text_color="#f1c40f"
                )
                return

            q_data = self.questions[self.current_q_idx]
            is_correct = self.selected_option == q_data["answer"]

            # Zablokuj przyciski opcji
            for btn in self.option_buttons:
                btn.configure(state="disabled")
                if btn.cget("text") == q_data["answer"]:
                    btn.configure(fg_color="#27ae60")  # Zielony dla poprawnej
                elif (
                    btn.cget("text") == self.selected_option and not is_correct
                ):
                    btn.configure(fg_color="#c0392b")  # Czerwony dla błędnej

            if is_correct:
                self.xp_points += 10
                self.lbl_xp.configure(text=f"⚡ Punkty XP: {self.xp_points}")
                self.lbl_feedback.configure(
                    text=f"🎉 Świetnie! {q_data['explanation']}",
                    text_color="#2ecc71",
                )
            else:
                self.lbl_feedback.configure(
                    text=f"❌ Poprawna odpowiedź: {q_data['answer']}\n{q_data['explanation']}",
                    text_color="#e74c3c",
                )

            self.btn_action.configure(text="Kontynuuj")

        else:
            # Przejście do następnego pytania
            self.current_q_idx += 1
            if self.current_q_idx < len(self.questions):
                self._display_question()
            else:
                self._finish_lesson()

    def _finish_lesson(self):
        """Ekran końcowy po przejściu lekcji."""
        self.progress_bar.set(1.0)
        self.lbl_question.configure(
            text=f"🏆 Gratulacje! Ukończyłeś moduł: {self.current_language}!"
        )

        for btn in self.option_buttons:
            btn.pack_forget()

        self.lbl_feedback.configure(
            text=f"Zdobyte punkty w tej sesji: +{len(self.questions) * 10} XP!",
            text_color="#f1c40f",
        )

        self.btn_action.configure(
            text="Zagraj ponownie",
            command=self._restart_lesson,
            fg_color="#2980b9",
        )

    def _restart_lesson(self):
        """Reset zestawu i przywrócenie widoku pytań."""
        for btn in self.option_buttons:
            btn.pack(fill="x", pady=5)
        self._load_language_data(self.current_language)
        self.btn_action.configure(command=self._check_or_next)


if __name__ == "__main__":
    app = FrugolingoApp()
    app.mainloop()