import customtkinter as ctk
from PIL import Image
from typing import Callable, List, Dict

class KPICard(ctk.CTkFrame):
    """Komponent karty podsumowującej kluczowe statystyki (KPI)."""
    def __init__(self, master, title: str, value: str, accent_color: str = "#3B82F6", **kwargs):
        super().__init__(master, fg_color="#1F2937", corner_radius=10, border_width=1, border_color="#374151", **kwargs)
        
        # Pasek akcentujący po lewej stronie
        accent_bar = ctk.CTkFrame(self, width=6, fg_color=accent_color, corner_radius=3)
        accent_bar.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # Kontener na tekst
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        title_lbl = ctk.CTkLabel(text_frame, text=title.upper(), font=("Helvetica", 11, "bold"), text_color="#9CA3AF", anchor="w")
        title_lbl.pack(fill="x")

        value_lbl = ctk.CTkLabel(text_frame, text=value, font=("Helvetica", 20, "bold"), text_color="#F9FAFB", anchor="w")
        value_lbl.pack(fill="x", pady=(2, 0))


class CustomDataTable(ctk.CTkScrollableFrame):
    """Uniwersalna Tabela Danych do wyświetlania rekordów z bazy."""
    def __init__(self, master, headers: List[str], **kwargs):
        super().__init__(master, fg_color="#111827", corner_radius=8, **kwargs)
        self.headers = headers
        self._build_header()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#1F2937", corner_radius=6)
        header_frame.pack(fill="x", pady=(0, 5), padx=2)

        for col_idx, header in enumerate(self.headers):
            lbl = ctk.CTkLabel(header_frame, text=header, font=("Helvetica", 12, "bold"), text_color="#3B82F6", anchor="w")
            lbl.grid(row=0, column=col_idx, sticky="ew", padx=10, pady=8)
            header_frame.grid_columnconfigure(col_idx, weight=1)

    def set_data(self, rows: List[List[str]]):
        """Czyści stare rekordy i ładuje nowe wiersze do tabeli."""
        # Usuwanie starych wierszy
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.winfo_children()[0]:
                widget.destroy()

        # Renderowanie nowych wierszy
        for row_idx, row_data in enumerate(rows):
            bg_color = "#1F2937" if row_idx % 2 == 0 else "#1A2234"
            row_frame = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=4)
            row_frame.pack(fill="x", pady=2, padx=2)

            for col_idx, cell_value in enumerate(row_data):
                lbl = ctk.CTkLabel(row_frame, text=str(cell_value), font=("Helvetica", 11), text_color="#F9FAFB", anchor="w")
                lbl.grid(row=0, column=col_idx, sticky="ew", padx=10, pady=6)
                row_frame.grid_columnconfigure(col_idx, weight=1)


class ActionHeader(ctk.CTkFrame):
    """Niestandardowy nagłówek podstrony z tytułem i przyciskiem akcji."""
    def __init__(self, master, title: str, button_text: str = None, command: Callable = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        title_lbl = ctk.CTkLabel(self, text=title, font=("Helvetica", 22, "bold"), text_color="#F9FAFB")
        title_lbl.pack(side="left", anchor="w")

        if button_text and command:
            btn = ctk.CTkButton(self, text=button_text, command=command, fg_color="#3B82F6", hover_color="#2563EB", font=("Helvetica", 12, "bold"))
            btn.pack(side="right", anchor="e")