import os
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QDesktopWidget, QWidget, \
    QVBoxLayout
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

        self.add_account_button = QPushButton("Add account", self)
        self.add_account_button.setGeometry(25, 25, 100, 50)
        self.add_account_button.clicked.connect(self.show_add_account_dialog)

        self.edit_profile_button = QPushButton('Edit Profiles', self)
        self.edit_profile_button.setGeometry(self.add_account_button.x() +
                                             self.add_account_button.width() + 20, 25, 100, 50)
        self.edit_profile_button.clicked.connect(self.show_profile_window)

        if not os.path.isfile('../DB/database.db'):
            create_db()

        conn = sqlite3.connect('../DB/database.db')

    def show_add_account_dialog(self):
        dialog = AddAccountDialog()
        if dialog.exec_() == QDialog.Accepted:
            email = dialog.email_line_edit.text()
            wallet_address = dialog.wallet_line_edit.text()  # использование правильного имени переменной
            twitter = dialog.twitter_line_edit.text()
            discord = dialog.discord_line_edit.text()
            self.save_to_db(email, wallet_address, twitter, discord)  # использование правильного имени метода
        else:
            pass

    def save_to_db(self, email, wallet_address, twitter, discord):
        conn = sqlite3.connect('../DB/database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO accounts (email, wallet_address, twitter, discord) VALUES (?, ?, ?, ?)",
                           (email, wallet_address, twitter, discord))
            conn.commit()
            print("Data inserted successfully!")
        except Exception as e:
            print("Error while inserting data:", e)
            conn.rollback()
        finally:
            conn.close()

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
