"""
LinguaMaster PRO - Nowoczesna aplikacja do nauki języków obcych (v2)
======================================================================
Autor: Claude (Anthropic)
Wymagania: pip install customtkinter --break-system-packages

NOWOŚCI W v2:
- Więcej słówek i kategorii dla każdego języka
- Wybór kategorii przed startem trybu (albo "wszystkie")
- Tryb "Powtórka błędów" - ćwiczy tylko słowa, które sprawiają Ci problem
- Tryb "Wyzwanie na czas" - quiz z odliczaniem czasu na pytanie
- System osiągnięć (odznaki) z ekranem "Osiągnięcia"
- System serii dni nauki (streak) z ikoną ognia
- Ekran Ustawienia (animacje wł/wył, reset postępów)
- Prawdziwe animacje: płynne wypełnianie pasków XP, flip fiszek 3D-like,
  konfetti po ukończeniu sesji, powiadomienia "toast", pulsowanie przycisków,
  animowany licznik wyniku, pierścień odliczania czasu
- 🤖 Asystent AI: czat z prawdziwym modelem Claude (Anthropic API), który zna
  wybrany język i pomaga z gramatyką, przykładami zdań i poprawianiem tekstu.
  Wymaga własnego klucza API wpisanego w Ustawieniach oraz: pip install anthropic

UWAGA O KLUCZU API:
Klucz jest zapisywany lokalnie w progress.json na Twoim dysku, żeby nie trzeba
było wpisywać go za każdym razem. Nie udostępniaj tego pliku innym osobom.
"""

import customtkinter as ctk
import tkinter as tk
import json
import os
import random
import math
import threading
from datetime import datetime, date, timedelta

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

AI_MODELS = {
    "Claude Haiku 4.5 (szybki)": "claude-haiku-4-5-20251001",
    "Claude Sonnet 5 (zbalansowany)": "claude-sonnet-5",
}

# ---------------------------------------------------------------------------
# KONFIGURACJA WYGLĄDU
# ---------------------------------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PROGRESS_FILE = "progress.json"

COLORS = {
    "bg": "#1a1a2e",
    "card": "#16213e",
    "card2": "#1f2b4d",
    "accent": "#0f3460",
    "highlight": "#e94560",
    "success": "#2ecc71",
    "error": "#e74c3c",
    "warning": "#f39c12",
    "text": "#f1f1f1",
    "muted": "#a0a0b0",
    "gold": "#ffd166",
}

CONFETTI_COLORS = ["#e94560", "#2ecc71", "#f39c12", "#3498db", "#ffd166", "#9b59b6"]

XP_PER_LEVEL = 100

# ---------------------------------------------------------------------------
# BAZA SŁÓWEK (rozszerzona)
# ---------------------------------------------------------------------------
VOCAB = {
    "Angielski": {"flag": "🇬🇧", "words": [
        ("hello", "cześć", "Podstawy"), ("goodbye", "do widzenia", "Podstawy"),
        ("please", "proszę", "Podstawy"), ("thank you", "dziękuję", "Podstawy"),
        ("yes", "tak", "Podstawy"), ("no", "nie", "Podstawy"), ("sorry", "przepraszam", "Podstawy"),
        ("water", "woda", "Jedzenie"), ("bread", "chleb", "Jedzenie"), ("apple", "jabłko", "Jedzenie"),
        ("coffee", "kawa", "Jedzenie"), ("cheese", "ser", "Jedzenie"), ("meat", "mięso", "Jedzenie"),
        ("soup", "zupa", "Jedzenie"), ("sugar", "cukier", "Jedzenie"),
        ("house", "dom", "Codzienność"), ("car", "samochód", "Codzienność"), ("book", "książka", "Codzienność"),
        ("friend", "przyjaciel", "Codzienność"), ("family", "rodzina", "Codzienność"), ("phone", "telefon", "Codzienność"),
        ("school", "szkoła", "Codzienność"), ("money", "pieniądze", "Codzienność"),
        ("to run", "biegać", "Czasowniki"), ("to eat", "jeść", "Czasowniki"), ("to sleep", "spać", "Czasowniki"),
        ("to work", "pracować", "Czasowniki"), ("to read", "czytać", "Czasowniki"), ("to speak", "mówić", "Czasowniki"),
        ("to buy", "kupować", "Czasowniki"), ("to love", "kochać", "Czasowniki"),
        ("beautiful", "piękny", "Przymiotniki"), ("fast", "szybki", "Przymiotniki"), ("happy", "szczęśliwy", "Przymiotniki"),
        ("big", "duży", "Przymiotniki"), ("small", "mały", "Przymiotniki"), ("cold", "zimny", "Przymiotniki"),
        ("airport", "lotnisko", "Podróże"), ("train station", "dworzec", "Podróże"), ("ticket", "bilet", "Podróże"),
        ("mountain", "góra", "Podróże"), ("hotel", "hotel", "Podróże"), ("map", "mapa", "Podróże"),
        ("weather", "pogoda", "Natura"), ("sun", "słońce", "Natura"), ("rain", "deszcz", "Natura"),
        ("tree", "drzewo", "Natura"), ("sea", "morze", "Natura"),
    ]},
    "Niemiecki": {"flag": "🇩🇪", "words": [
        ("hallo", "cześć", "Podstawy"), ("tschüss", "do widzenia", "Podstawy"),
        ("bitte", "proszę", "Podstawy"), ("danke", "dziękuję", "Podstawy"),
        ("ja", "tak", "Podstawy"), ("nein", "nie", "Podstawy"), ("Entschuldigung", "przepraszam", "Podstawy"),
        ("Wasser", "woda", "Jedzenie"), ("Brot", "chleb", "Jedzenie"), ("Apfel", "jabłko", "Jedzenie"),
        ("Kaffee", "kawa", "Jedzenie"), ("Käse", "ser", "Jedzenie"), ("Fleisch", "mięso", "Jedzenie"),
        ("Suppe", "zupa", "Jedzenie"), ("Zucker", "cukier", "Jedzenie"),
        ("Haus", "dom", "Codzienność"), ("Auto", "samochód", "Codzienność"), ("Buch", "książka", "Codzienność"),
        ("Freund", "przyjaciel", "Codzienność"), ("Familie", "rodzina", "Codzienność"), ("Telefon", "telefon", "Codzienność"),
        ("Schule", "szkoła", "Codzienność"), ("Geld", "pieniądze", "Codzienność"),
        ("laufen", "biegać", "Czasowniki"), ("essen", "jeść", "Czasowniki"), ("schlafen", "spać", "Czasowniki"),
        ("arbeiten", "pracować", "Czasowniki"), ("lesen", "czytać", "Czasowniki"), ("sprechen", "mówić", "Czasowniki"),
        ("kaufen", "kupować", "Czasowniki"), ("lieben", "kochać", "Czasowniki"),
        ("schön", "piękny", "Przymiotniki"), ("schnell", "szybki", "Przymiotniki"), ("glücklich", "szczęśliwy", "Przymiotniki"),
        ("groß", "duży", "Przymiotniki"), ("klein", "mały", "Przymiotniki"), ("kalt", "zimny", "Przymiotniki"),
        ("Flughafen", "lotnisko", "Podróże"), ("Bahnhof", "dworzec", "Podróże"), ("Ticket", "bilet", "Podróże"),
        ("Berg", "góra", "Podróże"), ("Hotel", "hotel", "Podróże"), ("Karte", "mapa", "Podróże"),
        ("Wetter", "pogoda", "Natura"), ("Sonne", "słońce", "Natura"), ("Regen", "deszcz", "Natura"),
        ("Baum", "drzewo", "Natura"), ("Meer", "morze", "Natura"),
    ]},
    "Hiszpański": {"flag": "🇪🇸", "words": [
        ("hola", "cześć", "Podstawy"), ("adiós", "do widzenia", "Podstawy"),
        ("por favor", "proszę", "Podstawy"), ("gracias", "dziękuję", "Podstawy"),
        ("sí", "tak", "Podstawy"), ("no", "nie", "Podstawy"), ("perdón", "przepraszam", "Podstawy"),
        ("agua", "woda", "Jedzenie"), ("pan", "chleb", "Jedzenie"), ("manzana", "jabłko", "Jedzenie"),
        ("café", "kawa", "Jedzenie"), ("queso", "ser", "Jedzenie"), ("carne", "mięso", "Jedzenie"),
        ("sopa", "zupa", "Jedzenie"), ("azúcar", "cukier", "Jedzenie"),
        ("casa", "dom", "Codzienność"), ("coche", "samochód", "Codzienność"), ("libro", "książka", "Codzienność"),
        ("amigo", "przyjaciel", "Codzienność"), ("familia", "rodzina", "Codzienność"), ("teléfono", "telefon", "Codzienność"),
        ("escuela", "szkoła", "Codzienność"), ("dinero", "pieniądze", "Codzienność"),
        ("correr", "biegać", "Czasowniki"), ("comer", "jeść", "Czasowniki"), ("dormir", "spać", "Czasowniki"),
        ("trabajar", "pracować", "Czasowniki"), ("leer", "czytać", "Czasowniki"), ("hablar", "mówić", "Czasowniki"),
        ("comprar", "kupować", "Czasowniki"), ("amar", "kochać", "Czasowniki"),
        ("hermoso", "piękny", "Przymiotniki"), ("rápido", "szybki", "Przymiotniki"), ("feliz", "szczęśliwy", "Przymiotniki"),
        ("grande", "duży", "Przymiotniki"), ("pequeño", "mały", "Przymiotniki"), ("frío", "zimny", "Przymiotniki"),
        ("aeropuerto", "lotnisko", "Podróże"), ("estación", "dworzec", "Podróże"), ("billete", "bilet", "Podróże"),
        ("montaña", "góra", "Podróże"), ("hotel", "hotel", "Podróże"), ("mapa", "mapa", "Podróże"),
        ("tiempo", "pogoda", "Natura"), ("sol", "słońce", "Natura"), ("lluvia", "deszcz", "Natura"),
        ("árbol", "drzewo", "Natura"), ("mar", "morze", "Natura"),
    ]},
    "Francuski": {"flag": "🇫🇷", "words": [
        ("bonjour", "cześć", "Podstawy"), ("au revoir", "do widzenia", "Podstawy"),
        ("s'il vous plaît", "proszę", "Podstawy"), ("merci", "dziękuję", "Podstawy"),
        ("oui", "tak", "Podstawy"), ("non", "nie", "Podstawy"), ("pardon", "przepraszam", "Podstawy"),
        ("eau", "woda", "Jedzenie"), ("pain", "chleb", "Jedzenie"), ("pomme", "jabłko", "Jedzenie"),
        ("café", "kawa", "Jedzenie"), ("fromage", "ser", "Jedzenie"), ("viande", "mięso", "Jedzenie"),
        ("soupe", "zupa", "Jedzenie"), ("sucre", "cukier", "Jedzenie"),
        ("maison", "dom", "Codzienność"), ("voiture", "samochód", "Codzienność"), ("livre", "książka", "Codzienność"),
        ("ami", "przyjaciel", "Codzienność"), ("famille", "rodzina", "Codzienność"), ("téléphone", "telefon", "Codzienność"),
        ("école", "szkoła", "Codzienność"), ("argent", "pieniądze", "Codzienność"),
        ("courir", "biegać", "Czasowniki"), ("manger", "jeść", "Czasowniki"), ("dormir", "spać", "Czasowniki"),
        ("travailler", "pracować", "Czasowniki"), ("lire", "czytać", "Czasowniki"), ("parler", "mówić", "Czasowniki"),
        ("acheter", "kupować", "Czasowniki"), ("aimer", "kochać", "Czasowniki"),
        ("beau", "piękny", "Przymiotniki"), ("rapide", "szybki", "Przymiotniki"), ("heureux", "szczęśliwy", "Przymiotniki"),
        ("grand", "duży", "Przymiotniki"), ("petit", "mały", "Przymiotniki"), ("froid", "zimny", "Przymiotniki"),
        ("aéroport", "lotnisko", "Podróże"), ("gare", "dworzec", "Podróże"), ("billet", "bilet", "Podróże"),
        ("montagne", "góra", "Podróże"), ("hôtel", "hotel", "Podróże"), ("carte", "mapa", "Podróże"),
        ("météo", "pogoda", "Natura"), ("soleil", "słońce", "Natura"), ("pluie", "deszcz", "Natura"),
        ("arbre", "drzewo", "Natura"), ("mer", "morze", "Natura"),
    ]},
    "Włoski": {"flag": "🇮🇹", "words": [
        ("ciao", "cześć", "Podstawy"), ("arrivederci", "do widzenia", "Podstawy"),
        ("per favore", "proszę", "Podstawy"), ("grazie", "dziękuję", "Podstawy"),
        ("sì", "tak", "Podstawy"), ("no", "nie", "Podstawy"), ("scusa", "przepraszam", "Podstawy"),
        ("acqua", "woda", "Jedzenie"), ("pane", "chleb", "Jedzenie"), ("mela", "jabłko", "Jedzenie"),
        ("caffè", "kawa", "Jedzenie"), ("formaggio", "ser", "Jedzenie"), ("carne", "mięso", "Jedzenie"),
        ("zuppa", "zupa", "Jedzenie"), ("zucchero", "cukier", "Jedzenie"),
        ("casa", "dom", "Codzienność"), ("macchina", "samochód", "Codzienność"), ("libro", "książka", "Codzienność"),
        ("amico", "przyjaciel", "Codzienność"), ("famiglia", "rodzina", "Codzienność"), ("telefono", "telefon", "Codzienność"),
        ("scuola", "szkoła", "Codzienność"), ("soldi", "pieniądze", "Codzienność"),
        ("correre", "biegać", "Czasowniki"), ("mangiare", "jeść", "Czasowniki"), ("dormire", "spać", "Czasowniki"),
        ("lavorare", "pracować", "Czasowniki"), ("leggere", "czytać", "Czasowniki"), ("parlare", "mówić", "Czasowniki"),
        ("comprare", "kupować", "Czasowniki"), ("amare", "kochać", "Czasowniki"),
        ("bello", "piękny", "Przymiotniki"), ("veloce", "szybki", "Przymiotniki"), ("felice", "szczęśliwy", "Przymiotniki"),
        ("grande", "duży", "Przymiotniki"), ("piccolo", "mały", "Przymiotniki"), ("freddo", "zimny", "Przymiotniki"),
        ("aeroporto", "lotnisko", "Podróże"), ("stazione", "dworzec", "Podróże"), ("biglietto", "bilet", "Podróże"),
        ("montagna", "góra", "Podróże"), ("hotel", "hotel", "Podróże"), ("mappa", "mapa", "Podróże"),
        ("tempo", "pogoda", "Natura"), ("sole", "słońce", "Natura"), ("pioggia", "deszcz", "Natura"),
        ("albero", "drzewo", "Natura"), ("mare", "morze", "Natura"),
    ]},
}

ACHIEVEMENTS = [
    {"id": "first_steps", "name": "Pierwsze kroki", "desc": "Udziel pierwszej odpowiedzi", "icon": "🌱",
     "cond": lambda p: sum(w["seen"] for w in p.data["words"].values()) >= 1},
    {"id": "getting_started", "name": "Rozpęd", "desc": "Osiągnij 5. poziom", "icon": "🚀",
     "cond": lambda p: p.data["level"] >= 5},
    {"id": "word_master", "name": "Mistrz słówek", "desc": "Poznaj 30 różnych słów", "icon": "📚",
     "cond": lambda p: len(p.data["words"]) >= 30},
    {"id": "perfectionist", "name": "Perfekcjonista", "desc": "Osiągnij 90% skuteczności (min. 20 prób)", "icon": "🎯",
     "cond": lambda p: p.overall_accuracy() >= 90 and sum(w["seen"] for w in p.data["words"].values()) >= 20},
    {"id": "streak_3", "name": "Trzy dni z rzędu", "desc": "Ucz się 3 dni pod rząd", "icon": "🔥",
     "cond": lambda p: p.data["streak"] >= 3},
    {"id": "streak_7", "name": "Tygodniowy zapał", "desc": "Ucz się 7 dni pod rząd", "icon": "🔥🔥",
     "cond": lambda p: p.data["streak"] >= 7},
    {"id": "polyglot", "name": "Poliglota", "desc": "Ćwicz w co najmniej 3 różnych językach", "icon": "🌍",
     "cond": lambda p: len({k.split(":")[0] for k in p.data["words"]}) >= 3},
    {"id": "veteran", "name": "Weteran", "desc": "Zdobądź 500 XP", "icon": "🏆",
     "cond": lambda p: p.data["xp"] >= 500},
    {"id": "sessions_10", "name": "Nawyk", "desc": "Ukończ 10 sesji nauki", "icon": "📅",
     "cond": lambda p: p.data["sessions"] >= 10},
]


# ---------------------------------------------------------------------------
# ZARZĄDZANIE POSTĘPAMI
# ---------------------------------------------------------------------------
class ProgressManager:
    def __init__(self, path=PROGRESS_FILE):
        self.path = path
        self.data = self._load()

    def _load(self):
        default = {"xp": 0, "level": 1, "words": {}, "sessions": 0, "last_played": None,
                   "streak": 0, "unlocked": [], "animations": True,
                   "api_key": "", "ai_model": "claude-haiku-4-5-20251001"}
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                default.update(loaded)
                return default
            except (json.JSONDecodeError, OSError):
                pass
        return default

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def word_key(self, lang, word):
        return f"{lang}:{word}"

    def get_word_stats(self, lang, word):
        return self.data["words"].get(self.word_key(lang, word), {"seen": 0, "correct": 0, "streak": 0})

    def record_answer(self, lang, word, correct):
        key = self.word_key(lang, word)
        stats = self.data["words"].get(key, {"seen": 0, "correct": 0, "streak": 0})
        stats["seen"] += 1
        if correct:
            stats["correct"] += 1
            stats["streak"] += 1
            self.add_xp(10)
        else:
            stats["streak"] = 0
            self.add_xp(2)
        self.data["words"][key] = stats
        self.save()

    def add_xp(self, amount):
        self.data["xp"] += amount
        self.data["level"] = self.data["xp"] // XP_PER_LEVEL + 1

    def mastery_weight(self, lang, word):
        stats = self.get_word_stats(lang, word)
        if stats["seen"] == 0:
            return 3.0
        accuracy = stats["correct"] / stats["seen"]
        return max(0.5, 3.0 - accuracy * 2.5 - stats["streak"] * 0.2)

    def word_accuracy(self, lang, word):
        stats = self.get_word_stats(lang, word)
        if stats["seen"] == 0:
            return None
        return stats["correct"] / stats["seen"]

    def worst_words(self, lang, n=10):
        words = VOCAB[lang]["words"]
        scored = []
        for w in words:
            acc = self.word_accuracy(lang, w[0])
            if acc is not None:
                scored.append((acc, w))
        scored.sort(key=lambda x: x[0])
        return [w for _, w in scored[:n]]

    def new_session(self):
        today = date.today()
        last = self.data.get("last_played")
        if last:
            last_date = datetime.fromisoformat(last).date()
            if last_date == today:
                pass
            elif last_date == today - timedelta(days=1):
                self.data["streak"] += 1
            else:
                self.data["streak"] = 1
        else:
            self.data["streak"] = 1
        self.data["sessions"] += 1
        self.data["last_played"] = datetime.now().isoformat(timespec="seconds")
        self.save()

    def overall_accuracy(self):
        seen = sum(w["seen"] for w in self.data["words"].values())
        correct = sum(w["correct"] for w in self.data["words"].values())
        return (correct / seen * 100) if seen else 0.0

    def check_new_achievements(self):
        newly = []
        for ach in ACHIEVEMENTS:
            if ach["id"] not in self.data["unlocked"] and ach["cond"](self):
                self.data["unlocked"].append(ach["id"])
                newly.append(ach)
        if newly:
            self.save()
        return newly

    def reset(self):
        self.data = {"xp": 0, "level": 1, "words": {}, "sessions": 0, "last_played": None,
                     "streak": 0, "unlocked": [], "animations": self.data.get("animations", True),
                     "api_key": self.data.get("api_key", ""), "ai_model": self.data.get("ai_model", "claude-haiku-4-5-20251001")}
        self.save()


# ---------------------------------------------------------------------------
# POMOCNICZE FUNKCJE ANIMACJI
# ---------------------------------------------------------------------------
def lerp_color(c1, c2, t):
    c1 = c1.lstrip("#"); c2 = c2.lstrip("#")
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
    r = int(r1 + (r2 - r1) * t); g = int(g1 + (g2 - g1) * t); b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class Toast(ctk.CTkFrame):
    """Powiadomienie 'toast' wjeżdżające od góry i znikające po chwili."""
    def __init__(self, master, text, color, duration=1300):
        super().__init__(master, fg_color=color, corner_radius=14, height=44)
        self.label = ctk.CTkLabel(self, text=text, font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color="#ffffff")
        self.label.pack(expand=True, padx=20, pady=8)
        self.master = master
        self.duration = duration
        self.place(relx=0.5, y=-50, anchor="n")
        self._animate_in()

    def _animate_in(self, y=-50, target=20, step=0):
        if step > 12:
            self.place(relx=0.5, y=target, anchor="n")
            self.after(self.duration, self._animate_out)
            return
        new_y = y + (target - y) * 0.35
        self.place(relx=0.5, y=new_y, anchor="n")
        self.after(15, lambda: self._animate_in(new_y, target, step + 1))

    def _animate_out(self, step=0):
        if step > 10 or not self.winfo_exists():
            try:
                self.destroy()
            except Exception:
                pass
            return
        try:
            info = self.place_info()
            y = float(info["y"])
            self.place(relx=0.5, y=y - 6, anchor="n")
            self.after(15, lambda: self._animate_out(step + 1))
        except Exception:
            pass


class ConfettiCanvas(tk.Canvas):
    """Prosty efekt konfetti spadającego po ukończeniu sesji."""
    def __init__(self, master, width, height, count=40):
        super().__init__(master, width=width, height=height, bg=COLORS["bg"],
                         highlightthickness=0)
        self.pieces = []
        for _ in range(count):
            x = random.randint(0, width)
            y = random.randint(-height, 0)
            size = random.randint(6, 12)
            color = random.choice(CONFETTI_COLORS)
            shape = self.create_rectangle(x, y, x + size, y + size, fill=color, outline="")
            vy = random.uniform(2, 5)
            vx = random.uniform(-1.5, 1.5)
            rot = random.uniform(-3, 3)
            self.pieces.append([shape, vx, vy, rot])
        self.height = height
        self.width = width
        self.frames_left = 90
        self._animate()

    def _animate(self):
        if self.frames_left <= 0 or not self.winfo_exists():
            try:
                self.destroy()
            except Exception:
                pass
            return
        for piece in self.pieces:
            shape, vx, vy, rot = piece
            try:
                self.move(shape, vx, vy)
            except Exception:
                continue
        self.frames_left -= 1
        self.after(16, self._animate)


# ---------------------------------------------------------------------------
# GŁÓWNA APLIKACJA
# ---------------------------------------------------------------------------
class LinguaMasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LinguaMaster PRO — Nowoczesna Nauka Języków")
        self.geometry("960x700")
        self.minsize(800, 600)
        self.configure(fg_color=COLORS["bg"])

        self.progress = ProgressManager()
        self.progress.new_session()

        self.current_lang = "Angielski"
        self.current_category = "Wszystkie"

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_main_menu()
        self.after(400, self._check_and_toast_achievements)

    # ------------------------------------------------------------------
    def animations_on(self):
        return self.progress.data.get("animations", True)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def toast(self, text, kind="success"):
        color = {"success": COLORS["success"], "error": COLORS["error"],
                 "gold": COLORS["gold"], "info": COLORS["accent"]}.get(kind, COLORS["accent"])
        Toast(self, text, color)

    def top_bar(self, title):
        bar = ctk.CTkFrame(self.container, fg_color="transparent")
        bar.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(bar, text=title, font=ctk.CTkFont(size=26, weight="bold"),
                     text_color=COLORS["text"]).pack(side="left")

        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right")
        streak = self.progress.data.get("streak", 0)
        if streak > 0:
            ctk.CTkLabel(right, text=f"🔥 {streak} dni", font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLORS["warning"]).pack(side="right", padx=(15, 0))
        stats_txt = f"⭐ Poziom {self.progress.data['level']}   XP: {self.progress.data['xp']}"
        ctk.CTkLabel(right, text=stats_txt, font=ctk.CTkFont(size=14),
                     text_color=COLORS["muted"]).pack(side="right")

        # animowany pasek XP pod górnym paskiem
        xp_in_level = self.progress.data["xp"] % XP_PER_LEVEL
        bar_bg = ctk.CTkFrame(self.container, fg_color=COLORS["accent"], height=10, corner_radius=5)
        bar_bg.pack(fill="x", pady=(0, 15))
        self._animated_bar(bar_bg, xp_in_level / XP_PER_LEVEL)

    def _animated_bar(self, bar_bg, target_pct, color=None):
        color = color or COLORS["success"]
        fill = ctk.CTkFrame(bar_bg, fg_color=color, height=10, corner_radius=5, width=0)
        fill.place(x=0, y=0, relheight=1)
        if not self.animations_on():
            bar_bg.update_idletasks()
            w = bar_bg.winfo_width() or 800
            fill.configure(width=max(2, int(w * target_pct)))
            return fill

        def step(pct=0.0):
            if not bar_bg.winfo_exists():
                return
            bar_bg.update_idletasks()
            w = bar_bg.winfo_width() or 800
            pct = min(pct + 0.03, target_pct)
            fill.configure(width=max(2, int(w * pct)))
            if pct < target_pct:
                self.after(12, lambda: step(pct))
        self.after(50, step)
        return fill

    def back_button(self):
        ctk.CTkButton(self.container, text="← Powrót do menu", width=160, corner_radius=12,
                      fg_color=COLORS["accent"], hover_color=COLORS["highlight"],
                      command=self.show_main_menu).pack(pady=15)

    def _check_and_toast_achievements(self):
        newly = self.progress.check_new_achievements()
        for i, ach in enumerate(newly):
            self.after(i * 1500, lambda a=ach: self.toast(f"{a['icon']} Odznaka: {a['name']}!", "gold"))

    # ------------------------------------------------------------------
    # EKRAN GŁÓWNY
    # ------------------------------------------------------------------
    def show_main_menu(self):
        self.clear_container()
        self.top_bar(f"LinguaMaster PRO  {VOCAB[self.current_lang]['flag']} {self.current_lang}")

        ctk.CTkLabel(self.container, text="Wybierz język do nauki:",
                     font=ctk.CTkFont(size=15), text_color=COLORS["muted"]).pack(pady=(5, 5))

        lang_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        lang_frame.pack(pady=(0, 15))
        for lang, info in VOCAB.items():
            btn = ctk.CTkButton(
                lang_frame, text=f"{info['flag']} {lang}", width=130, height=42,
                corner_radius=14, font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLORS["accent"] if lang != self.current_lang else COLORS["highlight"],
                hover_color=COLORS["highlight"],
                command=lambda l=lang: self.select_language(l),
            )
            btn.pack(side="left", padx=5)

        modes = [
            ("🃏 Fiszki", self.start_flashcards, "Ucz się nowych słówek."),
            ("❓ Quiz ABCD", self.start_quiz, "4 opcje do wyboru."),
            ("⌨️ Pisanie", self.start_typing, "Wpisz tłumaczenie."),
            ("🧩 Dopasowywanie", self.start_matching, "Połącz pary słów."),
            ("⏱️ Na czas", self.start_timed_challenge, "Quiz z odliczaniem."),
            ("🔁 Powtórka błędów", self.start_review, "Trudne słowa dla Ciebie."),
            ("🤖 Asystent AI", self.start_ai_assistant, "Zapytaj o gramatykę i zdania."),
            ("🏅 Osiągnięcia", self.show_achievements, "Twoje odznaki."),
            ("📊 Statystyki", self.show_stats, "Zobacz postępy."),
            ("⚙️ Ustawienia", self.show_settings, "Animacje, reset."),
        ]
        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(pady=5, fill="both", expand=True)

        for i, (label, cmd, desc) in enumerate(modes):
            card = ctk.CTkFrame(grid, fg_color=COLORS["card"], corner_radius=16)
            card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
            grid.grid_columnconfigure(i % 3, weight=1)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=17, weight="bold"),
                         text_color=COLORS["text"]).pack(pady=(14, 3), padx=12)
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=11), wraplength=170,
                         text_color=COLORS["muted"], justify="center").pack(pady=(0, 8), padx=12)
            b = ctk.CTkButton(card, text="Start", width=90, corner_radius=12,
                              fg_color=COLORS["highlight"], hover_color="#c73650", command=cmd)
            b.pack(pady=(0, 14))
            self._hover_pulse(b)

    def _hover_pulse(self, button):
        """Delikatne 'oddychanie' przycisku po najechaniu myszką."""
        if not self.animations_on():
            return
        state = {"growing": True, "scale": 90}

        def pulse():
            if not button.winfo_exists():
                return
            try:
                if button.instate is None:
                    pass
            except Exception:
                pass
        # lekki efekt: zmiana koloru obramowania przy hover (CTk obsługuje hover natywnie)
        button.bind("<Enter>", lambda e: button.configure(border_width=2, border_color=COLORS["gold"]))
        button.bind("<Leave>", lambda e: button.configure(border_width=0))

    def select_language(self, lang):
        self.current_lang = lang
        self.current_category = "Wszystkie"
        self.show_main_menu()

    def get_categories(self, lang):
        cats = sorted({w[2] for w in VOCAB[lang]["words"]})
        return ["Wszystkie"] + cats

    def filtered_words(self, lang, category):
        if category == "Wszystkie":
            return VOCAB[lang]["words"]
        return [w for w in VOCAB[lang]["words"] if w[2] == category]

    def get_weighted_words(self, lang, n, category="Wszystkie"):
        words = self.filtered_words(lang, category)
        weights = [self.progress.mastery_weight(lang, w[0]) for w in words]
        n = min(n, len(words))
        pool = list(zip(words, weights))
        chosen = []
        for _ in range(n):
            total = sum(w for _, w in pool)
            r = random.uniform(0, total)
            upto = 0
            for item, w in pool:
                upto += w
                if upto >= r:
                    chosen.append(item)
                    pool.remove((item, w))
                    break
        return chosen

    def category_picker(self, on_choose):
        """Mały ekran wyboru kategorii przed rozpoczęciem trybu."""
        self.clear_container()
        self.top_bar(f"Wybierz kategorię — {self.current_lang}")
        cats = self.get_categories(self.current_lang)
        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(pady=20)
        for i, cat in enumerate(cats):
            count = len(self.filtered_words(self.current_lang, cat))
            b = ctk.CTkButton(grid, text=f"{cat} ({count})", width=200, height=48, corner_radius=14,
                              font=ctk.CTkFont(size=14, weight="bold"),
                              fg_color=COLORS["accent"], hover_color=COLORS["highlight"],
                              command=lambda c=cat: on_choose(c))
            b.grid(row=i // 3, column=i % 3, padx=8, pady=8)
        self.back_button()

    # ------------------------------------------------------------------
    # TRYB: FISZKI (z animacją flip)
    # ------------------------------------------------------------------
    def start_flashcards(self):
        self.category_picker(self._start_flashcards_with_category)

    def _start_flashcards_with_category(self, category):
        self.current_category = category
        self.clear_container()
        self.top_bar("🃏 Fiszki")
        self.fc_words = self.get_weighted_words(self.current_lang, 10, category)
        self.fc_index = 0
        self.fc_show_translation = False
        self.fc_render()

    def fc_render(self):
        for w in self.container.winfo_children()[2:]:
            w.destroy()

        if self.fc_index >= len(self.fc_words):
            self._show_completion("🎉 Ukończono serię fiszek!")
            return

        word, translation, category = self.fc_words[self.fc_index]
        progress_txt = f"Fiszka {self.fc_index + 1} / {len(self.fc_words)}   •   {category}"
        ctk.CTkLabel(self.container, text=progress_txt, font=ctk.CTkFont(size=13),
                     text_color=COLORS["muted"]).pack(pady=(5, 15))

        self.fc_card_holder = ctk.CTkFrame(self.container, fg_color="transparent")
        self.fc_card_holder.pack(pady=10)
        self.fc_card = ctk.CTkFrame(self.fc_card_holder, fg_color=COLORS["card"], corner_radius=24,
                                    width=500, height=240)
        self.fc_card.pack()
        self.fc_card.pack_propagate(False)

        self.fc_label = ctk.CTkLabel(self.fc_card, text=word, font=ctk.CTkFont(size=32, weight="bold"),
                                     text_color=COLORS["text"])
        self.fc_label.pack(expand=True)
        self.fc_hint = ctk.CTkLabel(self.fc_card, text="Kliknij, aby zobaczyć tłumaczenie",
                                    font=ctk.CTkFont(size=12), text_color=COLORS["muted"])
        self.fc_hint.pack(pady=(0, 15))

        for widget in (self.fc_card, self.fc_label, self.fc_hint):
            widget.bind("<Button-1>", lambda e: self.fc_flip())

        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="❌ Nie znałem", width=150, corner_radius=12,
                      fg_color=COLORS["error"], hover_color="#c0392b",
                      command=lambda: self.fc_next(False)).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="✅ Znałem", width=150, corner_radius=12,
                      fg_color=COLORS["success"], hover_color="#27ae60",
                      command=lambda: self.fc_next(True)).pack(side="left", padx=10)

        self.back_button()

    def fc_flip(self):
        """Animacja 'flip' - karta zwęża się do 0, zmienia treść, rozszerza z powrotem."""
        word, translation, category = self.fc_words[self.fc_index]
        self.fc_show_translation = not self.fc_show_translation
        new_text = translation if self.fc_show_translation else word
        new_color = COLORS["success"] if self.fc_show_translation else COLORS["text"]
        new_hint = "Tłumaczenie — kliknij, by wrócić" if self.fc_show_translation else "Kliknij, aby zobaczyć tłumaczenie"

        if not self.animations_on():
            self.fc_label.configure(text=new_text, text_color=new_color)
            self.fc_hint.configure(text=new_hint)
            return

        full_width = 500
        def shrink(w=full_width):
            if w <= 20:
                self.fc_label.configure(text=new_text, text_color=new_color)
                self.fc_hint.configure(text=new_hint)
                grow(20)
                return
            self.fc_card.configure(width=w)
            self.after(8, lambda: shrink(w - 45))

        def grow(w=20):
            if w >= full_width:
                self.fc_card.configure(width=full_width)
                return
            self.fc_card.configure(width=w)
            self.after(8, lambda: grow(w + 45))

        shrink()

    def fc_next(self, knew_it):
        word = self.fc_words[self.fc_index][0]
        self.progress.record_answer(self.current_lang, word, knew_it)
        self.fc_index += 1
        self.fc_show_translation = False
        self.fc_render()

    def _show_completion(self, message, subtext=None):
        for w in self.container.winfo_children()[2:]:
            w.destroy()
        wrap = ctk.CTkFrame(self.container, fg_color="transparent")
        wrap.pack(fill="both", expand=True)
        if self.animations_on():
            confetti = ConfettiCanvas(wrap, 900, 200)
            confetti.place(relx=0.5, y=0, anchor="n")
        ctk.CTkLabel(wrap, text=message, font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLORS["success"]).pack(pady=(60, 5))
        if subtext:
            ctk.CTkLabel(wrap, text=subtext, font=ctk.CTkFont(size=15),
                         text_color=COLORS["muted"]).pack(pady=5)
        self.back_button()
        self._check_and_toast_achievements()

    # ------------------------------------------------------------------
    # TRYB: QUIZ ABCD
    # ------------------------------------------------------------------
    def start_quiz(self):
        self.category_picker(self._start_quiz_with_category)

    def _start_quiz_with_category(self, category):
        self.current_category = category
        self.clear_container()
        self.top_bar("❓ Quiz ABCD")
        self.quiz_words = self.get_weighted_words(self.current_lang, 8, category)
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_render()

    def quiz_render(self):
        for w in self.container.winfo_children()[2:]:
            w.destroy()

        if self.quiz_index >= len(self.quiz_words):
            self._show_completion("🏁 Quiz zakończony!", f"Wynik: {self.quiz_score} / {len(self.quiz_words)}")
            return

        word, correct_translation, category = self.quiz_words[self.quiz_index]
        all_words = VOCAB[self.current_lang]["words"]
        distractors = random.sample(
            [w[1] for w in all_words if w[1] != correct_translation],
            min(3, len(all_words) - 1))
        options = distractors + [correct_translation]
        random.shuffle(options)

        ctk.CTkLabel(self.container, text=f"Pytanie {self.quiz_index + 1} / {len(self.quiz_words)}",
                     font=ctk.CTkFont(size=13), text_color=COLORS["muted"]).pack(pady=(5, 8))
        ctk.CTkLabel(self.container, text=f'Jak przetłumaczyć: "{word}" ?',
                     font=ctk.CTkFont(size=26, weight="bold"), text_color=COLORS["text"]).pack(pady=18)

        self.quiz_feedback = ctk.CTkLabel(self.container, text="", font=ctk.CTkFont(size=14))
        self.quiz_feedback.pack(pady=5)

        opt_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        opt_frame.pack(pady=10)
        self.quiz_buttons = []
        for i, opt in enumerate(options):
            b = ctk.CTkButton(opt_frame, text=opt, width=220, height=50, corner_radius=14,
                              font=ctk.CTkFont(size=15), fg_color=COLORS["accent"],
                              hover_color=COLORS["highlight"],
                              command=lambda o=opt, cw=correct_translation, wd=word: self.quiz_answer(o, cw, wd))
            b.grid(row=i // 2, column=i % 2, padx=8, pady=8)
            self.quiz_buttons.append(b)

        self.back_button()

    def quiz_answer(self, chosen, correct, word):
        for b in self.quiz_buttons:
            b.configure(state="disabled")
            if b.cget("text") == correct:
                b.configure(fg_color=COLORS["success"])
            elif b.cget("text") == chosen:
                b.configure(fg_color=COLORS["error"])
        is_correct = chosen == correct
        if is_correct:
            self.quiz_score += 1
            self.quiz_feedback.configure(text="✅ Poprawnie!", text_color=COLORS["success"])
        else:
            self.quiz_feedback.configure(text=f"❌ Poprawna odpowiedź: {correct}", text_color=COLORS["error"])
        self.progress.record_answer(self.current_lang, word, is_correct)
        self.quiz_index += 1
        self.after(1000, self.quiz_render)

    # ------------------------------------------------------------------
    # TRYB: WYZWANIE NA CZAS (nowość) — pierścień odliczania
    # ------------------------------------------------------------------
    def start_timed_challenge(self):
        self.clear_container()
        self.top_bar("⏱️ Wyzwanie na czas")
        self.timed_words = self.get_weighted_words(self.current_lang, 10, "Wszystkie")
        self.timed_index = 0
        self.timed_score = 0
        self.timed_seconds_left = 8
        self.timed_timer_job = None
        self.timed_render()

    def timed_render(self):
        for w in self.container.winfo_children()[2:]:
            w.destroy()
        if self.timed_timer_job:
            self.after_cancel(self.timed_timer_job)

        if self.timed_index >= len(self.timed_words):
            self._show_completion("🏁 Wyzwanie ukończone!", f"Wynik: {self.timed_score} / {len(self.timed_words)}")
            return

        word, correct_translation, category = self.timed_words[self.timed_index]
        all_words = VOCAB[self.current_lang]["words"]
        distractors = random.sample(
            [w[1] for w in all_words if w[1] != correct_translation],
            min(3, len(all_words) - 1))
        options = distractors + [correct_translation]
        random.shuffle(options)

        ctk.CTkLabel(self.container, text=f"Pytanie {self.timed_index + 1} / {len(self.timed_words)}",
                     font=ctk.CTkFont(size=13), text_color=COLORS["muted"]).pack(pady=(5, 5))

        self.timed_canvas = tk.Canvas(self.container, width=90, height=90, bg=COLORS["bg"], highlightthickness=0)
        self.timed_canvas.pack(pady=5)
        self.timed_seconds_left = 8
        self.timed_arc = self.timed_canvas.create_arc(5, 5, 85, 85, start=90, extent=359,
                                                       fill=COLORS["success"], outline="")
        self.timed_text = self.timed_canvas.create_text(45, 45, text="8", font=("Arial", 20, "bold"),
                                                         fill=COLORS["text"])

        ctk.CTkLabel(self.container, text=f'Jak przetłumaczyć: "{word}" ?',
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["text"]).pack(pady=12)

        opt_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        opt_frame.pack(pady=10)
        self.timed_buttons = []
        for i, opt in enumerate(options):
            b = ctk.CTkButton(opt_frame, text=opt, width=220, height=48, corner_radius=14,
                              font=ctk.CTkFont(size=14), fg_color=COLORS["accent"],
                              hover_color=COLORS["highlight"],
                              command=lambda o=opt, cw=correct_translation, wd=word: self.timed_answer(o, cw, wd))
            b.grid(row=i // 2, column=i % 2, padx=8, pady=6)
            self.timed_buttons.append(b)

        self.back_button()
        self._timed_tick(word, correct_translation)

    def _timed_tick(self, word, correct):
        if not hasattr(self, "timed_canvas") or not self.timed_canvas.winfo_exists():
            return
        total = 8
        pct = self.timed_seconds_left / total
        extent = max(1, int(359 * pct))
        color = COLORS["success"] if pct > 0.5 else (COLORS["warning"] if pct > 0.25 else COLORS["error"])
        self.timed_canvas.itemconfig(self.timed_arc, extent=extent, fill=color)
        self.timed_canvas.itemconfig(self.timed_text, text=str(max(0, int(self.timed_seconds_left))))

        if self.timed_seconds_left <= 0:
            self.timed_answer(None, correct, word)
            return
        self.timed_seconds_left -= 0.2
        self.timed_timer_job = self.after(200, lambda: self._timed_tick(word, correct))

    def timed_answer(self, chosen, correct, word):
        if self.timed_timer_job:
            self.after_cancel(self.timed_timer_job)
            self.timed_timer_job = None
        for b in self.timed_buttons:
            b.configure(state="disabled")
            if b.cget("text") == correct:
                b.configure(fg_color=COLORS["success"])
            elif b.cget("text") == chosen:
                b.configure(fg_color=COLORS["error"])
        is_correct = chosen == correct
        if is_correct:
            self.timed_score += 1
            self.toast("✅ Świetnie!", "success")
        else:
            self.toast(f"❌ To było: {correct}", "error")
        self.progress.record_answer(self.current_lang, word, is_correct)
        self.timed_index += 1
        self.after(900, self.timed_render)

    # ------------------------------------------------------------------
    # TRYB: PISANIE
    # ------------------------------------------------------------------
    def start_typing(self):
        self.category_picker(self._start_typing_with_category)

    def _start_typing_with_category(self, category):
        self.current_category = category
        self.clear_container()
        self.top_bar("⌨️ Pisanie")
        self.typing_words = self.get_weighted_words(self.current_lang, 8, category)
        self.typing_index = 0
        self.typing_score = 0
        self.typing_render()

    def typing_render(self):
        for w in self.container.winfo_children()[2:]:
            w.destroy()

        if self.typing_index >= len(self.typing_words):
            self._show_completion("🏁 Ukończono!", f"Wynik: {self.typing_score} / {len(self.typing_words)}")
            return

        word, correct_translation, category = self.typing_words[self.typing_index]
        ctk.CTkLabel(self.container, text=f"Słowo {self.typing_index + 1} / {len(self.typing_words)}",
                     font=ctk.CTkFont(size=13), text_color=COLORS["muted"]).pack(pady=(5, 10))
        ctk.CTkLabel(self.container, text=f'Przetłumacz na polski: "{word}"',
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["text"]).pack(pady=18)

        self.typing_entry = ctk.CTkEntry(self.container, width=300, height=45, corner_radius=12,
                                          font=ctk.CTkFont(size=16), justify="center",
                                          placeholder_text="Wpisz tłumaczenie...")
        self.typing_entry.pack(pady=10)
        self.typing_entry.bind("<Return>", lambda e: self.typing_check(word, correct_translation))
        self.typing_entry.focus()

        self.typing_feedback = ctk.CTkLabel(self.container, text="", font=ctk.CTkFont(size=14))
        self.typing_feedback.pack(pady=8)

        ctk.CTkButton(self.container, text="Sprawdź", width=160, corner_radius=12,
                      fg_color=COLORS["highlight"], hover_color="#c73650",
                      command=lambda: self.typing_check(word, correct_translation)).pack(pady=10)

        self.back_button()

    def typing_check(self, word, correct):
        answer = self.typing_entry.get().strip().lower()
        is_correct = answer == correct.lower()
        if is_correct:
            self.typing_score += 1
            self.typing_feedback.configure(text="✅ Poprawnie!", text_color=COLORS["success"])
        else:
            self.typing_feedback.configure(text=f"❌ Poprawna odpowiedź: {correct}", text_color=COLORS["error"])
        self.typing_entry.configure(state="disabled")
        self.progress.record_answer(self.current_lang, word, is_correct)
        self.typing_index += 1
        self.after(1200, self.typing_render)

    # ------------------------------------------------------------------
    # TRYB: DOPASOWYWANIE PAR
    # ------------------------------------------------------------------
    def start_matching(self):
        self.category_picker(self._start_matching_with_category)

    def _start_matching_with_category(self, category):
        self.current_category = category
        self.clear_container()
        self.top_bar("🧩 Dopasowywanie par")
        pairs = self.get_weighted_words(self.current_lang, 6, category)
        self.match_pairs = {w: t for w, t, c in pairs}
        left = list(self.match_pairs.keys())
        right = list(self.match_pairs.values())
        random.shuffle(left); random.shuffle(right)
        self.match_selected_left = None
        self.match_selected_right = None
        self.match_solved = set()
        self.match_left_buttons = {}
        self.match_right_buttons = {}

        ctk.CTkLabel(self.container, text="Kliknij słowo, a potem jego tłumaczenie:",
                     font=ctk.CTkFont(size=14), text_color=COLORS["muted"]).pack(pady=(5, 15))

        cols = ctk.CTkFrame(self.container, fg_color="transparent")
        cols.pack(pady=5)
        left_col = ctk.CTkFrame(cols, fg_color="transparent"); left_col.pack(side="left", padx=30)
        right_col = ctk.CTkFrame(cols, fg_color="transparent"); right_col.pack(side="left", padx=30)

        for w in left:
            b = ctk.CTkButton(left_col, text=w, width=180, height=42, corner_radius=12,
                              fg_color=COLORS["accent"], hover_color=COLORS["highlight"],
                              command=lambda word=w: self.match_pick_left(word))
            b.pack(pady=6); self.match_left_buttons[w] = b
        for t in right:
            b = ctk.CTkButton(right_col, text=t, width=180, height=42, corner_radius=12,
                              fg_color=COLORS["accent"], hover_color=COLORS["highlight"],
                              command=lambda trans=t: self.match_pick_right(trans))
            b.pack(pady=6); self.match_right_buttons[t] = b

        self.match_status = ctk.CTkLabel(self.container, text="", font=ctk.CTkFont(size=14))
        self.match_status.pack(pady=15)
        self.back_button()

    def match_pick_left(self, word):
        if word in self.match_solved: return
        self.match_selected_left = word
        for w, b in self.match_left_buttons.items():
            if w not in self.match_solved:
                b.configure(fg_color=COLORS["highlight"] if w == word else COLORS["accent"])
        self.match_try_solve()

    def match_pick_right(self, trans):
        solved_trans = [self.match_pairs[w] for w in self.match_solved]
        if trans in solved_trans: return
        self.match_selected_right = trans
        for t, b in self.match_right_buttons.items():
            if t not in solved_trans:
                b.configure(fg_color=COLORS["highlight"] if t == trans else COLORS["accent"])
        self.match_try_solve()

    def match_try_solve(self):
        if self.match_selected_left is None or self.match_selected_right is None:
            return
        word, trans = self.match_selected_left, self.match_selected_right
        correct = self.match_pairs.get(word) == trans
        self.progress.record_answer(self.current_lang, word, correct)
        if correct:
            self.match_solved.add(word)
            self.match_left_buttons[word].configure(fg_color=COLORS["success"], state="disabled")
            self.match_right_buttons[trans].configure(fg_color=COLORS["success"], state="disabled")
            self.match_status.configure(text="✅ Dopasowano!", text_color=COLORS["success"])
        else:
            self.match_left_buttons[word].configure(fg_color=COLORS["error"])
            self.match_right_buttons[trans].configure(fg_color=COLORS["error"])
            self.match_status.configure(text="❌ Spróbuj ponownie", text_color=COLORS["error"])
            lw, rt = word, trans
            self.after(500, lambda: self.match_left_buttons[lw].configure(fg_color=COLORS["accent"])
                       if lw not in self.match_solved and self.match_left_buttons.get(lw) and self.match_left_buttons[lw].winfo_exists() else None)
            self.after(500, lambda: self.match_right_buttons[rt].configure(fg_color=COLORS["accent"])
                       if lw not in self.match_solved and self.match_right_buttons.get(rt) and self.match_right_buttons[rt].winfo_exists() else None)
        self.match_selected_left = None
        self.match_selected_right = None
        if len(self.match_solved) == len(self.match_pairs):
            self.match_status.configure(text="🎉 Wszystkie pary dopasowane!", text_color=COLORS["success"])
            if self.animations_on():
                confetti = ConfettiCanvas(self.container, 900, 150)
                confetti.place(relx=0.5, rely=1.0, anchor="s")
            self._check_and_toast_achievements()

    # ------------------------------------------------------------------
    # TRYB: POWTÓRKA BŁĘDÓW (nowość)
    # ------------------------------------------------------------------
    def start_review(self):
        self.clear_container()
        self.top_bar("🔁 Powtórka błędów")
        worst = self.progress.worst_words(self.current_lang, 10)
        if not worst:
            ctk.CTkLabel(self.container, text="Brak jeszcze wystarczających danych.\nPopraw kilka słówek w innych trybach!",
                         font=ctk.CTkFont(size=16), text_color=COLORS["muted"], justify="center").pack(pady=60)
            self.back_button()
            return
        self.review_words = worst
        self.review_index = 0
        self.review_score = 0
        self.review_render()

    def review_render(self):
        for w in self.container.winfo_children()[2:]:
            w.destroy()

        if self.review_index >= len(self.review_words):
            self._show_completion("🔁 Powtórka zakończona!", f"Wynik: {self.review_score} / {len(self.review_words)}")
            return

        word, correct_translation, category = self.review_words[self.review_index]
        acc = self.progress.word_accuracy(self.current_lang, word)
        acc_txt = f"(dotychczasowa skuteczność: {acc*100:.0f}%)" if acc is not None else ""

        ctk.CTkLabel(self.container, text=f"Trudne słowo {self.review_index + 1} / {len(self.review_words)} {acc_txt}",
                     font=ctk.CTkFont(size=13), text_color=COLORS["warning"]).pack(pady=(5, 10))
        ctk.CTkLabel(self.container, text=f'Przetłumacz: "{word}"',
                     font=ctk.CTkFont(size=26, weight="bold"), text_color=COLORS["text"]).pack(pady=18)

        self.review_entry = ctk.CTkEntry(self.container, width=300, height=45, corner_radius=12,
                                          font=ctk.CTkFont(size=16), justify="center",
                                          placeholder_text="Wpisz tłumaczenie...")
        self.review_entry.pack(pady=10)
        self.review_entry.bind("<Return>", lambda e: self.review_check(word, correct_translation))
        self.review_entry.focus()

        self.review_feedback = ctk.CTkLabel(self.container, text="", font=ctk.CTkFont(size=14))
        self.review_feedback.pack(pady=8)

        ctk.CTkButton(self.container, text="Sprawdź", width=160, corner_radius=12,
                      fg_color=COLORS["highlight"], hover_color="#c73650",
                      command=lambda: self.review_check(word, correct_translation)).pack(pady=10)
        self.back_button()

    def review_check(self, word, correct):
        answer = self.review_entry.get().strip().lower()
        is_correct = answer == correct.lower()
        if is_correct:
            self.review_score += 1
            self.review_feedback.configure(text="✅ Brawo, coraz lepiej!", text_color=COLORS["success"])
        else:
            self.review_feedback.configure(text=f"❌ Poprawna odpowiedź: {correct}", text_color=COLORS["error"])
        self.review_entry.configure(state="disabled")
        self.progress.record_answer(self.current_lang, word, is_correct)
        self.review_index += 1
        self.after(1200, self.review_render)

    # ------------------------------------------------------------------
    # OSIĄGNIĘCIA
    # ------------------------------------------------------------------
    def show_achievements(self):
        self.clear_container()
        self.top_bar("🏅 Osiągnięcia")

        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=10)

        unlocked_ids = set(self.progress.data.get("unlocked", []))
        for ach in ACHIEVEMENTS:
            unlocked = ach["id"] in unlocked_ids
            row = ctk.CTkFrame(scroll, fg_color=COLORS["card"] if unlocked else COLORS["card2"],
                               corner_radius=14)
            row.pack(fill="x", pady=6, padx=5)
            icon = ach["icon"] if unlocked else "🔒"
            color = COLORS["gold"] if unlocked else COLORS["muted"]
            ctk.CTkLabel(row, text=icon, font=ctk.CTkFont(size=26)).pack(side="left", padx=(15, 10), pady=12)
            text_col = ctk.CTkFrame(row, fg_color="transparent")
            text_col.pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(text_col, text=ach["name"], font=ctk.CTkFont(size=15, weight="bold"),
                         text_color=color, anchor="w").pack(fill="x")
            ctk.CTkLabel(text_col, text=ach["desc"], font=ctk.CTkFont(size=12),
                         text_color=COLORS["muted"], anchor="w").pack(fill="x")
            if unlocked:
                ctk.CTkLabel(row, text="ODBLOKOWANE", font=ctk.CTkFont(size=11, weight="bold"),
                             text_color=COLORS["success"]).pack(side="right", padx=15)

        self.back_button()

    # ------------------------------------------------------------------
    # STATYSTYKI
    # ------------------------------------------------------------------
    def show_stats(self):
        self.clear_container()
        self.top_bar("📊 Statystyki")

        d = self.progress.data
        acc = self.progress.overall_accuracy()
        xp_in_level = d["xp"] % XP_PER_LEVEL

        info = ctk.CTkFrame(self.container, fg_color=COLORS["card"], corner_radius=18)
        info.pack(fill="x", pady=10, padx=20)

        rows = [
            ("Poziom", str(d["level"])),
            ("Całkowite XP", str(d["xp"])),
            ("Postęp do kolejnego poziomu", f"{xp_in_level}/{XP_PER_LEVEL} XP"),
            ("Seria dni nauki", f"🔥 {d.get('streak', 0)} dni"),
            ("Liczba sesji nauki", str(d["sessions"])),
            ("Ogólna skuteczność odpowiedzi", f"{acc:.1f}%"),
            ("Poznane słówka (min. 1 próba)", str(len(d["words"]))),
            ("Odblokowane odznaki", f"{len(d.get('unlocked', []))}/{len(ACHIEVEMENTS)}"),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(info, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=7)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=14),
                         text_color=COLORS["muted"]).pack(side="left")
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLORS["text"]).pack(side="right")

        ctk.CTkLabel(self.container, text="Postęp do kolejnego poziomu:",
                     font=ctk.CTkFont(size=13), text_color=COLORS["muted"]).pack(pady=(15, 5), anchor="w", padx=22)
        bar_bg = ctk.CTkFrame(self.container, fg_color=COLORS["accent"], height=18, corner_radius=9)
        bar_bg.pack(fill="x", padx=20, pady=(0, 20))
        self._animated_bar(bar_bg, xp_in_level / XP_PER_LEVEL, color=COLORS["gold"])

        self.back_button()

    # ------------------------------------------------------------------
    # USTAWIENIA (nowość)
    # ------------------------------------------------------------------
    def show_settings(self):
        self.clear_container()
        self.top_bar("⚙️ Ustawienia")

        panel = ctk.CTkFrame(self.container, fg_color=COLORS["card"], corner_radius=18)
        panel.pack(fill="x", pady=15, padx=20)

        row = ctk.CTkFrame(panel, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(row, text="Animacje interfejsu", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["text"]).pack(side="left")
        switch_var = ctk.BooleanVar(value=self.progress.data.get("animations", True))

        def toggle():
            self.progress.data["animations"] = switch_var.get()
            self.progress.save()
            self.toast("Zapisano ustawienia", "info")

        ctk.CTkSwitch(row, text="", variable=switch_var, command=toggle,
                      progress_color=COLORS["success"]).pack(side="right")

        # --- Sekcja Asystent AI ---
        ai_panel = ctk.CTkFrame(self.container, fg_color=COLORS["card"], corner_radius=18)
        ai_panel.pack(fill="x", pady=(0, 15), padx=20)

        ctk.CTkLabel(ai_panel, text="🤖 Asystent AI (Anthropic API)", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 5))

        if not ANTHROPIC_AVAILABLE:
            ctk.CTkLabel(ai_panel, text="Biblioteka 'anthropic' nie jest zainstalowana.\n"
                         "Uruchom: pip install anthropic --break-system-packages",
                         font=ctk.CTkFont(size=12), text_color=COLORS["warning"],
                         justify="left").pack(anchor="w", padx=20, pady=(0, 15))
        else:
            key_row = ctk.CTkFrame(ai_panel, fg_color="transparent")
            key_row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(key_row, text="Klucz API:", font=ctk.CTkFont(size=13),
                         text_color=COLORS["muted"], width=90, anchor="w").pack(side="left")
            self.api_key_entry = ctk.CTkEntry(key_row, width=320, show="•", corner_radius=10,
                                              placeholder_text="sk-ant-...")
            self.api_key_entry.pack(side="left", padx=(5, 10))
            if self.progress.data.get("api_key"):
                self.api_key_entry.insert(0, self.progress.data["api_key"])
            ctk.CTkButton(key_row, text="Zapisz", width=80, corner_radius=10,
                          fg_color=COLORS["success"], hover_color="#27ae60",
                          command=self._save_api_key).pack(side="left")

            model_row = ctk.CTkFrame(ai_panel, fg_color="transparent")
            model_row.pack(fill="x", padx=20, pady=(5, 18))
            ctk.CTkLabel(model_row, text="Model:", font=ctk.CTkFont(size=13),
                         text_color=COLORS["muted"], width=90, anchor="w").pack(side="left")
            current_model_name = next((k for k, v in AI_MODELS.items()
                                       if v == self.progress.data.get("ai_model")), list(AI_MODELS.keys())[0])
            self.model_menu = ctk.CTkOptionMenu(model_row, values=list(AI_MODELS.keys()),
                                                fg_color=COLORS["accent"], button_color=COLORS["highlight"],
                                                command=self._save_ai_model, width=250)
            self.model_menu.set(current_model_name)
            self.model_menu.pack(side="left", padx=5)

        row2 = ctk.CTkFrame(panel, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(row2, text="Zresetuj cały postęp nauki", font=ctk.CTkFont(size=14),
                     text_color=COLORS["muted"]).pack(side="left")
        ctk.CTkButton(row2, text="Resetuj", width=110, corner_radius=12, fg_color=COLORS["error"],
                      hover_color="#c0392b", command=self._confirm_reset).pack(side="right")

        self.back_button()

    def _confirm_reset(self):
        self.clear_container()
        self.top_bar("⚠️ Potwierdzenie")
        ctk.CTkLabel(self.container, text="Czy na pewno chcesz zresetować cały postęp?\nTej operacji nie można cofnąć.",
                     font=ctk.CTkFont(size=16), text_color=COLORS["warning"], justify="center").pack(pady=50)
        row = ctk.CTkFrame(self.container, fg_color="transparent")
        row.pack(pady=10)
        ctk.CTkButton(row, text="Tak, resetuj", width=160, corner_radius=12, fg_color=COLORS["error"],
                      hover_color="#c0392b", command=self._do_reset).pack(side="left", padx=10)
        ctk.CTkButton(row, text="Anuluj", width=160, corner_radius=12, fg_color=COLORS["accent"],
                      hover_color=COLORS["highlight"], command=self.show_settings).pack(side="left", padx=10)

    def _do_reset(self):
        self.progress.reset()
        self.toast("Postęp został zresetowany", "info")
        self.show_main_menu()

    def _save_api_key(self):
        key = self.api_key_entry.get().strip()
        self.progress.data["api_key"] = key
        self.progress.save()
        self.toast("Klucz API zapisany", "success")

    def _save_ai_model(self, choice):
        self.progress.data["ai_model"] = AI_MODELS[choice]
        self.progress.save()
        self.toast(f"Model ustawiony: {choice}", "info")

    # ------------------------------------------------------------------
    # ASYSTENT AI (czat z modelem Claude, kontekstowo dopasowany do języka)
    # ------------------------------------------------------------------
    def start_ai_assistant(self):
        self.clear_container()
        self.top_bar(f"🤖 Asystent AI — {self.current_lang}")

        if not ANTHROPIC_AVAILABLE:
            ctk.CTkLabel(self.container,
                         text="Aby korzystać z asystenta, zainstaluj bibliotekę:\n"
                              "pip install anthropic --break-system-packages\n\n"
                              "i uruchom aplikację ponownie.",
                         font=ctk.CTkFont(size=15), text_color=COLORS["warning"],
                         justify="center").pack(pady=60)
            self.back_button()
            return

        if not self.progress.data.get("api_key"):
            ctk.CTkLabel(self.container,
                         text="Nie ustawiono klucza API.\nPrzejdź do Ustawień, aby go dodać.",
                         font=ctk.CTkFont(size=15), text_color=COLORS["warning"],
                         justify="center").pack(pady=40)
            ctk.CTkButton(self.container, text="⚙️ Przejdź do ustawień", width=200, corner_radius=12,
                          fg_color=COLORS["highlight"], hover_color="#c73650",
                          command=self.show_settings).pack(pady=10)
            self.back_button()
            return

        if not hasattr(self, "ai_history") or getattr(self, "ai_history_lang", None) != self.current_lang:
            self.ai_history = []  # lista (rola, treść) - resetuje się przy zmianie języka
            self.ai_history_lang = self.current_lang

        # Obszar czatu (przewijalny)
        self.ai_chat_frame = ctk.CTkScrollableFrame(self.container, fg_color=COLORS["card2"], corner_radius=16)
        self.ai_chat_frame.pack(fill="both", expand=True, pady=(0, 10))

        if not self.ai_history:
            self._ai_add_bubble("assistant",
                f"Cześć! Jestem Twoim asystentem do nauki języka {self.current_lang.lower()}a. "
                f"Możesz zapytać mnie o gramatykę, poprosić o przykładowe zdanie, albo napisać zdanie "
                f"do sprawdzenia. O co chcesz zapytać?")
        else:
            for role, text in self.ai_history:
                self._ai_add_bubble(role, text)

        # Szybkie akcje
        quick_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        quick_frame.pack(fill="x", pady=(0, 8))
        quick_actions = [
            ("📖 Wyjaśnij gramatykę", f"Wyjaśnij najważniejszą regułę gramatyczną początkującego w języku {self.current_lang.lower()}."),
            ("💬 Przykładowe zdanie", f"Podaj 3 proste przykładowe zdania w języku {self.current_lang.lower()} z tłumaczeniem na polski."),
            ("✍️ Sprawdź moje zdanie", None),
        ]
        for label, prompt in quick_actions:
            ctk.CTkButton(quick_frame, text=label, height=32, corner_radius=10,
                          fg_color=COLORS["accent"], hover_color=COLORS["highlight"],
                          font=ctk.CTkFont(size=12),
                          command=(lambda p=prompt: self._ai_quick_send(p)) if prompt
                          else self._ai_focus_input).pack(side="left", padx=4)

        # Pole wpisywania
        input_row = ctk.CTkFrame(self.container, fg_color="transparent")
        input_row.pack(fill="x", pady=(0, 5))
        self.ai_entry = ctk.CTkEntry(input_row, corner_radius=12, height=42,
                                      placeholder_text=f"Napisz wiadomość po polsku lub po {self.current_lang.lower()}u...")
        self.ai_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.ai_entry.bind("<Return>", lambda e: self._ai_send())
        self.ai_send_btn = ctk.CTkButton(input_row, text="Wyślij ➤", width=100, corner_radius=12,
                                         fg_color=COLORS["highlight"], hover_color="#c73650",
                                         command=self._ai_send)
        self.ai_send_btn.pack(side="left")

        self.back_button()
        self.ai_entry.focus()

    def _ai_focus_input(self):
        if hasattr(self, "ai_entry") and self.ai_entry.winfo_exists():
            self.ai_entry.focus()

    def _ai_add_bubble(self, role, text):
        is_user = role == "user"
        row = ctk.CTkFrame(self.ai_chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=6, padx=8, anchor="e" if is_user else "w")

        bubble = ctk.CTkFrame(row, fg_color=COLORS["highlight"] if is_user else COLORS["accent"],
                              corner_radius=14)
        bubble.pack(side="right" if is_user else "left", anchor="e" if is_user else "w")

        label = ctk.CTkLabel(bubble, text=text, font=ctk.CTkFont(size=13),
                             text_color="#ffffff", wraplength=520, justify="left")
        label.pack(padx=14, pady=10)
        self.ai_chat_frame.update_idletasks()
        self.ai_chat_frame._parent_canvas.yview_moveto(1.0)
        return label

    def _ai_quick_send(self, prompt_text):
        self._ai_dispatch(prompt_text, display_text=prompt_text)

    def _ai_send(self):
        text = self.ai_entry.get().strip()
        if not text:
            return
        self.ai_entry.delete(0, "end")
        self._ai_dispatch(text, display_text=text)

    def _ai_dispatch(self, message_for_model, display_text):
        self.ai_history.append(("user", display_text))
        self._ai_add_bubble("user", display_text)
        self.ai_send_btn.configure(state="disabled", text="...")

        thinking_label = self._ai_add_bubble("assistant", "💭 Asystent pisze")
        self._animate_thinking(thinking_label, 0)

        thread = threading.Thread(target=self._ai_call_api, args=(message_for_model, thinking_label), daemon=True)
        thread.start()

    def _animate_thinking(self, label, step):
        if not label.winfo_exists():
            return
        dots = "." * (step % 4)
        try:
            label.configure(text=f"💭 Asystent pisze{dots}")
        except Exception:
            return
        if getattr(label, "_stop_anim", False):
            return
        self.after(400, lambda: self._animate_thinking(label, step + 1))

    def _ai_call_api(self, message, thinking_label):
        system_prompt = (
            f"Jesteś przyjaznym, cierpliwym korepetytorem języka {self.current_lang.lower()}ego "
            f"dla Polaka, który się go uczy. Odpowiadaj zwięźle (maks. 4-5 zdań, chyba że użytkownik "
            f"prosi o więcej), w prostym języku. Gdy podajesz słowa lub zdania w {self.current_lang.lower()}u, "
            f"zawsze dodawaj tłumaczenie na polski w nawiasie. Jeśli użytkownik napisze zdanie do sprawdzenia, "
            f"popraw błędy i krótko wyjaśnij dlaczego."
        )
        try:
            client = Anthropic(api_key=self.progress.data["api_key"])
            history_msgs = [{"role": r, "content": t} for r, t in self.ai_history[-10:]]
            response = client.messages.create(
                model=self.progress.data.get("ai_model", "claude-haiku-4-5-20251001"),
                max_tokens=500,
                system=system_prompt,
                messages=history_msgs,
            )
            reply = "".join(block.text for block in response.content if hasattr(block, "text"))
        except Exception as e:
            reply = f"⚠️ Błąd połączenia z API: {e}"

        self.after(0, lambda: self._ai_finish_response(reply, thinking_label))

    def _ai_finish_response(self, reply, thinking_label):
        thinking_label._stop_anim = True
        try:
            thinking_label.configure(text=reply)
        except Exception:
            pass
        self.ai_history.append(("assistant", reply))
        if hasattr(self, "ai_send_btn") and self.ai_send_btn.winfo_exists():
            self.ai_send_btn.configure(state="normal", text="Wyślij ➤")
        if hasattr(self, "ai_chat_frame") and self.ai_chat_frame.winfo_exists():
            self.ai_chat_frame.update_idletasks()
            self.ai_chat_frame._parent_canvas.yview_moveto(1.0)


if __name__ == "__main__":
    app = LinguaMasterApp()
    app.mainloop()