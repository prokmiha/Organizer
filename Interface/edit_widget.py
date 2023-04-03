import re
import sqlite3

from PyQt5.QtWidgets import QPushButton, QMessageBox

from Interface.add_acc_widget import AddAccountDialog


class EditAccountDialog(AddAccountDialog):
    def __init__(self, account_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit account")
        self.account_id = account_id
        self.load_account_data()
        self.create_button.setText("Save")
        # self.create_button.clicked.connect(self.save_account_to_db)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_account)
        layout = self.layout()
        layout.addWidget(delete_button)
        print(account_id)

    def load_account_data(self):
        connection = sqlite3.connect('../DB/database.db')
        cursor = connection.cursor()

        # Get account data from DB
        query = "SELECT email, wallet_address, twitter, discord, extra_info FROM accounts WHERE id = ?"
        result = cursor.execute(query, (self.account_id,))
        account_data = result.fetchone()

        self.email_line_edit.setText(account_data[0])
        self.wallet_address_line_edit.setText(account_data[1])
        self.twitter_line_edit.setText(account_data[2])
        self.discord_line_edit.setText(account_data[3])
        self.extra_info_text_edit.setText(account_data[4])

        connection.close()

    def delete_account(self):
        connection = sqlite3.connect('../DB/database.db')
        cursor = connection.cursor()

        # Delete account from DB
        query = "DELETE FROM accounts WHERE id = ?"
        cursor.execute(query, (self.account_id,))

        connection.commit()
        connection.close()

        self.accept()
        QMessageBox.information(self, "Success", "Account has been deleted.")

    def save_account_to_db(self):
        email = self.email_line_edit.text()
        wallet = self.wallet_address_line_edit.text()
        twitter = self.twitter_line_edit.text()
        discord = self.discord_line_edit.text()
        extra_info = self.extra_info_text_edit.toPlainText()
        print(email, wallet, twitter, discord, extra_info, sep='\n')

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Error", "Type valid Email address")
            return

        connection = sqlite3.connect('../DB/database.db')
        cursor = connection.cursor()

        # Check if an account with the same email already exists

        query = "SELECT id FROM accounts WHERE email = ?"
        result = cursor.execute(query, (email,))
        existing_account = result.fetchone()

        if existing_account is not None and existing_account[0] != self.account_id:
            QMessageBox.warning(self, "Error", "Account with this email already exists")
            return

        # Update account in DB
        query = "UPDATE accounts SET email=?, wallet_address=?, twitter=?, discord=?, extra_info=? WHERE id=?"
        cursor.execute(query,
                       (email, wallet or None, twitter or None, discord or None, extra_info or None, self.account_id))

        connection.commit()
        connection.close()

        self.accept()
        QMessageBox.information(self, "Success", "Account has been saved to the database.")

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def reject(self):
        super().reject()
