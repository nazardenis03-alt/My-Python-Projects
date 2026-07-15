import datetime
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class OrderStatus(enum.Enum):
    DRAFT = "Szkic"
    PENDING = "Oczekujące"
    IN_PROGRESS = "W realizacji"
    COMPLETED = "Zakończone"
    CANCELLED = "Anulowane"

class InvoiceStatus(enum.Enum):
    UNPAID = "Nieopłacona"
    PAID = "Opłacona"
    OVERDUE = "Przeterminowana"
    CANCELLED = "Anulowana"

class StockMovementType(enum.Enum):
    IN = "Przyjęcie (PZ)"
    OUT = "Wydanie (WZ)"
    ADJUSTMENT = "Korekta"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="USER")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    company_name = Column(String(150))
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    orders = relationship("Order", back_populates="client")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False, default=0.0)
    stock_quantity = Column(Integer, nullable=False, default=0)
    min_stock_level = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    order_items = relationship("OrderItem", back_populates="product")
    movements = relationship("StockMovement", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="DRAFT")
    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    invoice = relationship("Invoice", uselist=False, back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    total_net = Column(Float, nullable=False)
    vat_rate = Column(Float, default=23.0)
    total_gross = Column(Float, nullable=False)
    status = Column(String(50), default="UNPAID")
    issue_date = Column(Date, default=datetime.date.today)
    due_date = Column(Date, nullable=False)
    order = relationship("Order", back_populates="invoice")

class StockMovement(Base):
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference_doc = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship("Product", back_populates="movements")