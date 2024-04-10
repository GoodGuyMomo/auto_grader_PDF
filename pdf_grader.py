# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QDialog, \
    QLabel, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QTextEdit, QHBoxLayout, QLineEdit, \
        QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPixmap, QImage, QFont, QPainter
from PyQt5.QtCore import Qt
import fitz
from PIL import Image
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem


class PicButton(QPushButton):
    def __init__(self, img, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = QPixmap(img)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)
    

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(100, 20, 100, 20)
        self.setStyleSheet("background-color: grey")

        self.img_splash = QPixmap("graphics/pdfGUI_welcomeBanner.png")
        self.lbl_splash = QLabel()
        self.lbl_splash.setPixmap(self.img_splash)
        layout.addWidget(self.lbl_splash)

        self.add_space(layout, 2)

        self.btn_open = PicButton("graphics/pdfGUI_pdfButton.png")
        self.btn_open.clicked.connect(self.upload_pdf)
        self.btn_open.setFixedSize(900, 150)
        layout.addWidget(self.btn_open)

        self.lbl_pdf = QLabel("", self)
        self.lbl_pdf.setStyleSheet("border: 1px solid black; background-color: white;")
        self.lbl_pdf.setFixedSize(900, 50)
        layout.addWidget(self.lbl_pdf)

        self.add_space(layout, 3)

        # Set a fixed size for the main window
        self.setMinimumSize(1000, 800)  # Adjust the size as need
        
        # Create button to upload comments
        self.btn_comments_upload = PicButton("graphics/pdfGUI_uploadButton.png")
        # Upon being clicked, the upload_comments function is run
        self.btn_comments_upload.clicked.connect(self.upload_comments)
        self.btn_comments_upload.setFixedSize(900, 150)
        layout.addWidget(self.btn_comments_upload)

        self.lbl_comments_upload = QLabel("", self)
        self.lbl_comments_upload.setStyleSheet("border: 1px solid black; background-color: white;")
        self.lbl_pdf.setFixedSize(900, 50)
        layout.addWidget(self.lbl_comments_upload)
        
        self.add_space(layout, 5)
        
        self.btn_submit = PicButton("graphics/pdfGUI_nextButton.png")
        self.btn_submit.clicked.connect(self.submit)
        self.btn_submit.setFixedSize(600, 100)
        layout.addWidget(self.btn_submit, alignment=Qt.AlignCenter)


    def add_space(self, l, times):
        for i in range(times):
            ql = QLabel("")
            ql.setFixedWidth(50)
            l.addWidget(ql)

    # Allows a user to upload a PDF file to the program
    def upload_pdf(self):
        
        # Gets the file path of the PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            # Displays the file path in the textbox
            self.lbl_pdf.setText(file_path)
        
    # Allows a user to select a .txt comments file to upload into the program
    def upload_comments(self):
        
        # Gets the filepath of the comments file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Comments File", "", "Text Files (*.txt)")
        if file_path:
            # Displays the file path in the textbox
            self.lbl_comments_upload.setText(file_path)
        
    def submit(self):
        pdf = self.lbl_pdf.text()
        upload = self.lbl_comments_upload.text()

        if pdf == "": 
            QMessageBox.critical(self, "Error", "Please upload a PDF document") 
        elif upload == "": 
            QMessageBox.critical(self, "Error", "Please upload an comments document") 
        else:  
            with open(upload, 'r') as file:
                ans = file.read()
            print("Loaded comments:", ans)  # Debug print
             
            self.setStyleSheet("background-color: ;")
            #DELETE THE ABOVE LINE ONCE THE GRAPHICS ARE ADDED TO THE SECOND PAGE
            
            next_page = SecondPage(pdf, ans)
            self.setCentralWidget(next_page)
            
class SecondPage(QWidget):
    def __init__(self, pdf_path, comments):
        super().__init__()

        layout = QGridLayout(self)
        layout.setContentsMargins(100, 100, 100, 100)

        #PDF view area --------------------------------------------------------
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area, 1, 1, 8, 1)
        #----------------------------------------------------------------------

        # Set a fixed size for the main window
        self.setMinimumSize(1000, 800)  # Adjust the size as needed
        
        
        # Comments preview table ----------------------------------------------
        self.comment_table = QTableWidget()
        self.comment_table.setColumnCount(4)
        self.comment_table.setHorizontalHeaderLabels(["Export", "Question #:", "Comment:", "Points Deducted:"])
        self.comment_table.verticalHeader().setVisible(False) # Hide the row numbers from the left of the comment table
        self.comment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Set the header to be stretched and fill the table completely

        # Set the size of each column to make the comments section the biggest
        for column in range(self.comment_table.columnCount()):
            if column == 0 or column == 1 or column == 3: # Question column or points column
                self.comment_table.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeToContents)
            else:
                self.comment_table.horizontalHeader().setSectionResizeMode(column, QHeaderView.Stretch)

        # Add the table widget to the layout
        layout.addWidget(self.comment_table, 1, 3, 4, 1) #row 1, column 3, spanning 5 rows and 1 coulmn
        #----------------------------------------------------------------------

        # Export Button
        self.save_comments_button = QPushButton("Export")
        self.save_comments_button.clicked.connect(self.save_comments_to_file)
        layout.addWidget(self.save_comments_button, 5, 3, 2, 1, alignment=Qt.AlignCenter)
        
        # Adding comments area ------------------------------------------------
        comment_layout = QHBoxLayout()
        layout.setSpacing(5)
        
        # QUESTION LABEL
        self.questions_label = QLabel("Question #:")
        comment_layout.addWidget(self.questions_label)
        # QUESTION BOX
        self.questions_edit = QLineEdit()
        self.questions_edit.setFixedWidth(30)
        self.questions_edit.setFixedHeight(25)
        comment_layout.addWidget(self.questions_edit)
        
        # COMMENT LABEL
        self.comment_label = QLabel("Comment:")
        comment_layout.addWidget(self.comment_label)
        # COMMENT BOX
        self.comment_text_edit = QTextEdit()
        self.comment_text_edit.setFixedHeight(25)
        comment_layout.addWidget(self.comment_text_edit)
        
        # POINT LABEL
        self.points_label = QLabel("Points off:")
        comment_layout.addWidget(self.points_label)
        # POINT BOX
        self.points_edit = QLineEdit()
        self.points_edit.setText("0") # This will initially set the points box to 0
        self.points_edit.setFixedWidth(30)
        self.points_edit.setFixedHeight(25)
        comment_layout.addWidget(self.points_edit)
        
        # ADD BUTTON
        self.add_comment_button = QPushButton("Add")
        self.add_comment_button.setFixedWidth(80)
        self.add_comment_button.setFixedHeight(25)
        self.add_comment_button.clicked.connect(self.add_comment)
        comment_layout.addWidget(self.add_comment_button)

        # LAYOUT SETTINGS
        layout.addLayout(comment_layout, 5, 3, 1, 1)

        # Store the comments in a list
        self.comments = []

        '''
        NEED TO ADD THESE TO THE TABLE ABOVE
        self.comments_display = QTextEdit()
        self.comments_display.setReadOnly(True)

        # Using !important to ensure these styles take precedence
        self.comments_display.setStyleSheet("QTextEdit {color: black; background-color: #f0f0f0;}")
    
        # Setting text color directly using QPalette
        #palette = self.comments_display.palette()
        #palette.setColor(QPalette.Text, Qt.black)
        #self.comments_display.setPalette(palette)
    
        #self.comments_display.setText(comments)  # Display the comments
        self.comments_display.setPlainText(comments)
        self.comments_display.setFont(QFont("Arial", 12))
        print("TextEdit size:", self.comments_display.size())
        print("TextEdit visibility:", self.comments_display.isVisible())
        layout.addWidget(self.comments_display, 6, 0, 1, 3)  # Add the comments_display to the layout
        '''
    
        file_path = pdf_path
        if file_path:
            try:
                pdf_document = fitz.open(file_path)

                self.clear_scroll_layout()

                for page_number in range(pdf_document.page_count):
                    page = pdf_document[page_number]
                    
                    # Print the text on the page
                    text = page.get_text("text")
                    print(f"Page {page_number + 1}:\n{text}\n")

                    # Display the page as an image
                    pix = page.get_pixmap()
                    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    
                    # Convert the image to QImage
                    q_image = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888)

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
                    self.scroll_layout.addWidget(image_label)

                pdf_document.close()
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    # Allows user to upload a txt file containing comments and points
    # Assumes the format that the first line contains the comment and the second line is the 
    # number of points lost
    def upload_comments(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Comments File", "", "Text Files (*.txt)")

        if file_path:
            try:
                comments = []
                points = []

                # Open text file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Iterate through lines and process comments and points
                    for i in range(0, len(lines), 2):
                        comments.append(lines[i].strip())
                        points.append(int(lines[i + 1].strip()))

                # Output comments and points to check list contents
                print("Comments:", comments)
                print("Points:", points)

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        

    def clear_scroll_layout(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def add_checkboxes_to_table(self):
        # Add checkboxes to the first column of the table widget
        for row in range(self.comment_table.rowCount()):
            checkbox = QCheckBox()
            self.comment_table.setCellWidget(row, 0, checkbox)

    # KEVIN UPDATED THIS FUNCTION
    def add_comment(self):
        # Allow a comment and question to be added and points deducted
        comment_text = self.comment_text_edit.toPlainText()
        points_text = self.points_edit.text()
        questions_text = self.questions_edit.text()
    
        # Append the question, comment, and points to the comments list
        self.comments.append((questions_text, comment_text, points_text))
    
        # Add a new row to the table widget
        row_position = self.comment_table.rowCount()
        self.comment_table.insertRow(row_position)
    
        # Add a checkbox to the first column of the new row
        checkbox = QCheckBox()
        checkbox_layout = QHBoxLayout()  # Set layout for the checkbox
        checkbox_layout.addWidget(checkbox, alignment=Qt.AlignCenter)  # Add checkbox to the layout
        checkbox_layout.setContentsMargins(0, 0, 0, 0)  # Set layout margins
        cell_widget = QWidget()  # Create a widget to hold the checkbox
        cell_widget.setLayout(checkbox_layout)  # Set layout for the widget
        self.comment_table.setCellWidget(row_position, 0, cell_widget)  # Set widget in the table cell
    
        # Add the question, comment, and points to the appropriate columns
        self.comment_table.setItem(row_position, 1, QTableWidgetItem(questions_text))
        self.comment_table.setItem(row_position, 2, QTableWidgetItem(comment_text))
        self.comment_table.setItem(row_position, 3, QTableWidgetItem(points_text))
    
        # Clear the comment and points fields
        self.questions_edit.clear()
        self.comment_text_edit.clear()
        self.points_edit.setText("0") # Autofills points box with zero

    # Exports the checked rows into a file
    def save_comments_to_file(self):
        # Allows the user to choose where to save the file and what to name it
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Comments", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    # Checks which rows are checked and will be included in the export
                    for row in range(self.comment_table.rowCount()):
                        checkbox_item = self.comment_table.cellWidget(row, 0)
                        if isinstance(checkbox_item, QWidget):  # Check if the cell contains a widget
                            checkbox_layout = checkbox_item.layout()
                            checkbox = checkbox_layout.itemAt(0).widget()  # Get the checkbox from the layout
                            if checkbox.isChecked():
                                question = self.comment_table.item(row, 1).text()
                                comment = self.comment_table.item(row, 2).text()
                                points = self.comment_table.item(row, 3).text()
                                file.write(f"Question #: {question}\nComment: {comment}\nPoints Deducted: {points}\n\n")
                QMessageBox.information(self, "Success", "Your selected comments were saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving your comments: {str(e)}")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())