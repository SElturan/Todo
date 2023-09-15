import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QLabel, QInputDialog
from PyQt5.QtCore import Qt

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
      
        self.init_db()

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 10, 50, 10)

        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #3498db;
            }
            QListWidget {
                border: 2px solid #3498db;
                border-radius: 5px;
            }
            QListWidgetItem {
                padding: 5px;
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 15px;
                qproperty-alignment: 'AlignCenter';
            }
        """)

        headerLabel = QLabel("Daily Tasks", self)
        self.userInput = QLineEdit(self)
        self.userInput.setPlaceholderText("Add todo")
        self.userList = QListWidget(self)
        self.load_users_from_db()

        self.addButton = QPushButton("Add", self)
        self.addButton.clicked.connect(self.add_user)
        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.clicked.connect(self.delete_user)
        self.editButton = QPushButton("Edit", self)  # Кнопка редактирования
        self.editButton.clicked.connect(self.edit_user)

        layout.addWidget(headerLabel)
        layout.addWidget(self.userInput)
        layout.addWidget(self.userList)
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.editButton)

        self.setLayout(layout)
        self.setWindowTitle("Todo App")
        self.resize(700, 500)

    def init_db(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """)

    def load_users_from_db(self):
        self.cursor.execute("SELECT name FROM users")
        users = self.cursor.fetchall()
        for user in users:
            self.userList.addItem(user[0])

    def add_user(self):
        user = self.userInput.text()
        if user:
            self.cursor.execute("INSERT INTO users (name) VALUES (?)", (user,))
            self.conn.commit()
            self.userList.addItem(user)
            self.userInput.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, напишите значение в поле Add todo")

    def delete_user(self):
        current_item = self.userList.currentItem()
        if current_item:
            user = current_item.text()
            self.cursor.execute("DELETE FROM users WHERE name=?", (user,))
            self.conn.commit()
            row = self.userList.row(current_item)
            self.userList.takeItem(row)
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите элемент для удаления.")

    def edit_user(self):
        current_item = self.userList.currentItem()
        if current_item:
            user = current_item.text()
            edited_user, ok = QInputDialog.getText(self, 'Edit user', 'New name:', text=user)
            if ok and edited_user:
                self.cursor.execute("UPDATE users SET name=? WHERE name=?", (edited_user, user))
                self.conn.commit()
                current_item.setText(edited_user)
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите элемент для редактирования.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.add_user()
        elif event.key() == Qt.Key_Delete:
            self.delete_user()
        elif event.key() == Qt.Key_F2:
            self.edit_user()    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
