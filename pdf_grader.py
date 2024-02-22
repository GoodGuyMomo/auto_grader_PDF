# pip install PyPDF2 DONE
# pip install PyMuPDF DONE
# The above lines are comments indicating that you need to install these libraries via pip if you haven't already done so.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,\
    QLabel, QVBoxLayout, QWidget, QMessageBox, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import fitz

class PDFPreviewer(QMainWindow): # Define a class named PDFPreviewer which inherits from QMainWindow.
    def __init__(self): # Define the constructor method for the PDFPreviewer class.
        super().__init__() # Call the constructor of the superclass (QMainWindow).

        # Create the main window and its central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(100, 100, 100, 100)  # Set margins for the layout

        # Create a button to open a PDF file
        self.btn_open = QPushButton("Open PDF")
        self.btn_open.clicked.connect(self.open_pdf)  # Connect the button click event to the open_pdf method

        # Create a scroll area to contain the PDF page labels
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow the scroll area widget to resize

        # Create a widget to serve as the contents of the scroll area
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)  # Create a layout for the scroll widget
        self.scroll_area.setWidget(self.scroll_widget)  # Set the scroll widget as the content of the scroll area

        # Add the button and the scroll area to the layout of the central widget
        layout.addWidget(self.btn_open)
        layout.addWidget(self.scroll_area)

    def open_pdf(self):
        # Open a file dialog to select a PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        
        if file_path:
            try:
                # Open the PDF document
                doc = fitz.open(file_path)
                page_count = doc.page_count  # Get the number of pages in the PDF

                # Clear any previous content from the scroll layout
                self.clear_scroll_layout()

                # Display each page of the PDF as an image in the scroll area
                for page_number in range(page_count):
                    pixmap = doc[page_number].get_pixmap()  # Get the pixmap for the current page
                    
                    if not pixmap:
                        print("Pixmap is None for page", page_number)
                        continue  # Skip to the next page if the pixmap is None
                    
                    # Convert the pixmap to QImage
                    q_image = QImage(pixmap.tobytes(), pixmap.width, pixmap.height, QImage.Format_RGB888)
                    
                    if q_image.isNull():
                        print("QImage is null for page", page_number)
                        continue  # Skip to the next page if the QImage is null
                    
                    # Convert QImage to QPixmap
                    q_pixmap = QPixmap.fromImage(q_image)
                    
                    if q_pixmap.isNull():
                        print("QPixmap is null for page", page_number)
                        continue  # Skip to the next page if the QPixmap is null
                    
                    # Create a QLabel to display the QPixmap
                    image_label = QLabel()
                    image_label.setPixmap(q_pixmap)
                    self.scroll_layout.addWidget(image_label)  # Add image label to the scroll layout

                doc.close()  # Close the PDF document
            except Exception as e:
                print('check')
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_scroll_layout(self):
        # Clear all widgets from the scroll layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()  # Delete the widget and free its memory

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFPreviewer()
    window.show()
    sys.exit(app.exec_())
