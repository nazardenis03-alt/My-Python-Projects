from sqlalchemy.orm import Session
from database.models import Invoice, Order, Product
from database.db_manager import get_db
from config import EXPORTS_DIR
import datetime
import os

# Importy Matplotlib do generowania wykresów biznesowych
import matplotlib
matplotlib.use('Agg')  # Tryb bez okna graficznego (wymagany do integracji z Tkinter)
import matplotlib.pyplot as plt

class AnalyticsModule:
    @staticmethod
    def get_basic_stats() -> dict:
        """Oblicza kluczowe wskaźniki efektywności (KPI) dla firmy."""
        db: Session = get_db()
        try:
            invoices = db.query(Invoice).all()
            orders = db.query(Order).all()
            products = db.query(Product).all()

            total_revenue = sum(i.total_gross for i in invoices if i.status == "PAID")
            pending_revenue = sum(i.total_gross for i in invoices if i.status == "UNPAID")
            total_orders = len(orders)
            
            # Produkty z niskim stanem magazynowym
            low_stock_count = sum(1 for p in products if p.stock_quantity <= p.min_stock_level)

            return {
                "total_revenue": total_revenue,
                "pending_revenue": pending_revenue,
                "total_orders": total_orders,
                "low_stock_count": low_stock_count
            }
        finally:
            db.close()

    @staticmethod
    def generate_revenue_chart() -> str:
        """Generuje wykres przychodów firmy i zapisuje go jako plik PNG."""
        db: Session = get_db()
        try:
            invoices = db.query(Invoice).order_by(Invoice.issue_date.asc()).all()
            
            # Agregacja przychodów miesięcznych
            monthly_data = {}
            for inv in invoices:
                month_key = inv.issue_date.strftime("%Y-%m")
                monthly_data[month_key] = monthly_data.get(month_key, 0.0) + inv.total_gross

            if not monthly_data:
                # Dane domyślne, jeśli baza jest pusta
                monthly_data = {datetime.datetime.now().strftime("%Y-%m"): 0.0}

            months = list(monthly_data.keys())
            revenues = list(monthly_data.values())

            # Tworzenie wykresu Matplotlib
            plt.figure(figsize=(6, 3.5), facecolor='#1F2937')
            ax = plt.axes()
            ax.set_facecolor('#111827')

            plt.bar(months, revenues, color='#3B82F6', width=0.4)
            
            # Stylizacja wykresu pod ciemny motyw systemu (Dark Mode)
            plt.title("Przychody w ujęciu miesięcznym (PLN)", color='#F9FAFB', fontsize=12, pad=15)
            plt.xticks(rotation=15, color='#9CA3AF')
            plt.yticks(color='#9CA3AF')
            
            ax.spines['bottom'].color = '#374151'
            ax.spines['top'].color = '#374151'
            ax.spines['left'].color = '#374151'
            ax.spines['right'].color = '#374151'
            ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#374151')

            plt.tight_layout()
            
            # Zapis wykresu do folderu exports
            chart_path = os.path.join(EXPORTS_DIR, "revenue_chart.png")
            plt.savefig(chart_path, dpi=150, facecolor='#1F2937')
            plt.close()

            return chart_path
        finally:
            db.close()

    @staticmethod
    def generate_category_chart() -> str:
        """Generuje wykres udziału kategorii produktowych w magazynie."""
        db: Session = get_db()
        try:
            products = db.query(Product).all()
            
            category_data = {}
            for p in products:
                category_data[p.category] = category_data.get(p.category, 0) + p.stock_quantity

            if not category_data:
                category_data = {"Brak danych": 0}

            categories = list(category_data.keys())
            quantities = list(category_data.values())

            # Tworzenie wykresu kołowego
            plt.figure(figsize=(5, 3.5), facecolor='#1F2937')
            colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6']
            
            plt.pie(
                quantities, 
                labels=categories, 
                autopct='%1.1f%%', 
                startangle=140, 
                textprops={'color': '#F9FAFB', 'fontsize': 9},
                colors=colors[:len(categories)]
            )
            
            plt.title("Struktura zapasów magazynowych", color='#F9FAFB', fontsize=12, pad=15)
            plt.tight_layout()

            chart_path = os.path.join(EXPORTS_DIR, "category_chart.png")
            plt.savefig(chart_path, dpi=150, facecolor='#1F2937')
            plt.close()

            return chart_path
        finally:
            db.close()