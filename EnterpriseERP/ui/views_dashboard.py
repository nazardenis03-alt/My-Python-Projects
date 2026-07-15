import customtkinter as ctk
from PIL import Image, ImageTk
import os
from ui.components import KPICard, ActionHeader
from modules.analytics import AnalyticsModule
from config import CURRENCY

class DashboardView(ctk.CTkFrame):
    """Główny panel analityczny Business Intelligence."""
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Nagłówek panelu
        self.header = ActionHeader(self, title="Pulpit Menedżerski (Business Intelligence)", button_text="Odśwież Dane", command=self.refresh_dashboard)
        self.header.pack(fill="x", padx=20, pady=(20, 10))

        # Kontener na karty KPI
        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.pack(fill="x", padx=20, pady=10)

        # Kontener na wykresy
        self.charts_container = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Inicjalizacja i załadowanie danych
        self.refresh_dashboard()

    def refresh_dashboard(self):
        """Pobiera najświeższe dane z bazy i odświeża cały widok panelu."""
        # 1. Pobieranie statystyk
        stats = AnalyticsModule.get_basic_stats()

        # Czyszczenie starych kart KPI
        for widget in self.kpi_container.winfo_children():
            widget.destroy()

        # Generowanie nowych kart KPI
        revenue_card = KPICard(
            self.kpi_container, 
            title="Przychód (Opłacone)", 
            value=f"{stats['total_revenue']:,.2f} {CURRENCY}".replace(",", " "), 
            accent_color="#10B981"
        )
        revenue_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        pending_card = KPICard(
            self.kpi_container, 
            title="Należności (Oczekujące)", 
            value=f"{stats['pending_revenue']:,.2f} {CURRENCY}".replace(",", " "), 
            accent_color="#F59E0B"
        )
        pending_card.pack(side="left", fill="both", expand=True, padx=10)

        stock_card = KPICard(
            self.kpi_container, 
            title="Niskie Stany Magazynowe", 
            value=f"{stats['low_stock_count']} szt.", 
            accent_color="#EF4444"
        )
        stock_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # 2. Generowanie i ładowanie wykresów
        chart_revenue_path = AnalyticsModule.generate_revenue_chart()
        chart_category_path = AnalyticsModule.generate_category_chart()

        # Czyszczenie starych wykresów
        for widget in self.charts_container.winfo_children():
            widget.destroy()

        # Wyświetlanie wykresu przychodów (po lewej)
        if os.path.exists(chart_revenue_path):
            img_rev = Image.open(chart_revenue_path)
            # Konwersja obrazu dla CustomTkinter (dopasowanie rozmiaru)
            ctk_img_rev = ctk.CTkImage(light_image=img_rev, dark_image=img_rev, size=(450, 260))
            
            rev_frame = ctk.CTkFrame(self.charts_container, fg_color="#1F2937", corner_radius=10, border_width=1, border_color="#374151")
            rev_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            lbl_rev = ctk.CTkLabel(rev_frame, image=ctk_img_rev, text="")
            lbl_rev.pack(fill="both", expand=True, padx=10, pady=10)

        # Wyświetlanie wykresu kategorii (po prawej)
        if os.path.exists(chart_category_path):
            img_cat = Image.open(chart_category_path)
            ctk_img_cat = ctk.CTkImage(light_image=img_cat, dark_image=img_cat, size=(380, 260))
            
            cat_frame = ctk.CTkFrame(self.charts_container, fg_color="#1F2937", corner_radius=10, border_width=1, border_color="#374151")
            cat_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
            
            lbl_cat = ctk.CTkLabel(cat_frame, image=ctk_img_cat, text="")
            lbl_cat.pack(fill="both", expand=True, padx=10, pady=10)