import customtkinter as ctk
from tkinter import filedialog
import threading
import os
from pypdf import PdfReader

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DocumentAnalyzer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Poprawiony tytuł okna
        self.title("Smart PDF & Text Document Analyzer")
        self.geometry("850x600")

        self.selected_file_path = ""

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_file_picker()
        self._build_editor()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Poprawiony nagłówek w aplikacji
        self.lbl_title = ctk.CTkLabel(
            self.header_frame, 
            text="📄 Analizator Dokumentów (PDF / TXT)", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_title.pack(anchor="w")

    def _build_file_picker(self):
        self.card_frame = ctk.CTkFrame(self)
        self.card_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.btn_browse = ctk.CTkButton(
            self.card_frame, 
            text="Otwórz Plik (PDF/TXT)", 
            command=self._select_file
        )
        self.btn_browse.pack(side="left", padx=15, pady=15)

        self.lbl_file_name = ctk.CTkLabel(
            self.card_frame, 
            text="Brak wybranego pliku", 
            text_color="gray"
        )
        self.lbl_file_name.pack(side="left", padx=10, pady=15)

        self.btn_process = ctk.CTkButton(
            self.card_frame, 
            text="Przeanalizuj Dokument", 
            fg_color="#8e44ad", 
            hover_color="#732d91",
            state="disabled",
            command=self._process_document
        )
        self.btn_process.pack(side="right", padx=15, pady=15)

    def _build_editor(self):
        self.txt_result = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13))
        self.txt_result.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.txt_result.insert("1.0", "Wybierz plik z dysku, aby rozpocząć odczyt i analizę...")

    def _select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Pliki PDF i TXT", "*.pdf *.txt")]
        )
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            self.lbl_file_name.configure(text=file_name, text_color="white")
            self.btn_process.configure(state="normal")

    def _process_document(self):
        self.btn_process.configure(state="disabled")
        self.txt_result.delete("1.0", "end")
        self.txt_result.insert("1.0", "⏳ Odczytywanie pliku i analiza zawartości w tle...\n")

        threading.Thread(target=self._analyze_file_thread, daemon=True).start()

    def _analyze_file_thread(self):
        try:
            extracted_text = ""
            file_ext = os.path.splitext(self.selected_file_path)[1].lower()

            if file_ext == ".txt":
                with open(self.selected_file_path, "r", encoding="utf-8") as f:
                    extracted_text = f.read()

            elif file_ext == ".pdf":
                reader = PdfReader(self.selected_file_path)
                
                text_runs = []
                for idx, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_runs.append(f"--- STRONA {idx+1} ---\n{page_text}")
                
                extracted_text = "\n\n".join(text_runs)

            if not extracted_text.strip():
                analysis_report = "⚠️ Plik nie zawiera żadnego możliwego do odczytania tekstu (może to być skan/obraz)."
            else:
                analysis_report = self._generate_analysis_report(extracted_text)

            self.after(0, self._show_result, analysis_report)

        except Exception as e:
            err_msg = f"❌ Wystąpił błąd podczas odczytu pliku:\n{str(e)}"
            self.after(0, self._show_result, err_msg)

    def _generate_analysis_report(self, text: str) -> str:
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        lines_count = len(text.splitlines())

        keywords = ["umowa", "termin", "koszt", "cena", "zalecenia", "zł", "pln", "ważne", "uwaga", "dane"]
        found_sentences = []

        sentences = text.replace("\n", " ").split(".")
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in keywords):
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 10 and clean_sentence not in found_sentences:
                    found_sentences.append(clean_sentence)

        report = []
        report.append("==================================================")
        report.append("          RAPORT ANALIZY DOKUMENTU                ")
        report.append("==================================================\n")
        
        report.append("📊 METRYKI PLIKU:")
        report.append(f"  • Liczba słów: {word_count}")
        report.append(f"  • Liczba znaków: {char_count}")
        report.append(f"  • Liczba linii/akapitów: {lines_count}\n")

        report.append("🔑 WYZNACZONE ZDANIA KLUCZOWE (Kontekst):")
        if found_sentences:
            for idx, s in enumerate(found_sentences[:5], start=1):
                report.append(f"  {idx}. \"{s}.\"")
        else:
            report.append("  • Nie znaleziono standardowych fraz kluczowych w tekście.")

        report.append("\n" + "="*50)
        report.append("📝 PEŁNA TREŚĆ DOKUMENTU (PODGLĄD):")
        report.append("="*50 + "\n")
        report.append(text[:2000] + ("\n\n[... przycięto długi tekst ...]" if len(text) > 2000 else ""))

        return "\n".join(report)

    def _show_result(self, result_text: str):
        self.txt_result.delete("1.0", "end")
        self.txt_result.insert("1.0", result_text)
        self.btn_process.configure(state="normal")


if __name__ == "__main__":
    app = DocumentAnalyzer()
    app.mainloop()