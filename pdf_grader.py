'''
Make sure to have these pip installed:
pip install PyPDF2
pip install PyMuPDF   
pip install Pillow
'''


import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, \
    QDialog, QLabel, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QTextEdit, \
        QHBoxLayout, QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, \
            QHeaderView, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QFont, QPainter, QIcon, QIntValidator, QValidator
from PyQt5.QtCore import Qt
import fitz
from PIL import Image
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem
import os
from os.path import splitext, basename


class PicButton(QPushButton):
    def __init__(self, img, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = QPixmap(img)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)


# Get the directory of the current script
current_dir = os.path.dirname(__file__)

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set a fixed size for the main window
        self.setMinimumSize(1000, 800)  # Adjust the size as need

        #MAIN SCREEN SETTING --------------------------------------------------
        #Create a vertical box layout for the widget
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(100, 20, 100, 20) #set the margins
        self.setStyleSheet("background-color: white") #background color
        self.img_splash = QPixmap(os.path.join(current_dir, "graphics/pdfGUI_welcomeBanner.png"))
        #----------------------------------------------------------------------
        
        
        #ADDING ELEMENTS TO MAIN PAGE -----------------------------------------
        #Top banner
        self.lbl_splash = QLabel() #crreate a label for the banner
        self.lbl_splash.setPixmap(self.img_splash) #set map for banner
        layout.addWidget(self.lbl_splash, alignment=Qt.AlignCenter) #add to layout'
        
        self.add_space(layout, 2) #spacing

        #Open PDF butoon
        self.btn_open = PicButton(os.path.join(current_dir, "graphics/pdfGUI_pdfButton.png"))
        self.btn_open.clicked.connect(self.upload_pdf)
        self.btn_open.setFixedSize(900, 150)
        layout.addWidget(self.btn_open, alignment=Qt.AlignCenter) #add to layout

        #Text box for PDF file path disply - not needed for now
        self.lbl_pdf = QLabel("", self)
        #self.lbl_pdf.setStyleSheet("border: 1px solid black; background-color: white;")
        #self.lbl_pdf.setFixedSize(900, 50)
        #layout.addWidget(self.lbl_pdf)
        
        self.add_space(layout, 1) #spacing

        
        # Upload comments button
        self.btn_comments_upload = PicButton(os.path.join(current_dir,"graphics/pdfGUI_uploadButton.png"))
        self.btn_comments_upload.clicked.connect(self.upload_comments)
        self.btn_comments_upload.setFixedSize(900, 150)
        layout.addWidget(self.btn_comments_upload, alignment=Qt.AlignCenter) #add to layout

        #Text box for PDF file path disply - not needed for now
        self.lbl_comments_upload = QLabel("", self)
        #self.lbl_comments_upload.setStyleSheet("border: 1px solid black; background-color: white;")
        #self.lbl_pdf.setFixedSize(900, 50)
        #layout.addWidget(self.lbl_comments_upload)
        
        self.add_space(layout, 1) #spacing
        
        
        # Total Points Textbox
        self.total_points = QLineEdit()
        self.total_points.setText("Type the total points here...")
        self.total_points.setReadOnly(False)
        self.total_points.setStyleSheet("background-color: white; border: 1px solid black;")
        self.total_points.setFixedWidth(850)
        self.total_points.setFixedHeight(70)
        layout.addWidget(self.total_points, alignment=Qt.AlignCenter) #add to layout
        
        # Total Points Save Button
        points_save_button = QPushButton("Save Total Points")
        points_save_button.clicked.connect(self.save_points)
        self.btn_comments_upload.setFixedSize(900, 150)
        self.btn_comments_upload.setStyleSheet("background-color: lightblue")
        layout.addWidget(points_save_button, alignment=Qt.AlignCenter)
        
        self.add_space(layout, 5) #spacing
        
        #Submit button
        self.btn_submit = PicButton(os.path.join(current_dir,"graphics/pdfGUI_nextButton.png"))
        self.btn_submit.clicked.connect(self.submit)
        self.btn_submit.setFixedSize(600, 100)
        layout.addWidget(self.btn_submit, alignment=Qt.AlignCenter) #add to layout
        #----------------------------------------------------------------------


    def add_space(self, l, times):
        for i in range(times):
            ql = QLabel("")
            ql.setFixedWidth(50)
            l.addWidget(ql)

    def save_points(self):
        global points
    
        # Validate input
        validator = QIntValidator()
        if validator.validate(self.total_points.text(), 0)[0] == QValidator.Acceptable:
            points = int(self.total_points.text())
            self.points = points  # Store total points as an attribute
            QMessageBox.information(self, "Points Saved", "Points has been saved.")
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer for total points.")
            
            

    # Allows a user to upload a folder of PDFs
    # Updated 4/15
    def upload_pdf(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder of PDFs")
        if folder_path:
            # List all PDF files in the folder
            pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]
            if pdf_files:
                self.lbl_pdf.setText(folder_path)  # Display folder path
                self.pdf_files = [os.path.join(folder_path, file) for file in pdf_files]
                self.current_pdf_index = 0  # Initialize current PDF index
                QMessageBox.information(self, "Success", "Folder successfully uploaded")
            else:
                QMessageBox.critical(self, "Error", "No PDF files found in the selected folder")
        
    
    
    
    # Allows a user to select a .txt comments file to upload into the program
    def upload_comments(self):
        global comments_path
        
        # Gets the filepath of the comments file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Comments File", "", "Text Files (*.txt)")
        if file_path:
            # Displays the file path in the textbox
            self.lbl_comments_upload.setText(file_path)
            QMessageBox.information(self, "Success", "Comments successfully uploaded")
        
        comments_path = file_path
    
        
    def submit(self):
        pdf = self.lbl_pdf.text()
        upload = self.lbl_comments_upload.text()
    
        if pdf == "":
            QMessageBox.critical(self, "Error", "Please upload a PDF document")
        elif upload == "":
            QMessageBox.critical(self, "Error", "Please upload a comments document")
        else:  
            # Switch content within MainPage
            self.second_page = SecondPage(pdf, self.pdf_files, points, comments_path)  # Pass pdf_files to SecondPage
            self.setCentralWidget(self.second_page)
            self.second_page.load_pdf()  # Load the first PDF on the SecondPage


            
class SecondPage(QWidget):
    def __init__(self, pdf_path, pdf_files, points, comments_path):
        super().__init__()
        
        # Grabbing Info -------------------------------------------------------
        self.pdf_path = pdf_path
        self.pdf_files = pdf_files  # Store the list of PDF files
        self.pdf_index = 0  # Index to keep track of the current PDF
        self.current_pdf_index = 0  # Initialize the current PDF index
        
        
        self.current_pdf_name = None
        if pdf_files:
            self.current_pdf_name = basename(pdf_files[self.pdf_index])
            
        #grab points from the previous page
        self.points = points
        # ---------------------------------------------------------------------
        
        
        
        
        #MAIN SCREEN SETTING --------------------------------------------------
        #Create a vertical box layout for the widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(100, 20, 100, 20) #set the margins
        self.setStyleSheet("background-color: white") #background color
       
        # Set a fixed size for the main window
        self.setMinimumSize(2000, 2000)  # Adjust the size as needed

        
        # Back button ---------------------------------------------------------
        self.back_button = QPushButton("Back to Main Screen")
        self.back_button.clicked.connect(self.go_to_main_page)
        self.back_button.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        

        
        #PDF view area --------------------------------------------------------
        #PDF Layout 
        pdf_layout = QVBoxLayout()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setMaximumHeight(1500)
        pdf_layout.addWidget(self.scroll_area)
        
        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        
        # Previous PDF button
        self.previous_button = PicButton(os.path.join(current_dir, "graphics/prev_arrow.png"))
        self.previous_button.clicked.connect(self.load_previous_pdf)
        button_layout.addWidget(self.previous_button, alignment=Qt.AlignLeft)
        
        # Next PDF button
        self.next_button = PicButton(os.path.join(current_dir, "graphics/next_arrow.png"))
        self.next_button.clicked.connect(self.load_next_pdf)
        button_layout.addWidget(self.next_button, alignment=Qt.AlignRight)
        
        # Add button layout to the main layout
        pdf_layout.addLayout(button_layout)
        #----------------------------------------------------------------------
        
        
        # Comments preview table ----------------------------------------------
        #comments layout
        comments_layout = QVBoxLayout()
        
        self.comment_table = QTableWidget()
        self.comment_table.setColumnCount(4)
        self.comment_table.setHorizontalHeaderLabels(["Export", "Question #:", "Comment:", "Points Deducted:"])
        self.comment_table.verticalHeader().setVisible(False) # Hide the row numbers from the left of the comment table
        self.comment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Set the header to be stretched and fill the table completely
        
        # Set size policy for the table widget
        self.comment_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the size of each column to make the comments section the biggest
        for column in range(self.comment_table.columnCount()):
            if column == 0 or column == 1 or column == 3: # Question column or points column
                self.comment_table.horizontalHeader().setSectionResizeMode(column, QHeaderView.ResizeToContents)
            else:
                self.comment_table.horizontalHeader().setSectionResizeMode(column, QHeaderView.Stretch)

        self.comment_table.setMaximumHeight(1200)
        self.fill_comments() #fill in the comments
        
        # Add the table widget to the layout
        comments_layout.addWidget(self.comment_table)
        #----------------------------------------------------------------------
        
        
        # Adding comments area ------------------------------------------------
        comm_layout = QHBoxLayout()
        
        # QUESTION LABEL
        self.questions_label = QLabel("Question #:")
        self.questions_label.setStyleSheet("background-color: #FFCCCC;")
        comm_layout.addWidget(self.questions_label)
        comm_layout.setSpacing(5)
        
        # QUESTION BOX
        self.questions_edit = QLineEdit()
        comm_layout.addWidget(self.questions_edit)
        comm_layout.setSpacing(10)
        
        # POINT LABEL
        self.points_label = QLabel("Points off:")
        self.points_label.setStyleSheet("background-color: #FFCCCC")
        comm_layout.addWidget(self.points_label)
        comm_layout.setSpacing(5)
        
        # POINT BOX
        self.points_edit = QLineEdit()
        self.points_edit.setText("0") # This will initially set the points box to 0
        comm_layout.addWidget(self.points_edit)
        
        comments_layout.setSpacing(5)
        comments_layout.addLayout(comm_layout)
        comments_layout.setSpacing(5)
        
        # COMMENT LABEL
        self.comment_label = QLabel("Comment:")
        self.comment_label.setAlignment(Qt.AlignCenter)
        self.comment_label.setStyleSheet("background-color: #FFCCCC;")
        self.comment_label.setFixedHeight(40)
        comments_layout.addWidget(self.comment_label)
        
        # COMMENT BOX
        self.comment_text_edit = QTextEdit()
        self.comment_text_edit.setFixedHeight(100)
        comments_layout.addWidget(self.comment_text_edit)
        comments_layout.setSpacing(10)
        
        # ADD BUTTON
        self.add_comment_button = QPushButton("Add")
        self.add_comment_button.setFixedHeight(50)
        self.add_comment_button.clicked.connect(self.add_comment)
        self.add_comment_button.setStyleSheet("background-color: #lightblue;")
        comments_layout.addWidget(self.add_comment_button)
        comments_layout.setSpacing(30)
        
        # Export Button
        self.save_comments_button = QPushButton("Export")
        self.save_comments_button.clicked.connect(self.save_comments_to_file)
        self.save_comments_button.setStyleSheet("background-color: lightblue;")
        comments_layout.addWidget(self.save_comments_button)
        # ---------------------------------------------------------------------

        # LAYOUT SETTINGS
        document_layout = QHBoxLayout()  #for side-by-side arrangement
        
        # Add the PDF view area to the document layout
        document_layout.addLayout(pdf_layout)
        
        # Add some spacing between the PDF view area and comments preview table
        document_layout.addSpacing(20)
        
        # Add the comments layout to the document layout
        document_layout.addLayout(comments_layout)
        
        # Add the document layout to the main layout
        layout.addLayout(document_layout)

        

        # Store the comments in a list
        self.comments = []
        
        # Load the first PDF when the SecondPage is initialized
        self.load_pdf()

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
    
    # Add the load_pdf() method to load and display PDFs
    # Load PDF on second page
    def load_pdf(self):
        try:
            self.clear_scroll_layout()
            pdf_files = [file for file in os.listdir(self.pdf_path) if file.endswith('.pdf')]
            if pdf_files:
                pdf_file = pdf_files[self.pdf_index]
                pdf_document = fitz.open(os.path.join(self.pdf_path, pdf_file))
                for page_number in range(pdf_document.page_count):
                    page = pdf_document[page_number]
                    pix = page.get_pixmap()
                    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    q_image = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888)
                    if not q_image.isNull():
                        image_label = QLabel()
                        image_label.setPixmap(QPixmap.fromImage(q_image))
                        self.scroll_layout.addWidget(image_label)
                pdf_document.close()
            else:
                QMessageBox.critical(self, "Error", "No PDF files found in the selected folder")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    # Load previous PDF
    def load_previous_pdf(self):
        if self.pdf_index > 0:
            self.pdf_index -= 1
            self.load_pdf()

    # Load next PDF
    def load_next_pdf(self):
        if self.pdf_index < len(self.pdf_files) - 1:
            self.pdf_index += 1
            self.load_pdf()
            
    def clear_scroll_layout(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def fill_comments(self):
        if comments_path:
            try:
                with open(comments_path, 'r') as file:
                    lines = file.readlines()
    
                    # Iterate through lines and process comments and points
                    for i in range(0, len(lines), 3):
                        question = lines[i].strip()
                        comment = lines[i + 1].strip()
                        points = int(lines[i + 2].strip()) if i + 2 < len(lines) else 0  # Default points to 0 if not provided
                        # Add the comment to the table
                        self.add_comment_to_table(question, comment, points)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def add_comment_to_table(self, question, comment, points):
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
        self.comment_table.setItem(row_position, 1, QTableWidgetItem(question))
        self.comment_table.setItem(row_position, 2, QTableWidgetItem(comment))
        self.comment_table.setItem(row_position, 3, QTableWidgetItem(str(points)))



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

    def calculate_total_score(self):
        # Iterate over the rows of the table to calculate total score
        total_score = int(self.points)  # Assuming points is the total points saved from the first page
        
        # Iterate over the rows of the table
        for row in range(self.comment_table.rowCount()):
            checkbox_item = self.comment_table.cellWidget(row, 0)
            if isinstance(checkbox_item, QWidget):  # Check if the cell contains a widget
                checkbox_layout = checkbox_item.layout()
                checkbox = checkbox_layout.itemAt(0).widget()  # Get the checkbox from the layout
                if checkbox.isChecked():
                    points = int(self.comment_table.item(row, 3).text())
                    total_score -= points
    
        return total_score
    
    # Exports the checked rows into a file
    def save_comments_to_file(self):
        # Automatically prefill the filename with the current PDF name and comments
        default_filename = f"{self.current_pdf_name}_comments.txt"
        
        # Allows the user to choose where to save the file and what to name it
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Comments", default_filename, "Text Files (*.txt)")
        if file_path:
            try:
                total_score = int(self.points)  # Assuming points is the total points saved from the first page
                with open(file_path, 'w') as file:
                    
                    # Calculate the total score
                    total_score = self.calculate_total_score()
                    # Write the total score to the file
                    file.write(f"Total Score: {total_score}\n\n")
                    
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
       
    # Allows the user to return to the main page
    def go_to_main_page(self):
        main_window = self.window()
        if main_window is not None:
            main_page = MainPage()
            main_window.setCentralWidget(main_page)

def run():
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
