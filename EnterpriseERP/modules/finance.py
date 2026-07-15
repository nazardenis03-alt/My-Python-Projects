import customtkinter as ctk
from database.db_manager import SessionLocal
from database.models import Invoice

class FinanceModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Układ (lewa strona: wystawianie faktury, prawa strona: lista faktur)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- LEWY PANEL: WYSTAWIANIE FAKTURY ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        form_title = ctk.CTkLabel(self.form_frame, text="Nowa Faktura", font=ctk.CTkFont(size=18, weight="bold"))
        form_title.pack(pady=15, padx=15, anchor="w")

        self.lbl_number = ctk.CTkLabel(self.form_frame, text="Numer Faktury:")
        self.lbl_number.pack(padx=15, anchor="w")
        self.entry_number = ctk.CTkEntry(self.form_frame, placeholder_text="np. FV/2026/07/01")
        self.entry_number.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_amount = ctk.CTkLabel(self.form_frame, text="Kwota brutto (PLN):")
        self.lbl_amount.pack(padx=15, anchor="w")
        self.entry_amount = ctk.CTkEntry(self.form_frame, placeholder_text="np. 1230.50")
        self.entry_amount.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_status_choice = ctk.CTkLabel(self.form_frame, text="Status płatności:")
        self.lbl_status_choice.pack(padx=15, anchor="w")
        
        self.status_dropdown = ctk.CTkOptionMenu(
            self.form_frame, 
            values=["Opłacona", "Nieopłacona", "Przeterminowana"]
        )
        self.status_dropdown.pack(fill="x", padx=15, pady=(0, 20))

        self.btn_save = ctk.CTkButton(self.form_frame, text="Wystaw Fakturę", command=self.add_invoice)
        self.btn_save.pack(fill="x", padx=15, pady=10)

        self.lbl_status = ctk.CTkLabel(self.form_frame, text="", text_color="green")
        self.lbl_status.pack(pady=5)

        # --- PRAWY PANEL: REJESTR FAKTUR ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")

        list_title = ctk.CTkLabel(self.list_frame, text="Rejestr Sprzedaży", font=ctk.CTkFont(size=18, weight="bold"))
        list_title.pack(pady=15, padx=15, anchor="w")

        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame)
        self.scrollable_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.refresh_invoice_list()

    def add_invoice(self):
        number = self.entry_number.get().strip()
        amount_str = self.entry_amount.get().strip()
        status = self.status_dropdown.get()

        if not number or not amount_str:
            self.lbl_status.configure(text="Uzupełnij numer i kwotę!", text_color="red")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            self.lbl_status.configure(text="Kwota must być liczbą!", text_color="red")
            return

        db = SessionLocal()
        new_invoice = Invoice(
            invoice_number=number,
            total_amount=amount,
            status=status
        )
        try:
            db.add(new_invoice)
            db.commit()
            
            self.entry_number.delete(0, 'end')
            self.entry_amount.delete(0, 'end')
            
            self.lbl_status.configure(text="Faktura wystawiona pomyślnie!", text_color="green")
            self.refresh_invoice_list()
        except Exception as e:
            db.rollback()
            self.lbl_status.configure(text=f"Błąd zapisu: Numer musi być unikalny!", text_color="red")
        finally:
            db.close()

    def refresh_invoice_list(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()