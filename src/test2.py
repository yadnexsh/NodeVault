import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QMessageBox, QErrorMessage)

class ErrorDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Multiple Errors Demo")
        self.resize(300, 200)
        
        layout = QVBoxLayout()

        # Method 1: All in one main message
        btn_combined = QPushButton("Show All in One List")
        btn_combined.clicked.connect(self.show_combined_errors)
        layout.addWidget(btn_combined)

        # Method 2: Collapsible Details
        btn_detailed = QPushButton("Show with 'Details' Box")
        btn_detailed.clicked.connect(self.show_detailed_errors)
        layout.addWidget(btn_detailed)

        # Method 3: Queued Errors (shown sequentially)
        btn_queued = QPushButton("Queue 3 Separate Errors")
        btn_queued.clicked.connect(self.show_queued_errors)
        layout.addWidget(btn_queued)
        
        # We create one instance of QErrorMessage to handle queuing
        self.error_dialog = QErrorMessage(self)
        self.setLayout(layout)

    def show_combined_errors(self):
        """Joins multiple errors into a single string for one message box."""
        errors = ["Invalid Email", "Password too short", "Zip Code must be numeric"]
        error_string = "\n".join(f"• {err}" for err in errors)
        
        QMessageBox.critical(self, "Validation Errors", 
                           f"Please fix the following:\n\n{error_string}")

    def show_detailed_errors(self):
        """Uses setDetailedText to hide a long list of errors behind a button."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Process Issues")
        msg.setText("The process finished with several issues.")
        msg.setInformativeText("Click 'Show Details' to see the full error log.")
        
        log_data = "Error 404: Asset missing\nError 500: Timeout\nWarning: Low memory"
        msg.setDetailedText(log_data) #
        msg.exec()

    def show_queued_errors(self):
        """Queues messages so they pop up one by one as the user clicks OK."""
        self.error_dialog.showMessage("Error 1: Connection Lost")
        self.error_dialog.showMessage("Error 2: File Not Found")
        self.error_dialog.showMessage("Error 3: Access Denied")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorDemo()
    window.show()
    sys.exit(app.exec())
