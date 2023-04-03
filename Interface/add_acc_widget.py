import re
import sqlite3

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QTextEdit, QFormLayout, QMessageBox


class AddAccountDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new account")
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.save_account_to_db)
        self.email_line_edit = QLineEdit()
        self.wallet_address_line_edit = QLineEdit()
        self.twitter_line_edit = QLineEdit()
        self.discord_line_edit = QLineEdit()
        self.extra_info_text_edit = QTextEdit()
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Email"), self.email_line_edit)
        layout.addRow(QLabel("Wallet Address"), self.wallet_address_line_edit)
        layout.addRow(QLabel("Twitter"), self.twitter_line_edit)
        layout.addRow(QLabel("Discord"), self.discord_line_edit)
        layout.addRow(QLabel("Extra Info"), self.extra_info_text_edit)
        layout.addRow(self.create_button)
        self.setLayout(layout)

    def save_account_to_db(self):
        email = self.email_line_edit.text()
        wallet = self.wallet_address_line_edit.text()
        twitter = self.twitter_line_edit.text()
        discord = self.discord_line_edit.text()
        extra_info = self.extra_info_text_edit.toPlainText()

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Error", "Type valid Email address")
            return

        connection = sqlite3.connect('../DB/database.db')
        cursor = connection.cursor()

        # Check if an account with the same email already exists
        query = "SELECT id FROM accounts WHERE email = ?"
        result = cursor.execute(query, (email,))
        existing_account = result.fetchone()

        if existing_account is not None:
            QMessageBox.warning(self, "Error", "Account with this email already exists")
            return

        # Insert account into DB
        query = "INSERT INTO accounts(email, wallet_address, twitter, discord, extra_info) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (email, wallet or None, twitter or None, discord or None, extra_info or None))

        connection.commit()
        connection.close()

        self.accept()
        QMessageBox.information(self, "Success", "Account has been added to the database.")

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def reject(self):
        super().reject()
