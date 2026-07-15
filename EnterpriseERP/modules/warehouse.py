import customtkinter as ctk
from database.db_manager import SessionLocal
from database.models import Product

class WarehouseModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Układ (lewa strona: dodawanie produktu, prawa strona: stany magazynowe)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- LEWY PANEL: DODAWANIE PRODUKTU ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        form_title = ctk.CTkLabel(self.form_frame, text="Dodaj Nowy Produkt", font=ctk.CTkFont(size=18, weight="bold"))
        form_title.pack(pady=15, padx=15, anchor="w")

        self.lbl_name = ctk.CTkLabel(self.form_frame, text="Nazwa Produktu:")
        self.lbl_name.pack(padx=15, anchor="w")
        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="np. Kabel RJ45 5m")
        self.entry_name.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_sku = ctk.CTkLabel(self.form_frame, text="Kod SKU:")
        self.lbl_sku.pack(padx=15, anchor="w")
        self.entry_sku = ctk.CTkEntry(self.form_frame, placeholder_text="np. KAB-RJ45-05")
        self.entry_sku.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_price = ctk.CTkLabel(self.form_frame, text="Cena netto (PLN):")
        self.lbl_price.pack(padx=15, anchor="w")
        self.entry_price = ctk.CTkEntry(self.form_frame, placeholder_text="np. 15.99")
        self.entry_price.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_stock = ctk.CTkLabel(self.form_frame, text="Stan początkowy (szt.):")
        self.lbl_stock.pack(padx=15, anchor="w")
        self.entry_stock = ctk.CTkEntry(self.form_frame, placeholder_text="np. 100")
        self.entry_stock.pack(fill="x", padx=15, pady=(0, 20))

        self.btn_save = ctk.CTkButton(self.form_frame, text="Zapisz w Magazynie", command=self.add_product)
        self.btn_save.pack(fill="x", padx=15, pady=10)

        self.lbl_status = ctk.CTkLabel(self.form_frame, text="", text_color="green")
        self.lbl_status.pack(pady=5)

        # --- PRAWY PANEL: LISTA PRODUKTÓW ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")

        list_title = ctk.CTkLabel(self.list_frame, text="Aktualne Stany Magazynowe", font=ctk.CTkFont(size=18, weight="bold"))
        list_title.pack(pady=15, padx=15, anchor="w")

        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame)
        self.scrollable_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.refresh_product_list()

    def add_product(self):
        name = self.entry_name.get().strip()
        sku = self.entry_sku.get().strip()
        price_str = self.entry_price.get().strip()
        stock_str = self.entry_stock.get().strip()

        if not name or not sku:
            self.lbl_status.configure(text="Nazwa i SKU są wymagane!", text_color="red")
            return

        try:
            price = float(price_str) if price_str else 0.0
            stock = int(stock_str) if stock_str else 0
        except ValueError:
            self.lbl_status.configure(text="Cena i stan muszą być liczbami!", text_color="red")
            return

        db = SessionLocal()
        new_product = Product(name=name, sku=sku, price=price, stock_quantity=stock)
        try:
            db.add(new_product)
            db.commit()
            
            self.entry_name.delete(0, 'end')
            self.entry_sku.delete(0, 'end')
            self.entry_price.delete(0, 'end')
            self.entry_stock.delete(0, 'end')
            
            self.lbl_status.configure(text="Produkt pomyślnie dodany!", text_color="green")
            self.refresh_product_list()
        except Exception as e:
            db.rollback()
            self.lbl_status.configure(text=f"Błąd: SKU musi być unikalny!", text_color="red")
        finally:
            db.close()

    def refresh_product_list(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        db = SessionLocal()
        try:
            products = db.query(Product).order_by(Product.name.asc()).all()
            
            if not products:
                no_products = ctk.CTkLabel(self.scrollable_list, text="Magazyn jest pusty. Dodaj pierwszy produkt!")
                no_products.pack(pady=20)
                return

            for prod in products:
                card = ctk.CTkFrame(self.scrollable_list, fg_color=["#EAEAEA", "#2B2B2B"], corner_radius=6)
                card.pack(fill="x", pady=5, padx=5)

                info_text = f"📦 {prod.name} | SKU: {prod.sku}"
                
                # Ostrzeżenie o niskim stanie magazynowym
                stock_color = "orange" if prod.stock_quantity < 5 else ["#000000", "#FFFFFF"]
                stock_text = f"Stan: {prod.stock_quantity} szt. | Cena: {prod.price:.2f} PLN"

                lbl_info = ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(weight="bold"))
                lbl_info.pack(anchor="w", padx=10, pady=(5, 2))

                lbl_stock = ctk.CTkLabel(card, text=stock_text, font=ctk.CTkFont(size=11), text_color=stock_color)
                lbl_stock.pack(anchor="w", padx=10, pady=(2, 5))
        except Exception as e:
            err_lbl = ctk.CTkLabel(self.scrollable_list, text=f"Błąd ładowania: {e}", text_color="red")
            err_lbl.pack(pady=20)
        finally:
            db