import customtkinter as ctk
import random
from typing import List, Dict

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ClientCRMApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Enterprise Client & Order Manager Pro")
        self.geometry("950x650")
        self.minsize(850, 550)

        # Baza danych zleceniowa (przykładowe dane)
        self.orders: List[Dict[str, str]] = [
            {
                "id": "ZLE-101",
                "klient": "TechCorp Sp. z o.o.",
                "usluga": "Integracja AI w CRM",
                "kwota": "2500 PLN",
                "status": "W trakcie",
            },
            {
                "id": "ZLE-102",
                "klient": "Sklep Opona-24",
                "usluga": "Web Scraping Cenników",
                "kwota": "800 PLN",
                "status": "Zakończone",
            },
            {
                "id": "ZLE-103",
                "klient": "Biuro Nieruchomości Home",
                "usluga": "Generator Opisów Ofert",
                "kwota": "1200 PLN",
                "status": "Oczekuje",
            },
        ]

        # Układ główny
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header_stats()
        self._build_main_tabview()

    def _build_header_stats(self):
        """Pasek ze statystykami biznesowymi (KPI Cards)."""
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(
            row=0, column=0, sticky="ew", padx=20, pady=(15, 5)
        )
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Kafelek 1: Liczba Zleceń
        self.card1 = ctk.CTkFrame(self.stats_frame, corner_radius=10)
        self.card1.grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkLabel(
            self.card1,
            text="Wszystkie Zlecenia",
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color="gray",
        ).pack(pady=(10, 0))
        self.lbl_stat_total = ctk.CTkLabel(
            self.card1,
            text=str(len(self.orders)),
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.lbl_stat_total.pack(pady=(0, 10))

        # Kafelek 2: Łączny Przychód
        self.card2 = ctk.CTkFrame(self.stats_frame, corner_radius=10)
        self.card2.grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkLabel(
            self.card2,
            text="Suma Budżetów",
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color="gray",
        ).pack(pady=(10, 0))
        self.lbl_stat_revenue = ctk.CTkLabel(
            self.card2,
            text=self._calculate_total_revenue(),
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2ecc71",
        )
        self.lbl_stat_revenue.pack(pady=(0, 10))

        # Kafelek 3: W trakcie
        self.card3 = ctk.CTkFrame(self.stats_frame, corner_radius=10)
        self.card3.grid(row=0, column=2, padx=5, sticky="ew")
        ctk.CTkLabel(
            self.card3,
            text="W Realizacji",
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color="gray",
        ).pack(pady=(10, 0))
        self.lbl_stat_active = ctk.CTkLabel(
            self.card3,
            text=str(
                sum(1 for o in self.orders if o["status"] == "W trakcie")
            ),
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#3498db",
        )
        self.lbl_stat_active.pack(pady=(0, 10))

    def _build_main_tabview(self):
        """Główny interfejs oparty na zakładkach."""
        self.tabview = ctk.CTkTabview(self, corner_radius=15)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))

        self.tab_list = self.tabview.add("📋 Lista Zleceń")
        self.tab_add = self.tabview.add("➕ Nowe Zlecenie")

        self._setup_orders_list_tab()
        self._setup_add_order_tab()

    def _setup_orders_list_tab(self):
        """Zakładka 1: Tabela i podgląd szczegółów."""
        self.tab_list.grid_columnconfigure(0, weight=1)
        self.tab_list.grid_rowconfigure(0, weight=1)

        self.scroll_orders = ctk.CTkScrollableFrame(self.tab_list)
        self.scroll_orders.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self._refresh_orders_list()

    def _refresh_orders_list(self):
        """Generuje dynamiczne wiersze tabeli z opcją zmiany statusu."""
        for widget in self.scroll_orders.winfo_children():
            widget.destroy()

        for idx, order in enumerate(self.orders):
            row_frame = ctk.CTkFrame(self.scroll_orders, fg_color="#2b2b2b")
            row_frame.pack(fill="x", pady=5, padx=5, ipady=5)

            # Id i Nazwa Klienta
            lbl_info = ctk.CTkLabel(
                row_frame,
                text=f"[{order['id']}] {order['klient']}\nUsługa: {order['usluga']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                justify="left",
            )
            lbl_info.pack(side="left", padx=15)

            # Kwota
            lbl_price = ctk.CTkLabel(
                row_frame,
                text=order["kwota"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2ecc71",
            )
            lbl_price.pack(side="right", padx=15)

            # Status (Badge)
            color_map = {
                "Zakończone": "#27ae60",
                "W trakcie": "#2980b9",
                "Oczekuje": "#e67e22",
            }
            lbl_status = ctk.CTkLabel(
                row_frame,
                text=order["status"],
                fg_color=color_map.get(order["status"], "gray"),
                corner_radius=8,
                padx=10,
                pady=2,
                font=ctk.CTkFont(size=11, weight="bold"),
            )
            lbl_status.pack(side="right", padx=10)

    def _setup_add_order_tab(self):
        """Zakładka 2: Formularz dodawania nowego klienta/zlecenia."""
        form_frame = ctk.CTkFrame(self.tab_add, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=40, pady=20)

        # Pola formularza
        ctk.CTkLabel(
            form_frame, text="Nazwa Klienta / Firmy:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(10, 2))
        self.entry_client = ctk.CTkEntry(
            form_frame, placeholder_text="np. Jan Kowalski / Firma XYZ"
        )
        self.entry_client.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            form_frame, text="Nazwa Usługi / Projektu:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(10, 2))
        self.entry_service = ctk.CTkEntry(
            form_frame, placeholder_text="np. Strona w Python / Automatyzacja"
        )
        self.entry_service.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            form_frame, text="Wycena (PLN):", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(10, 2))
        self.entry_price = ctk.CTkEntry(
            form_frame, placeholder_text="np. 1500 PLN"
        )
        self.entry_price.pack(fill="x", pady=(0, 15))

        # Przycisk Zapisu
        self.btn_save = ctk.CTkButton(
            form_frame,
            text="💾 Dodaj Zlecenie do Bazy",
            height=45,
            fg_color="#27ae60",
            hover_color="#219150",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._add_new_order,
        )
        self.btn_save.pack(fill="x", pady=(10, 0))

        self.lbl_form_msg = ctk.CTkLabel(form_frame, text="")
        self.lbl_form_msg.pack(pady=10)

    def _add_new_order(self):
        """Walidacja i dodawanie nowego zlecenia."""
        client = self.entry_client.get().strip()
        service = self.entry_service.get().strip()
        price = self.entry_price.get().strip()

        if not client or not service or not price:
            self.lbl_form_msg.configure(
                text="⚠️ Wypełnij wszystkie pola!", text_color="#e74c3c"
            )
            return

        new_id = f"ZLE-{random.randint(104, 999)}"
        new_order = {
            "id": new_id,
            "klient": client,
            "usluga": service,
            "kwota": price if "PLN" in price else f"{price} PLN",
            "status": "Oczekuje",
        }

        self.orders.append(new_order)

        # Czyszczenie pól i aktualizacja
        self.entry_client.delete(0, "end")
        self.entry_service.delete(0, "end")
        self.entry_price.delete(0, "end")

        self.lbl_form_msg.configure(
            text=f"✅ Pomyślnie dodano zlecenie [{new_id}]!",
            text_color="#2ecc71",
        )

        # Odświeżenie widoków i statystyk
        self._refresh_orders_list()
        self._update_stats()

    def _calculate_total_revenue(self) -> str:
        total = 0
        for o in self.orders:
            num = "".join(filter(str.isdigit, o["kwota"]))
            if num:
                total += int(num)
        return f"{total} PLN"

    def _update_stats(self):
        """Aktualizacja wskaźników na samej górze."""
        self.lbl_stat_total.configure(text=str(len(self.orders)))
        self.lbl_stat_revenue.configure(text=self._calculate_total_revenue())
        self.lbl_stat_active.configure(
            text=str(
                sum(1 for o in self.orders if o["status"] == "W trakcie")
            )
        )


if __name__ == "__main__":
    app = ClientCRMApp()
    app.mainloop()