import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Client, Product, Order, OrderItem, Invoice, StockMovement
from config import DATABASE_URL

# Inicjalizacja silnika bazy danych SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Tworzy nową sesję bazy danych i dba o jej zamknięcie."""
    db = SessionLocal()
    return db

def init_db():
    """Tworzy wszystkie tabele w bazie danych na podstawie modeli."""
    Base.metadata.create_all(bind=engine)

def seed_database():
    """Generuje realistyczne dane testowe (seed), jeśli baza jest pusta."""
    db = SessionLocal()
    try:
        # Sprawdzamy czy baza jest już uzupełniona (np. czy są użytkownicy)
        if db.query(User).first() is not None:
            return  # Dane już istnieją, nie dodajemy ponownie

        # 1. Dodawanie użytkownika (Administratora)
        admin = User(username="admin", password_hash="admin123", role="ADMIN")
        db.add(admin)

        # 2. Dodawanie przykładowych klientów
        client1 = Client(name="Jan Kowalski", company_name="Kowalski Transport", email="jan@kowalski.pl", phone="123456789")
        client2 = Client(name="Anna Nowak", company_name="Nowak Logistics", email="anna@nowak.pl", phone="987654321")
        db.add_all([client1, client2])
        db.flush()  # Pobranie ID wygenerowanych klientów

        # 3. Dodawanie produktów do magazynu
        prod1 = Product(name="Serwer Rack 1U", sku="SRV-1U-01", category="Sprzęt IT", price=4500.00, stock_quantity=15, min_stock_level=5)
        prod2 = Product(name="Switch 24-Port", sku="SW-24-GIG", category="Sieci", price=1200.00, stock_quantity=3, min_stock_level=5) # Niski stan!
        prod3 = Product(name="Kabel UTP Cat6 305m", sku="CAB-UTP-C6", category="Okablowanie", price=350.00, stock_quantity=50, min_stock_level=10)
        db.add_all([prod1, prod2, prod3])
        db.flush()

        # 4. Dodawanie zamówień i transakcji finansowych
        order1 = Order(client_id=client1.id, status="COMPLETED")
        db.add(order1)
        db.flush()

        item1 = OrderItem(order_id=order1.id, product_id=prod1.id, quantity=2, price=4500.00)
        db.add(item1)
        db.flush()

        # Generowanie faktury do zamówienia
        invoice1 = Invoice(
            order_id=order1.id,
            invoice_number="FV/2026/07/01",
            total_net=9000.00,
            vat_rate=23.0,
            total_gross=11070.00,
            status="PAID",
            issue_date=datetime.date(2026, 7, 10),
            due_date=datetime.date(2026, 7, 24)
        )
        db.add(invoice1)

        # 5. Historia magazynowa (Stock Movement)
        movement = StockMovement(
            product_id=prod1.id,
            movement_type="Przyjęcie (PZ)",
            quantity=15,
            reference_doc="PZ 01/2026"
        )
        db.add(movement)

        db.commit()
        print("Baza danych została pomyślnie zainicjalizowana testowymi danymi!")
    except Exception as e:
        db.rollback()
        print(f"Błąd podczas uzupełniania bazy danych: {e}")
    finally:
        db.close()