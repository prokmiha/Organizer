import re
import sqlite3

from PyQt5.QtWidgets import QPushButton, QMessageBox

from Interface.add_acc_widget import AddAccountDialog


class EditAccountDialog(AddAccountDialog):
    def __init__(self, account_id):
        super().__init__()
        self.setWindowTitle("Edit account")
        self.account_id = account_id
        self.load_account_data()
        # self.create_button.setText("Save")
        # delete_button = QPushButton("Delete")
        # delete_button.clicked.connect(self.delete_account)
        # layout = self.layout()
        # layout.addWidget(delete_button)

    # def load_account_data(self):
    #     connection = sqlite3.connect('../DB/database.db')
    #     cursor = connection.cursor()
    #
    #     # Get account data from DB
    #     query = "SELECT email, wallet, twitter, discord FROM accounts WHERE id = ?"
    #     result = cursor.execute(query, (self.account_id,))
    #     account_data = result.fetchone()
    #
    #     self.email_line_edit.setText(account_data[0])
    #     self.wallet_line_edit.setText(account_data[1])
    #     self.twitter_line_edit.setText(account_data[2])
    #     self.discord_line_edit.setText(account_data[3])
    #
    #     connection.close()
    #
    # def delete_account(self):
    #     connection = sqlite3.connect('../DB/database.db')
    #     cursor = connection.cursor()
    #
    #     # Delete account from DB
    #     query = "DELETE FROM accounts WHERE id = ?"
    #     cursor.execute(query, (self.account_id,))
    #
    #     connection.commit()
    #     connection.close()
    #
    #     self.accept()
    #     QMessageBox.information(self, "Success", "Account has been deleted.")
    #
    # def save_account_to_db(self):
    #     email = self.email_line_edit.text()
    #     wallet = self.wallet_line_edit.text()
    #     twitter = self.twitter_line_edit.text()
    #     discord = self.discord_line_edit.text()
    #
    #     if not self.is_valid_email(email):
    #         QMessageBox.warning(self, "Error", "Type valid Email address")
    #         return
    #
    #     # Check conditions for Twitter field
    #     if len(twitter) == 0:
    #         pass
    #     elif twitter.startswith("@") and len(twitter) >= 4:
    #         # Save Twitter account
    #         pass
    #     else:
    #         QMessageBox.warning(self, "Error",
    #                             "Twitter account should start with '@' and contain at least 4 characters")
    #         return
    #
    #     # Check conditions for Discord field
    #     if len(discord) == 0:
    #         pass
    #     elif discord[:discord.find('#')].isalpha() and "#" in discord:
    #         index = discord.index("#")
    #         if len(discord[index + 1:]) >= 2:
    #             # Save Discord account
    #             pass
    #         else:
    #             QMessageBox.warning(self, "Error",
    #                                 "Discord account should contain '#' followed by at least 2 letters/numbers")
    #             return
    #     else:
    #         QMessageBox.warning(self, "Error",
    #                             "Discord account should start with letters and contain '#' followed by at least 2 letters/numbers")
    #         return
    #
    #     connection = sqlite3.connect('../DB/database.db')
    #     cursor = connection.cursor()
    #
    #     # Check if an account with the same email already exists
    #     query = "SELECT id FROM accounts WHERE email = ?"
    #     result = cursor.execute(query, (email,))
    #     existing_account = result.fetchone()
    #
    #     if existing_account is not None and existing_account[0] != self.account_id:
    #         QMessageBox.warning(self, "Error", "Account with this email already exists")
    #         return
    #
    #     # Update account in DB
    #     query = "UPDATE accounts SET email = ?, wallet = ?, twitter =?, discord = ? WHERE id = ?"
    #     cursor.execute(query, (email, wallet, twitter, discord, self.account_id))
    #
    #     connection.commit()
    #     connection.close()
    #
    #     self.accept()
    #     QMessageBox.information(self, "Success", "Account has been saved to the database.")
    #
    # def is_valid_email(self, email):
    #     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #     return re.match(pattern, email) is not None

    def reject(self):
        super().reject()
