from PyQt5.QtWidgets import (QApplication, QDialog, QCheckBox, QMainWindow, 
    QLineEdit, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel, 
    QRadioButton, QMessageBox, QScrollArea, QFrame,QComboBox,QListWidget)
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator, QIcon
from faker import Faker
import sys
import csv
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='faker_gui.log'
)
class AttributeInputGroup(QFrame):
    """Custom widget for attribute name input and data type selection"""
    def __init__(self, faker_functions: List[Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.faker_functions = faker_functions
        self.attribute_rows = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Define Data Attributes")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)

        # Scrollable area for attribute inputs
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)  # Align content to top
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        
        # Add initial attribute row
        self.add_attribute_row()
        
        # Add button
        add_button = QPushButton("+ Add Attribute")
        add_button.clicked.connect(self.add_attribute_row)
        self.scroll_layout.addWidget(add_button)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def add_attribute_row(self):
        """Add a new row with attribute name input and data type dropdown"""
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        
        # Attribute name input
        name_input = QLineEdit()
        name_input.setPlaceholderText("Attribute name")
        name_input.setFixedWidth(150)
        
        # Data type dropdown
        type_combo = QComboBox()
        type_combo.setFixedWidth(100)
        for func in self.faker_functions:
            type_combo.addItem(f"{func['type']} - {func['description']}", func['type'])
        
        # Remove button
        remove_button = QPushButton("×")
        remove_button.setFixedSize(20, 30)
        remove_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        remove_button.setStyleSheet("padding: 0px; margin: 0px; font-size: 14px;")
        remove_button.clicked.connect(lambda: self.remove_attribute_row(row_widget))
        
        row_layout.addWidget(name_input)
        row_layout.addWidget(type_combo)
        row_layout.addWidget(remove_button)
        row_layout.addStretch()
        
        # Insert the new row before the Add button
        self.scroll_layout.insertWidget(len(self.attribute_rows), row_widget)
        self.attribute_rows.append(row_widget)

    def remove_attribute_row(self, row_widget):
        """Remove an attribute row"""
        if len(self.attribute_rows) > 1:  # Keep at least one row
            self.attribute_rows.remove(row_widget)
            row_widget.deleteLater()

    def get_selected_attributes(self) -> List[Dict[str, str]]:
        """Get the list of attribute names and their corresponding faker types"""
        attributes = []
        for row in self.attribute_rows:
            name_input = row.findChild(QLineEdit)
            type_combo = row.findChild(QComboBox)
            if name_input and type_combo and name_input.text().strip():
                attributes.append({
                    'name': name_input.text().strip(),
                    'type': type_combo.currentData()
                })
        return attributes
    
class FakerData:
    """Class to handle Faker data generation and functionality"""
    def __init__(self):
        self.fake = Faker()
        self.formatted_functionality = [
            {"func": self.fake.name, "type": "name", "description": "Full name"},
            {"func": self.fake.last_name, "type": "last_name", "description": "Last name only"},
            {"func": self.fake.email, "type": "email", "description": "Email address"},
            {"func": self.fake.phone_number, "type": "phone_number", "description": "Phone number"},
            {"func": self.fake.address, "type": "address", "description": "Full address"},
            {"func": self.fake.text, "type": "text", "description": "Random text"},
            {"func": self.fake.date, "type": "date", "description": "Random date"},
            {"func": self.fake.time, "type": "time", "description": "Random time"},
            {"func": self.fake.url, "type": "url", "description": "Website URL"},
            {"func": self.fake.job, "type": "job", "description": "Job title"},
            {"func": self.fake.company, "type": "company", "description": "Company name"},
            {"func": self.fake.country, "type": "country", "description": "Country name"},
            {"func": self.fake.currency_code, "type": "currency_code", "description": "Currency code"},
            {"func": self.fake.file_name, "type": "file_name", "description": "Random file name"},
            {"func": self.fake.image_url, "type": "image_url", "description": "Image URL"},
            {"func": self.fake.ipv4, "type": "ipv4", "description": "IPv4 address"},
            {"func": self.fake.user_name, "type": "user_name", "description": "Username"},
            {"func": self.fake.color_name, "type": "color_name", "description": "Color name"},
            {"func": self.fake.ssn, "type": "ssn", "description": "Social Security Number"},
            {"func": self.fake.boolean, "type": "boolean", "description": "True/False"},
            {"func": self.fake.credit_card_number, "type": "credit_card_number", "description": "Credit card number"},
            {"func": self.fake.date_of_birth, "type": "date_of_birth", "description": "Date of birth"},
            {"func": self.fake.file_extension, "type": "file_extension", "description": "File extension"},
            {"func": self.fake.hex_color, "type": "hex_color", "description": "Hex color code"},
            {"func": self.fake.isbn10, "type": "isbn10", "description": "ISBN-10"},
            {"func": self.fake.isbn13, "type": "isbn13", "description": "ISBN-13"},
            {"func": self.fake.language_code, "type": "language_code", "description": "Language code"},
            {"func": self.fake.mac_address, "type": "mac_address", "description": "MAC address"},
            {"func": self.fake.mime_type, "type": "mime_type", "description": "MIME type"},
            {"func": self.fake.password, "type": "password", "description": "Random password"},
            {"func": self.fake.random_digit, "type": "random_digit", "description": "Random digit (0-9)"},
            {"func": self.fake.random_letter, "type": "random_letter", "description": "Random letter (a-z)"},
            {"func": self.fake.street_address, "type": "street_address", "description": "Street address"},
            {"func": self.fake.word, "type": "word", "description": "Random word"},
            {"func": self.fake.zipcode, "type": "zipcode", "description": "Zip code"},
            {"func": self.fake.latitude, "type": "latitude", "description": "Latitude coordinate"},
            {"func": self.fake.longitude, "type": "longitude", "description": "Longitude coordinate"},
        ]
        

    def generate_fake_data(self, selected_choices: List[str], number_of_items: int) -> List[Dict[str, Any]]:
            """Generate fake data based on selected choices"""
            if not selected_choices:
                raise ValueError("At least one data type must be selected")
                
            available_types = {func["type"] for func in self.formatted_functionality}
            invalid_types = set(selected_choices) - available_types
            if invalid_types:
                raise ValueError(f"Invalid data type(s): {', '.join(invalid_types)}")
                
            try:
                fake_data = []
                for _ in range(number_of_items):
                    data = {}
                    for type_name in selected_choices:
                        func = next(f["func"] for f in self.formatted_functionality 
                                if f["type"] == type_name)
                        data[type_name] = func()
                    fake_data.append(data)
                return fake_data
            except Exception as e:
                logging.error(f"Error generating fake data: {str(e)}")
                raise

class FileHandler:
    """Class to handle file operations"""
    @staticmethod
    def write_csv(file_name: str, header: List[str], data: List[Dict[str, Any]]) -> None:
        """Write data to CSV file"""
        try:
            output_path = Path(file_name).with_suffix('.csv')
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Successfully wrote CSV file: {output_path}")
        except Exception as e:
            logging.error(f"Error writing CSV file: {str(e)}")
            raise

    @staticmethod
    def write_json(file_name: str, data: List[Dict[str, Any]]) -> None:
        """Write data to JSON file"""
        try:
            output_path = Path(file_name).with_suffix('.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Successfully wrote JSON file: {output_path}")
        except Exception as e:
            logging.error(f"Error writing JSON file: {str(e)}")
            raise

class CheckboxGroup(QFrame):
    """Custom widget to group checkboxes with search and custom name functionality"""
    def __init__(self, items: List[Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.items = items
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search data types...")
        self.search_box.textChanged.connect(self.filter_items)
        layout.addWidget(self.search_box)

        # Create scrollable area for items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        item_widget = QWidget()
        self.item_layout = QVBoxLayout(item_widget)
        
        # Create checkbox and name input for each item
        self.item_widgets = []
        for item in self.items:
            # Create container for each item
            item_container = QWidget()
            container_layout = QHBoxLayout(item_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add checkbox
            checkbox = QCheckBox(f"{item['type']} - {item['description']}")
            checkbox.setObjectName(f"checkbox_{item['type']}")
            container_layout.addWidget(checkbox)
            
            # Add name input field
            name_input = QLineEdit()
            name_input.setPlaceholderText("Custom name...")
            name_input.setObjectName(f"name_{item['type']}")
            name_input.setFixedWidth(150)
            container_layout.addWidget(name_input)
            
            self.item_layout.addWidget(item_container)
            self.item_widgets.append({
                'container': item_container,
                'checkbox': checkbox,
                'name_input': name_input,
                'type': item['type']
            })
        
        scroll.setWidget(item_widget)
        layout.addWidget(scroll)

    def filter_items(self, text: str):
        """Filter items based on search text"""
        for item in self.item_widgets:
            item['container'].setVisible(text.lower() in item['checkbox'].text().lower())

    def get_selected_items(self) -> List[Dict[str, str]]:
        """Get selected items with their custom names"""
        selected_items = []
        for item in self.item_widgets:
            if item['checkbox'].isChecked():
                custom_name = item['name_input'].text().strip()
                selected_items.append({
                    'type': item['type'],
                    'name': custom_name if custom_name else item['type']
                })
        return selected_items
    
class DataTypeSelector(QFrame):
    """Custom widget to select and add data types"""
    def __init__(self, items: List[Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.items = items
        self.selected_types = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add type selection group
        selection_layout = QHBoxLayout()
        
        # Dropdown for data types
        self.type_combo = QComboBox()
        for item in self.items:
            self.type_combo.addItem(f"{item['type']} - {item['description']}", item['type'])
        selection_layout.addWidget(self.type_combo)
        
        # Add button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_type)
        selection_layout.addWidget(add_button)
        
        layout.addLayout(selection_layout)
        
        # List of selected types
        self.selected_list = QListWidget()
        layout.addWidget(self.selected_list)
        
        # Remove button
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_selected)
        layout.addWidget(remove_button)

    def add_type(self):
        """Add selected type to the list"""
        current_type = self.type_combo.currentData()
        current_text = self.type_combo.currentText()
        
        # Check if type is already in the list
        existing_items = [self.selected_list.item(i).data(Qt.UserRole) 
                         for i in range(self.selected_list.count())]
        
        if current_type not in existing_items:
            item = QtWidgets.QListWidgetItem(current_text)
            item.setData(Qt.UserRole, current_type)
            self.selected_list.addItem(item)

    def remove_selected(self):
        """Remove selected items from the list"""
        for item in self.selected_list.selectedItems():
            self.selected_list.takeItem(self.selected_list.row(item))

    def get_selected_types(self) -> List[str]:
        """Get list of selected type identifiers"""
        return [self.selected_list.item(i).data(Qt.UserRole) 
                for i in range(self.selected_list.count())]
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.faker_data = FakerData()
        self.file_handler = FileHandler()
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        self.setWindowTitle("Faker GUI")
        self.setGeometry(100, 100, 1000, 700)
        self.center_on_screen()

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left side - Attribute input group
        self.attribute_group = AttributeInputGroup(self.faker_data.formatted_functionality)
        main_layout.addWidget(self.attribute_group)

        # Right side - Controls
        control_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Data Generator")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(title_label)

        # File name input
        file_layout = self.create_input_group("File Name:", "file_input", "[A-Za-z0-9_]+")
        control_layout.addLayout(file_layout)

        # Number of records input
        number_layout = self.create_input_group("Number of Records:", "number_input", "\\d+")
        control_layout.addLayout(number_layout)

        # File format selection
        format_layout = QHBoxLayout()
        self.csv_radio = QRadioButton("CSV")
        self.json_radio = QRadioButton("JSON")
        format_layout.addWidget(self.csv_radio)
        format_layout.addWidget(self.json_radio)
        control_layout.addLayout(format_layout)

        # Generate button
        generate_button = QPushButton("Generate Data")
        generate_button.clicked.connect(self.generate_data)
        control_layout.addWidget(generate_button)

        main_layout.addLayout(control_layout)
        self.setCentralWidget(main_widget)

    def create_input_group(self, label_text: str, input_name: str, regex_pattern: str = None) -> QHBoxLayout:
        """Create a labeled input group with optional regex validation"""
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setObjectName(input_name)
        input_field.setFixedSize(200, 40)
        
        # Add regex validator if pattern is provided
        if regex_pattern:
            validator = QRegExpValidator(QRegExp(regex_pattern))
            input_field.setValidator(validator)
        
        layout.addWidget(label)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        layout.addWidget(input_field)
        return layout

    def setup_styles(self):
        """Set up the application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel#title_label {
                font-size: 32pt;
                font-weight: bold;
                color: #2c3e50;
                margin: 20px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QRadioButton {
                font-size: 14px;
                padding: 5px;
            }
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

    def generate_data(self):
        """Generate and save the fake data"""
        try:
            # Validate inputs
            file_name = self.findChild(QLineEdit, "file_input").text()
            number_str = self.findChild(QLineEdit, "number_input").text()
            
            if not all([file_name, number_str, any([self.csv_radio.isChecked(), self.json_radio.isChecked()])]):
                raise ValueError("Please fill in all fields")

            number = int(number_str)
            if number <= 0:
                raise ValueError("Number of records must be greater than 0")

            # Get selected attributes
            attributes = self.attribute_group.get_selected_attributes()
            if not attributes:
                raise ValueError("Please add at least one attribute")

            # Generate fake data
            fake_data = []
            for _ in range(number):
                record = {}
                for attr in attributes:
                    faker_func = next(f["func"] for f in self.faker_data.formatted_functionality 
                                   if f["type"] == attr["type"])
                    record[attr["name"]] = faker_func()
                fake_data.append(record)

            # Save data
            if self.csv_radio.isChecked():
                self.file_handler.write_csv(file_name, [attr["name"] for attr in attributes], fake_data)
            else:
                self.file_handler.write_json(file_name, fake_data)

            QMessageBox.information(self, "Success", f"Generated {number} records successfully!")

        except Exception as e:
            logging.error(f"Error in generate_data: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))


    def center_on_screen(self):
        """Center the window on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        
def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Faker GUI")
        app_icon = QIcon('./images/logo.png')
        app.setWindowIcon(app_icon)
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        logging.critical(f"Application failed to start: {str(e)}")
        raise

if __name__ == "__main__":
    main()