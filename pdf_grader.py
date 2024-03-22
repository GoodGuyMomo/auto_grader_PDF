# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QDialog, \
    QLabel, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QTextEdit, QHBoxLayout, QLineEdit, \
        QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz
from PIL import Image

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
               
        # Create widgets for comment functionality
        self.comment_text_edit = QTextEdit()
        self.points_edit = QLineEdit()
        self.add_comment_button = QPushButton("Add Comment")
        self.add_comment_button.clicked.connect(self.add_comment)
        
        # Add the button to save comments to a file
        self.save_comments_button = QPushButton("Save Comments")
        self.save_comments_button.clicked.connect(self.save_comments_to_file)
        
        # Add the comment widgets
        layout.addWidget(self.comment_text_edit, 0, 0)
        layout.addWidget(self.points_edit, 1, 0)
        layout.addWidget(self.add_comment_button, 2, 0)
        layout.addWidget(self.save_comments_button, 3, 0)
        layout.addWidget(self.scroll_area, 4, 0)
        
        # Create button to upload answers
        self.upload_answer_button = QPushButton("Upload Answers")
        self.upload_answer_button.clicked.connect(self.upload_answers)
        
        # Add the answer widgets
        layout.addWidget(self.upload_answer_button)

        # Store the comments in a list
        #self.comments = []

    
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
    
    def add_comment(self):
        # Allow a comment to be added and points deducted
        comment_text = self.comment_text_edit.toPlainText()
        points_text = self.points_edit.text()
        self.comments.append((comment_text, str(points_text)))
        self.comment_text_edit.clear()
        self.points_edit.clear()
        print("Comment added: ", comment_text, "| Points Deducted: ", points_text)

    def save_comments_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Comments", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for comment, points in self.comments:
                        file.write(f"Comment: {comment}\tPoints: {points}\n")
                QMessageBox.information(self, "Success", "Your comments were saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occured while saving your comments: {str(e)}")
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())