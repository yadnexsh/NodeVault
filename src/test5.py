import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QMessageBox)

class SubmitApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integer Check")
        layout = QVBoxLayout(self)

        # Input field (allows any characters)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something...")
        layout.addWidget(self.input_field)

        # Submit button
        self.btn = QPushButton("Submit")
        self.btn.clicked.connect(self.check_input)
        layout.addWidget(self.btn)

    def check_input(self):
        text = self.input_field.text()
        
        # Check if the text is an integer (handles negative numbers too)
        try:
            val = int(text)
            print(f"Success! You entered: {val}")
            QMessageBox.information(self, "Success", f"Verified: {val} is an integer.")
        except ValueError:
            # This triggers if it's a string, float, or empty
            QMessageBox.critical(self, "Error", "Invalid input! Please enter integers only.")
            self.input_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubmitApp()
    window.show()
    sys.exit(app.exec())
