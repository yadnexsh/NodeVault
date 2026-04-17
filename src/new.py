from PySide2.QtWidgets import QPushButton, QApplication

app = QApplication([])
button = QPushButton("Click Me")

# Set a dynamic property named "urgent"
button.setProperty("urgent", True)

# Retrieve it later using .property()
is_urgent = button.property("urgent") 
print(f"Is urgent: {is_urgent}") # Output: True
