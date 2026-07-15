import os
from pathlib import Path

# Ścieżki systemowe
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

# Tworzenie katalogów roboczych, jeśli nie istnieją
for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Konfiguracja Bazy Danych
DB_PATH = DATA_DIR / "enterprise_system.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Ustawienia Aplikacji
APP_NAME = "Enterprise ERP & BI Platform"
APP_VERSION = "2.5.0"
COMPANY_NAME = "NovaTech Global Solutions Sp. z o.o."
CURRENCY = "PLN"
TAX_RATE_DEFAULT = 0.23  # VAT 23%

# Konfiguracja Wyglądu Interfejsu (CustomTkinter)
UI_THEME = "dark"  # "dark" lub "light"
UI_COLOR_ACCENT = "blue"  # "blue", "green", "dark-blue"

# Paleta Kolorów Systemu (HEX)
COLORS = {
    "primary": "#1F2937",
    "secondary": "#3B82F6",
    "accent": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "background_dark": "#111827",
    "card_dark": "#1F2937",
    "text_light": "#F9FAFB",
    "text_muted": "#9CA3AF",
    "border": "#374151"
}

# Integracje i API
AI_MODEL_NAME = "claude-haiku-4-5-20251001"
MAX_AI_TOKENS = 1500

# Uprawnienia i Role Użytkowników
ROLES = {
    "ADMIN": "Administrator Systemu",
    "MANAGER": "Kierownik / Manager",
    "ACCOUNTANT": "Księgowy / Finanse",
    "SALES": "Przedstawiciel Handlowy",
    "WAREHOUSE": "Magazynier"
}