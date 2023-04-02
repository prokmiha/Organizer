import re
import sqlite3

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, QTextEdit


class AddAccountDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add account")
        self.email_line_edit = QLineEdit()
        self.wallet_line_edit = QLineEdit()
        self.twitter_line_edit = QLineEdit()
        self.discord_line_edit = QLineEdit()
        self.extra_info_text_edit = QTextEdit()  # создаем экземпляр QTextEdit
        self.create_button = QPushButton("Create")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_line_edit)
        layout.addWidget(QLabel("Wallet:"))
        layout.addWidget(self.wallet_line_edit)
        layout.addWidget(QLabel("Twitter:"))
        layout.addWidget(self.twitter_line_edit)
        layout.addWidget(QLabel("Discord:"))
        layout.addWidget(self.discord_line_edit)
        layout.addWidget(QLabel("Extra info:"))
        layout.addWidget(self.extra_info_text_edit)
        layout.addWidget(self.create_button)

        self.twitter_line_edit.setPlaceholderText("Twitter: starts with '@' and contains at least 4 characters")
        self.discord_line_edit.setPlaceholderText(
            "Discord: starts with letters and contains '#' followed by at least 2 letters/numbers")
        self.setLayout(layout)
        self.create_button.clicked.connect(self.save_account_to_db)
        self.resize(430, 400)
        self.center()
        extra_info_pos_y = 320
        if self.discord_line_edit.isVisible():
            extra_info_pos_y += 50
        self.extra_info_text_edit.setGeometry(20, extra_info_pos_y, 390, 50)
        print("AddAccountDialog.__init__()")

    def center(self):
        screen_geometry = QDesktopWidget().availableGeometry()

        dialog_geometry = self.geometry()

        center_point = screen_geometry.center()

        dialog_geometry.moveCenter(center_point)
        self.move(dialog_geometry.topLeft())

    def save_account_to_db(self):
        print(1)
        email = self.email_line_edit.text()
        print(2)
        wallet = self.wallet_line_edit.text()
        print(3)
        twitter = self.twitter_line_edit.text()
        print(4)
        discord = self.discord_line_edit.text()
        print(5)
        extra_info = self.extra_info_text_edit.toPlainText()
        print(6)
        print("AddAccountDialog.accept()")
        if not self.is_valid_email(email):
            QMessageBox.warning(self,
                                "Error",
                                "Type valid Email address")
            return

        # Check conditions for Twitter field
        if len(twitter) == 0:
            pass
        elif twitter.startswith("@") and len(twitter) >= 4:
            # Save Twitter account
            pass
        else:
            QMessageBox.warning(self, "Error", "Twitter account should start with '@' and contain at least 4 characters")
            return

        # Check conditions for Discord field
        if len(discord) == 0:
            pass
        elif discord[:discord.find('#')].isalpha() and "#" in discord:
            index = discord.index("#")
            if len(discord[index+1:]) >= 2:
                # Save Discord account
                pass
            else:
                QMessageBox.warning(self, "Error", "Discord account should contain '#' followed by at least 2 letters/numbers")
                return
        else:
            QMessageBox.warning(self, "Error", "Discord account should start with letters and contain '#' followed by at least 2 letters/numbers")
            return

        try:
            # TODO: save data to DB
            pass
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save account to the database: {e}")
            return

        connection = sqlite3.connect('../DB/database.db')
        cursor = connection.cursor()
        print("AddAccountDialog.closeEvent(1)")
        # Проверка на отсутствие аналогичного email в базе данных
        query = "SELECT email FROM accounts WHERE email = ?"
        result = cursor.execute(query, (email,))
        try:
            if result.fetchone():
                QMessageBox.warning(self, "Error", "Account with this email already exists")
                return
            connection.close()
        except:
            pass
        self.accept()
        QMessageBox.information(self, "Success", "Account has been saved to the database.")

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        print("AddAccountDialog.closeEvent(2)")
        return re.match(pattern, email) is not None


    def reject(self):
        super().reject()
        print("AddAccountDialog.closeEvent(3)")
