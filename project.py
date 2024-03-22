from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QMainWindow , QLineEdit, QHBoxLayout , QWidget ,QPushButton , QVBoxLayout , QLabel, QRadioButton 
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt ,QRegExp
from PyQt5.QtGui import QFont , QIntValidator  ,QRegExpValidator , QIcon
from faker import Faker
import sys
import csv 
import json

fake = Faker()

formatted_functionality = [
    {"func": fake.name, "type": "name"},
    {"func": fake.last_name, "type": "last_name"},
    {"func": fake.email, "type": "email"},
    {"func": fake.phone_number, "type": "phone_number"},
    {"func": fake.address, "type": "address"},
    {"func": fake.text, "type": "text"},
    {"func": fake.date, "type": "date"},
    {"func": fake.time, "type": "time"},
    {"func": fake.url, "type": "url"},
    {"func": fake.job, "type": "job"},
    {"func": fake.company, "type": "company"},
    {"func": fake.country, "type": "country"},
    {"func": fake.currency_code, "type": "currency_code"},
    {"func": fake.file_name, "type": "file_name"},
    {"func": fake.image_url, "type": "image_url"},
    {"func": fake.ipv4, "type": "ipv4"},
    {"func": fake.user_name, "type": "user_name"},
    {"func": fake.color_name, "type": "color_name"},
    {"func": fake.ssn, "type": "ssn"},
    {"func": fake.boolean, "type": "boolean"},
    {"func": fake.credit_card_number, "type": "credit_card_number"},
    {"func": fake.date_of_birth, "type": "date_of_birth"},
    {"func": fake.file_extension, "type": "file_extension"},
    {"func": fake.hex_color, "type": "hex_color"},
    {"func": fake.isbn10, "type": "isbn10"},
    {"func": fake.isbn13, "type": "isbn13"},
    {"func": fake.language_code, "type": "language_code"},
    {"func": fake.mac_address, "type": "mac_address"},
    {"func": fake.mime_type, "type": "mime_type"},
    {"func": fake.password, "type": "password"},
    {"func": fake.random_digit, "type": "random_digit"},
    {"func": fake.random_letter, "type": "random_letter"},
    {"func": fake.street_address, "type": "street_address"},
    {"func": fake.word, "type": "word"},
    {"func": fake.zipcode, "type": "zipcode"},
    {"func": fake.latitude, "type": "latitude"},
    {"func": fake.longitude, "type": "longitude"}
]

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Faker")
        self.setGeometry(100, 100, 800, 600)  
        self.setMaximumHeight(600)
        self.setMinimumHeight(600)
        self.setMaximumWidth(800)
        self.setMinimumWidth(800)
        self.center_on_screen()
        font = QFont("Helvetica") 
        self.setFont(font)
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QLabel#title_label{
                font-size: 32pt;  
                font-weight: bold;  
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
            }
            QCheckBox, QRadioButton {
                font-size: 14px;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 16px;
                background-color: #4CAF50;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QDialog {
                border: 1px solid #45a049;
                width: 300px;
                height: 100px;
            }
        """)
        
        # main_layout 
        main_layout = QHBoxLayout()

        # add three colum the one colum have a list of a fake data
        colum_one = QVBoxLayout()  
        colum_two = QVBoxLayout()
        colum_three = QVBoxLayout()   
        
        # add the content of the list in the three colum 
        checkboxes_per_column = len(formatted_functionality) // 3
        for i in range(0, checkboxes_per_column):
            colum_one.addWidget(QCheckBox(formatted_functionality[i]["type"]))
        for i in range(checkboxes_per_column, checkboxes_per_column * 2):
            colum_two.addWidget(QCheckBox(formatted_functionality[i]["type"]))
        for i in range(checkboxes_per_column * 2, len(formatted_functionality)):
            colum_three.addWidget(QCheckBox(formatted_functionality[i]["type"]))
        
        layout_columns = QHBoxLayout()
        layout_columns.addLayout(colum_one)
        layout_columns.addLayout(colum_two)
        layout_columns.addLayout(colum_three) 

        layout_text = QVBoxLayout()
        # Add a title label 
        title_label = QLabel("Data\nGenerator")
        title_font = QFont("Arial", 32)  
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter) 
        title_label.setObjectName("title_label")  
        layout_text.addWidget(title_label, alignment=Qt.AlignCenter)  

        # File Name layout
        regex = QRegExp("[A-Za-z0-9_]+")
        validator = QRegExpValidator(regex)
        file_layout = QHBoxLayout()
        file_label = QLabel("File Name:")
        file_layout.addWidget(file_label)
        file_input = QLineEdit()
        file_input.setObjectName("file_input")  
        file_input.setPlaceholderText("Enter file name")
        file_input.setFixedSize(200, 30)
        file_input.setValidator(validator)
        file_layout.addWidget(file_input)
        layout_text.addLayout(file_layout)

        # Number of Data layout
        validator_int = QIntValidator()
        number_layout = QHBoxLayout()
        number_label = QLabel("Number of Data:")
        number_layout.addWidget(number_label)
        number_input = QLineEdit()
        number_input.setObjectName("number_input") 
        number_input.setPlaceholderText("Enter number")
        number_input.setFixedSize(200, 30)
        number_input.setValidator(validator_int) 
        number_layout.addWidget(number_input)
        layout_text.addLayout(number_layout)

        # Radio buttons layout
        radio_layout = QHBoxLayout()
        csv_radio_button = QRadioButton("CSV")
        radio_layout.addWidget(csv_radio_button)
        json_radio_button = QRadioButton("JSON")
        radio_layout.addWidget(json_radio_button)
        layout_text.addLayout(radio_layout)

        # Add generate button
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.click)
        
        layout_text.addWidget(generate_button)

        main_layout.addLayout(layout_columns)
        main_layout.addLayout(layout_text)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
    def click(self):
        try :
            number = int(self.get_number())
            if number <= 0:
                raise ValueError("Number of data must be greater than 0")
            elif self.get_radio() == None:
                raise ValueError("Please select a file type")
            elif self.get_name_file() == None:
                raise ValueError("Please enter a file name")
            elif len(self.get_check()) == 0:
                raise ValueError("Please select at least one data type")
            else: 
                make_file(self.get_check(), number, self.get_radio() ,self.get_name_file())
        except ValueError:
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            dlg.setLayout(QVBoxLayout())
            dlg.layout().addWidget(QLabel("Please  provide all information to generate the file."))
            dlg.exec_()

    def get_check(self):
        all_checkboxes = self.findChildren(QCheckBox)
        selected_choices = []
        for checkbox in all_checkboxes:
            if checkbox.isChecked():
                selected_choices.append(checkbox.text())
        return selected_choices
    
    def get_radio(self):
        all_radio_buttons = self.findChildren(QRadioButton)
        selected_radio = None
        for radio_button in all_radio_buttons:
            if radio_button.isChecked():
                selected_radio = radio_button.text()
                break
        return selected_radio

    def get_name_file(self):
        file_input = self.findChild(QLineEdit, "file_input")  
        if file_input:
            return file_input.text()
        return 

    def get_number(self):
        number_input = self.findChild(QLineEdit, "number_input")  
        if number_input:
            return number_input.text()
        return 0
    
    def center_on_screen(self):
        frame_geometry = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        # Move the center of the frame geometry to the center point.
        frame_geometry.moveCenter(center_point)
        # Move the top-left point of the application window to the top-left point of the frame geometry.
        self.move(frame_geometry.topLeft())

def generate_fake_data(selected_choices, number_of_items):
    fake_data = []
    if not selected_choices or not number_of_items:
        raise ValueError("Please provide all information to generate the file.")
    for _ in  range(number_of_items):
        data = {}
        for choice in formatted_functionality:
            if choice["type"] in selected_choices:
                data[choice["type"]] = choice["func"]()
        fake_data.append(data)
    return fake_data

def make_file(selected_choices, number_of_items , type_file , file_name):
    fake_data = generate_fake_data(selected_choices, number_of_items)
    if(type_file == "JSON"):
        write_json(file_name, fake_data)
    else:
        write_csv(file_name, selected_choices, fake_data)

def write_csv(file_name, header , data):
    if not all([file_name, header, data]):
        raise ValueError("Please provide all information to generate the file.")
    if not (isinstance(header, (list, tuple)) or isinstance(data, (dict,list))):
        raise ValueError("Invalid data format")
    with open(f'{file_name}.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def write_json(file_name, data):
    if not file_name or not data:
        raise ValueError("Please provide all information to generate the file.")
    if not isinstance(data, (dict,list, tuple)):
        raise ValueError("Invalid data format")
    with open(f'{file_name}.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():    
    app = QApplication(sys.argv)
    app.setApplicationName("Faker")
    app_icon = QIcon(r'./images/logo.png')
    app.setWindowIcon(app_icon)
    window = Window()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()

