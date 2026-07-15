import customtkinter as ctk
from database.db_manager import SessionLocal
from database.models import Client

class CRMModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Konfiguracja układu (lewa strona: formularz, prawa strona: lista)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- LEWY PANEL: FORMULARZ DODAWANIA ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        form_title = ctk.CTkLabel(self.form_frame, text="Dodaj Klienta", font=ctk.CTkFont(size=18, weight="bold"))
        form_title.pack(pady=15, padx=15, anchor="w")

        # Pola wprowadzania danych
        self.lbl_name = ctk.CTkLabel(self.form_frame, text="Imię i Nazwisko:")
        self.lbl_name.pack(padx=15, anchor="w")
        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Jan Kowalski")
        self.entry_name.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_company = ctk.CTkLabel(self.form_frame, text="Nazwa Firmy:")
        self.lbl_company.pack(padx=15, anchor="w")
        self.entry_company = ctk.CTkEntry(self.form_frame, placeholder_text="ACME Sp. z o.o.")
        self.entry_company.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_email = ctk.CTkLabel(self.form_frame, text="Adres E-mail:")
        self.lbl_email.pack(padx=15, anchor="w")
        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="kontakt@firma.pl")
        self.entry_email.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_phone = ctk.CTkLabel(self.form_frame, text="Telefon:")
        self.lbl_phone.pack(padx=15, anchor="w")
        self.entry_phone = ctk.CTkEntry(self.form_frame, placeholder_text="+48 123 456 789")
        self.entry_phone.pack(fill="x", padx=15, pady=(0, 20))

        # Przycisk zapisu
        self.btn_save = ctk.CTkButton(self.form_frame, text="Zapisz Klienta", command=self.add_client)
        self.btn_save.pack(fill="x", padx=15, pady=10)

        # Status zapisu
        self.lbl_status = ctk.CTkLabel(self.form_frame, text="", text_color="green")
        self.lbl_status.pack(pady=5)

        # --- PRAWY PANEL: LISTA KLIENTÓW ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")

        list_title = ctk.CTkLabel(self.list_frame, text="Baza Kontrahentów", font=ctk.CTkFont(size=18, weight="bold"))
        list_title.pack(pady=15, padx=15, anchor="w")

        # Przewijana lista (ScrollableFrame)
        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame)
        self.scrollable_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Wczytaj klientów na start
        self.refresh_client_list()

    def add_client(self):
        name = self.entry_name.get().strip()
        company = self.entry_company.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()

        if not name:
            self.lbl_status.configure(text="Imię i nazwisko jest wymagane!", text_color="red")
            return

        # Bezpośrednie użycie SessionLocal() zamiast get_db
        db = SessionLocal()
        new_client = Client(name=name, company_name=company, email=email, phone=phone)
        try:
            db.add(new_client)
            db.commit()
            
            # Reset pól formularza
            self.entry_name.delete(0, 'end')
            self.entry_company.delete(0, 'end')
            self.entry_email.delete(0, 'end')
            self.entry_phone.delete(0, 'end')
            
            self.lbl_status.configure(text="Klient został pomyślnie zapisany!", text_color="green")
            self.refresh_client_list()
        except Exception as e:
            db.rollback()
            self.lbl_status.configure(text=f"Błąd zapisu: {e}", text_color="red")
        finally:
            db.close()

    def refresh_client_list(self):
        # Czyszczenie starej listy
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        # Bezpośrednie użycie SessionLocal() zamiast get_db
        db = SessionLocal()
        try:
            clients = db.query(Client).order_by(Client.created_at.desc()).all()
            
            if not clients:
                no_clients = ctk.CTkLabel(self.scrollable_list, text="Brak klientów w bazie danych. Dodaj pierwszego!")
                no_clients.pack(pady=20)
                return

            for client in clients:
                card = ctk.CTkFrame(self.scrollable_list, fg_color=["#EAEAEA", "#2B2B2B"], corner_radius=6)
                card.pack(fill="x", pady=5, padx=5)

                info_text = f"👤 {client.name}"
                if client.company_name:
                    info_text += f" | 🏢 {client.company_name}"
                
                contact_text = f"✉ {client.email or 'brak'} | 📞 {client.phone or 'brak'}"

                lbl_info = ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(weight="bold"))
                lbl_info.pack(anchor="w", padx=10, pady=(5, 2))

                lbl_contact = ctk.CTkLabel(card, text=contact_text, font=ctk.CTkFont(size=11))
                lbl_contact.pack(anchor="w", padx=10, pady=(2, 5))
        except Exception as e:
            err_lbl = ctk.CTkLabel