# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QDialog, \
    QLabel, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QTextEdit, QHBoxLayout, QLineEdit, \
        QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
import fitz
from PIL import Image
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout(central_widget)
        layout.setContentsMargins(100, 100, 100, 100)

        self.btn_open = QPushButton("Open PDF")
        self.btn_open.clicked.connect(self.upload_pdf)
        layout.addWidget(self.btn_open, 0, 1)

        self.lbl_pdf = QLabel("", self)
        self.lbl_pdf.setStyleSheet("border: 1px solid black;")
        self.lbl_pdf.adjustSize()
        layout.addWidget(self.lbl_pdf, 1, 1)

        self.add_space(layout, 2, 1)

        # Set a fixed size for the main window
        self.setMinimumSize(850, 900)  # Adjust the size as need
        
        # Create button to upload answers
        self.btn_answer_upload = QPushButton("Upload Answers")
        # Upon being clicked, the upload_answers function is run
        self.btn_answer_upload.clicked.connect(self.upload_answers)
        layout.addWidget(self.btn_answer_upload, 4, 0)

        self.lbl_answer_upload = QLabel("", self)
        self.lbl_answer_upload.setStyleSheet("border: 1px solid black;")
        self.lbl_answer_upload.adjustSize()
        layout.addWidget(self.lbl_answer_upload, 5, 0)

        self.btn_answer_create = QPushButton("Create Answers")
        self.btn_answer_create.clicked.connect(self.create_answers)
        layout.addWidget(self.btn_answer_create, 4, 2)
        
        self.lbl_answer_create = QLabel("", self)
        self.lbl_answer_create.setStyleSheet("border: 1px solid black;")
        self.lbl_answer_create.adjustSize()
        layout.addWidget(self.lbl_answer_create, 5, 2)
        
        self.add_space(layout, 6, 0)
        self.add_space(layout, 6, 2)
        
        self.btn_submit = QPushButton("--- SUBMIT ---")
        self.btn_submit.clicked.connect(self.submit)
        layout.addWidget(self.btn_submit, 7, 1)


    def add_space(self, l, y, x):
        l.addWidget(QLabel(""), y, x)

    # Allows a user to upload a PDF file to the program
    def upload_pdf(self):
        
        # Gets the file path of the PDF file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            # Displays the file path in the textbox
            self.lbl_pdf.setText(file_path)
        
    # Allows a user to select a .txt answer file to upload into the program
    def upload_answers(self):
        
        # Gets the filepath of the answer file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Answer File", "", "Text Files (*.txt)")
        if file_path:
            # Displays the file path in the textbox
            self.lbl_answer_upload.setText(file_path)
            self.lbl_answer_create.setText("")

    def create_answers(self):
        #INSERT FUNCTIONALITY HERE
        self.lbl_answer_create.setText("Idk what goes here lmao")
        self.lbl_answer_upload.setText("")
        
    def submit(self):
        pdf = self.lbl_pdf.text()
        upload = self.lbl_answer_upload.text()
        create = self.lbl_answer_create.text()

        if pdf == "": 
            QMessageBox.critical(self, "Error", "Please upload a PDF document") 
        elif upload == "" and create == "": 
            QMessageBox.critical(self, "Error", "Please upload or create an answer document") 
        else: 
            ans = self.lbl_answer_upload.text() 
            if ans == "": 
                ans = self.lbl_answer_create.text() 
            if upload:
                with open(upload, 'r') as file:
                    ans = file.read()
                print("Loaded answers:", ans)  # Debug print
                 
            
            next_page = SecondPage(pdf, ans)
            self.setCentralWidget(next_page)
            


class SecondPage(QWidget):
    def __init__(self, pdf_path, answers):
        super().__init__()

        layout = QGridLayout(self)
        layout.setContentsMargins(100, 100, 100, 100)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        layout.addWidget(self.scroll_area)

        # Set a fixed size for the main window
        self.setMinimumSize(850, 900)  # Adjust the size as needed
        
        # KEVINS ADDED CODE
        
        # Create a table widget to display the export option, comments, points, and question numbers
        self.comment_table = QTableWidget()
        self.comment_table.setColumnCount(4)
        self.comment_table.setHorizontalHeaderLabels(["Export", "Question #:", "Comment:", "Points Deducted:"])
        
        # Hide the row numbers from the left of the comment table
        self.comment_table.verticalHeader().setVisible(False)

        # Set the header to be stretched and fill the table completely
        self.comment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Set the size of each column to make the comments section the biggest
        for column in range(self.comment_table.columnCount()):
            if column == 1 or column == 3: # Question column or points column
                self.comment_table.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeToContents)
            else:
                self.comment_table.horizontalHeader().setSectionResizeMode(column, QHeaderView.Stretch)

        # Add the table widget to the layout
        layout.addWidget(self.comment_table, 1, 0, 1, 3)

        # Create a layout for the comment, points, and question fields
        comment_layout = QHBoxLayout()
        
        # Create a QLabel for the questions box
        self.questions_label = QLabel("Question:")
        comment_layout.addWidget(self.questions_label)
        
        # Create a QLineEdit for the questions box
        self.questions_edit = QLineEdit()
        self.questions_edit.setFixedWidth(50)
        self.questions_edit.setFixedHeight(30)
        comment_layout.addWidget(self.questions_edit)


       # Create a QLabel for the comments box
        self.comment_label = QLabel("Comments:")
        comment_layout.addWidget(self.comment_label)
        
        # Create a QTextEdit for the comments box
        self.comment_text_edit = QTextEdit()
        self.comment_text_edit.setFixedHeight(30)
        comment_layout.addWidget(self.comment_text_edit)
        
        # Create a QLabel for the points box
        self.points_label = QLabel("Points:")
        comment_layout.addWidget(self.points_label)
        
        # Create a QLineEdit for the points box
        self.points_edit = QLineEdit()
        self.points_edit.setFixedWidth(50)
        self.points_edit.setFixedHeight(30)
        comment_layout.addWidget(self.points_edit)


        # Create a smaller ADD button to add the comments, points, and question number to a list
        self.add_comment_button = QPushButton("Add")
        self.add_comment_button.setFixedWidth(80)
        self.add_comment_button.setFixedHeight(30)
        self.add_comment_button.clicked.connect(self.add_comment)
        comment_layout.addWidget(self.add_comment_button)

        # Add the layout to the main layout
        layout.addLayout(comment_layout, 2, 0, 1, 3)

        # Add the button to save comments to a file and export
        self.save_comments_button = QPushButton("Export")
        self.save_comments_button.clicked.connect(self.save_comments_to_file)

        # Add the comment and scroll widgets
        layout.addWidget(self.save_comments_button, 3, 0, 1, 3)
        layout.addWidget(self.scroll_area, 4, 0, 1, 3)
        
        # Create button to upload answers
        self.upload_answer_button = QPushButton("Upload Answers")
        self.upload_answer_button.clicked.connect(self.upload_answers)
        
        # Add the answer widgets
        layout.addWidget(self.upload_answer_button, 5, 0, 1, 3)

        # Store the comments in a list
        self.comments = []

        # KEVINS ENDED CODE

        # NEW CODE DJF
        
        self.answers_display = QTextEdit()
        self.answers_display.setReadOnly(True)

        # Using !important to ensure these styles take precedence
        self.answers_display.setStyleSheet("QTextEdit {color: black; background-color: #f0f0f0;}")
    
        # Setting text color directly using QPalette
        #palette = self.answers_display.palette()
        #palette.setColor(QPalette.Text, Qt.black)
        #self.answers_display.setPalette(palette)
    
        #self.answers_display.setText(answers)  # Display the answers
        self.answers_display.setPlainText(answers)
        self.answers_display.setFont(QFont("Arial", 12))
        print("TextEdit size:", self.answers_display.size())
        print("TextEdit visibility:", self.answers_display.isVisible())
        layout.addWidget(self.answers_display, 6, 0, 1, 3)  # Add the answers_display to the layout

        # NEW CODE DJF END
    
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
    def upload_answers(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Answer File", "", "Text Files (*.txt)")

        if file_path:
            try:
                answers = []
                points = []

                # Open text file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Iterate through lines and process answers and points
                    for i in range(0, len(lines), 2):
                        answers.append(lines[i].strip())
                        points.append(int(lines[i + 1].strip()))

                # Output answers and points to check list contents
                print("Answers:", answers)
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
        self.points_edit.clear()



    # KEVIN UPDATED THIS FUNCTION
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