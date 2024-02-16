# pip install PyPDF2
# pip install PyMuPDF
# The above lines are comments indicating that you need to install these libraries via pip if you haven't already done so.

import sys  # Import the sys module which provides functions and variables used to manipulate different parts of the Python runtime environment.
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,\
    QTextEdit, QMessageBox, QVBoxLayout, QWidget # Import necessary PyQt5 modules for creating the GUI.
from PyQt5.QtCore import Qt  # Import the Qt module from PyQt5 for core functionality.
import fitz  # Import the fitz module from PyMuPDF library for PDF handling.

class PDFPreviewer(QMainWindow):  # Define a class named PDFPreviewer which inherits from QMainWindow.
    def __init__(self):  # Define the constructor method for the PDFPreviewer class.
        super().__init__()  # Call the constructor of the superclass (QMainWindow).

        # Create a central widget to hold the button and text preview
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(100, 100, 100, 100)  # Add margins to the layout

        # Create and configure the "Open PDF" button
        self.btn_open = QPushButton("Open PDF")
        self.btn_open.clicked.connect(self.open_pdf)

        # Create and configure the text preview area
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)

        # Add the button and text preview to the layout
        layout.addWidget(self.btn_open)
        layout.addWidget(self.text_preview)

    def open_pdf(self):  # Define a method to open and display the content of a PDF file.
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")

        if file_path:
            try:
                doc = fitz.open(file_path)
                page = doc.load_page(0)
                page_content = page.get_text()

                self.text_preview.setPlainText(page_content)

                doc.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":  # Check if the script is being run directly.
    app = QApplication(sys.argv)  # Create a QApplication instance.
    window = PDFPreviewer()  # Create an instance of the PDFPreviewer class.
    window.show()  # Show the main window.
    sys.exit(app.exec_())  # Start the event loop and exit the application when it's done.
