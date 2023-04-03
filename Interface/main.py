import os
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QDesktopWidget, QWidget, \
    QVBoxLayout, QMessageBox
from add_acc_widget import AddAccountDialog
from profile_edit_widget import ProfileWindow
from DB.create_dp import create_db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        desktop = QDesktopWidget().screenGeometry()
        width = int(desktop.width() * 0.7)
        height = int(desktop.height() * 0.7)
        self.resize(width, height)
        self.setWindowTitle("Account Manager")

        if not os.path.isfile('../DB/database.db'):
            create_db()

        self.add_account_button = QPushButton("Add account", self)
        self.add_account_button.setGeometry(25, 25, 100, 50)
        self.add_account_button.clicked.connect(self.show_add_account_dialog)

        self.edit_profile_button = QPushButton('Edit Profiles', self)
        self.edit_profile_button.setGeometry(self.add_account_button.x() +
                                             self.add_account_button.width() + 20, 25, 100, 50)
        self.edit_profile_button.clicked.connect(self.show_profile_window)
        conn = sqlite3.connect('../DB/database.db')

    def show_add_account_dialog(self):
        try:
            dialog = AddAccountDialog(self)
            if dialog.exec() == QDialog.Accepted:
                email = dialog .email_line_edit.text()
                wallet_address = dialog.wallet_address_line_edit.text()  # использование правильного имени переменной
                twitter = dialog.twitter_line_edit.text()
                discord = dialog.discord_line_edit.text()
                extra_info = dialog .extra_info_text_edit.toPlainText()
                self.save_to_db(email,
                                wallet_address,
                                twitter,
                                discord,
                                extra_info)  # использование правильного имени метода
            else:
                print('Error')
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save account to the database: {e}")

    def save_to_db(self, email, wallet_address, twitter, discord, extra_info):
        print(1)
        try:
            print(2)
            connection = sqlite3.connect('../DB/database.db')
            cursor = connection.cursor()

            query = "INSERT INTO accounts (email, wallet_address, twitter, discord, extra_info) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (email, wallet_address, twitter, discord, extra_info))

            connection.commit()
            connection.close()
            print("Account has been saved to the database.")
            return True

        except Exception as e:
            print(f"Failed to save account to the database: {e}")
            return False

    def show_profile_window(self):
        profile_window = ProfileWindow()
        if profile_window.exec_() == QDialog.Accepted:
            # обработка данных, введенных пользователем в окне Edit Profile
            pass
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
