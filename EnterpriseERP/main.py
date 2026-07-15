import customtkinter as ctk
from config import APP_NAME, APP_VERSION, UI_THEME, UI_COLOR_ACCENT
from database.db_manager import init_db, seed_database

# Import widoków (views)
from ui.views_dashboard import DashboardView

# Próba zaimportowania modułów. Jeśli są napisane jako klasy, używamy ich.
# Jeśli to czyste skrypty, obsłużymy je jako zakładki dynamiczne.
try:
    from modules.crm import CRMModule
except ImportError:
    CRMModule = None

try:
    from modules.warehouse import WarehouseModule
except ImportError:
    WarehouseModule = None

try:
    from modules.finance import FinanceModule
except ImportError:
    FinanceModule = None

# Ustawienia motywu CustomTkinter
ctk.set_appearance_mode(UI_THEME)
ctk.set_default_color_theme("blue")

class EnterpriseERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} - {APP_VERSION}")
        self.geometry("1280x720")
        self.minsize(1024, 600)

        # Inicjalizacja bazy danych przy starcie
        init_db()
        seed_database()

        # Główny układ okna (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. LEWY PANEL NAWIGACYJNY (Sidebar)
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Logo / Nazwa aplikacji
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=APP_NAME.upper(), 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=UI_COLOR_ACCENT
        )
        self.logo_label.pack(pady=(20, 30), padx=20)

        # Przyciski nawigacji
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="Pulpit BI (Dashboard)", 
            command=self.show_dashboard, anchor="w", height=40
        )
        self.btn_dashboard.pack(fill="x", padx=15, pady=5)

        self.btn_crm = ctk.CTkButton(
            self.sidebar_frame, text="Klienci (CRM)", 
            command=self.show_crm, anchor="w", height=40
        )
        self.btn_crm.pack(fill="x", padx=15, pady=5)

        self.btn_warehouse = ctk.CTkButton(
            self.sidebar_frame, text="Magazyn (Logistyka)", 
            command=self.show_warehouse, anchor="w", height=40
        )
        self.btn_warehouse.pack(fill="x", padx=15, pady=5)

        self.btn_finance = ctk.CTkButton(
            self.sidebar_frame, text="Finanse i Faktury", 
            command=self.show_finance, anchor="w", height=40
        )
        self.btn_finance.pack(fill="x", padx=15, pady=5)

        # Stopka w panelu bocznym
        self.version_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text=f"Wersja {APP_VERSION}", 
            font=ctk.CTkFont(size=11)
        )
        self.version_label.pack(side="bottom", pady=15)

        # 2. GŁÓWNY KONTENER NA PODSTRONY (Prawa strona)
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.current_view = None
        
        # Domyślny widok przy starcie systemu
        self.show_dashboard()

    def clear_container(self):
        """Usuwa aktualnie wyświetlany widok z kontenera."""
        if self.current_view is not None:
            self.current_view.destroy()

    def highlight_active_button(self, active_button):
        """Wizualnie wyróżnia aktywny przycisk w menu."""
        buttons = [self.btn_dashboard, self.btn_crm, self.btn_warehouse, self.btn_finance]
        for btn in buttons:
            if btn == active_button:
                btn.configure(fg_color=UI_COLOR_ACCENT, hover_color=UI_COLOR_ACCENT)
            else:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#3277A8", "#144870"])

    # --- FUNKCJE PRZEŁĄCZANIA WIDOKÓW ---

    def show_dashboard(self):
        self.clear_container()
        self.highlight_active_button(self.btn_dashboard)
        self.current_view = DashboardView(self.main_container)
        self.current_view.pack(fill="both", expand=True)

    def show_crm(self):
        self.clear_container()
        self.highlight_active_button(self.btn_crm)
        
        self.current_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_view.pack(fill="both", expand=True)
        
        title = ctk.CTkLabel(self.current_view, text="Panel CRM - Zarządzanie Klientami", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 20))
        
        if CRMModule:
            try:
                crm_ui = CRMModule(self.current_view)
                crm_ui.pack(fill="both", expand=True)
            except Exception as e:
                err_label = ctk.CTkLabel(self.current_view, text=f"Moduł CRM wykryty, ale nie zainicjalizowany jako klasa: {e}\nWyświetlam widok alternatywny.", text_color="orange")
                err_label.pack(pady=20)
        else:
            placeholder = ctk.CTkLabel(self.current_view, text="Brak pliku modułu CRM w folderze modules.", font=ctk.CTkFont(size=16))
            placeholder.pack(pady=40)

    def show_warehouse(self):
        self.clear_container()
        self.highlight_active_button(self.btn_warehouse)
        
        self.current_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_view.pack(fill="both", expand=True)
        
        title = ctk.CTkLabel(self.current_view, text="Panel Magazynowy i Logistyka", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 20))
        
        if WarehouseModule:
            try:
                warehouse_ui = WarehouseModule(self.current_view)
                warehouse_ui.pack(fill="both", expand=True)
            except Exception as e:
                err_label = ctk.CTkLabel(self.current_view, text=f"Moduł Magazynu wykryty, ale nie zainicjalizowany jako klasa: {e}\nWyświetlam widok alternatywny.", text_color="orange")
                err_label.pack(pady=20)
        else:
            placeholder = ctk.CTkLabel(self.current_view, text="Brak pliku modułu Magazynu w folderze modules.", font=ctk.CTkFont(size=16))
            placeholder.pack(pady=40)

    def show_finance(self):
        self.clear_container()
        self.highlight_active_button(self.btn_finance)
        
        self.current_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_view.pack(fill="both", expand=True)
        
        title = ctk.CTkLabel(self.current_view, text="Księgowość i Finanse", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 20))
        
        if FinanceModule:
            try:
                finance_ui = FinanceModule(self.current_view)
                finance_ui.pack(fill="both", expand=True)
            except Exception as e:
                err_label = ctk.CTkLabel(self.current_view, text=f"Moduł Finansów wykryty, ale nie zainicjalizowany jako klasa: {e}\nWyświetlam widok alternatywny.", text_color="orange")
                err_label.pack(pady=20)
        else:
            placeholder = ctk.CTkLabel(self.current_view, text="Brak pliku modułu Finansów w folderze modules.", font=ctk.CTkFont(size=16))
            placeholder.pack(pady=40)

if __name__ == "__main__":
    app = EnterpriseERPApp()
    app.mainloop()