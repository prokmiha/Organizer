# Вікно, після натискання Edit Profile

import sqlite3
from functools import partial

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from edit_widget import EditAccountDialog

class ProfileWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Profiles')
        self.resize(500, 300)
        self.layout = QVBoxLayout(self)
        self.profiles_widget = QWidget()
        self.profiles_layout = QVBoxLayout(self.profiles_widget)
        self.layout.addWidget(self.profiles_widget)

        conn = sqlite3.connect('../DB/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, wallet_address FROM accounts")
        rows = cursor.fetchall()
        for row in rows:
            profile = QHBoxLayout()
            profile.addWidget(QLabel(row[1], self.profiles_widget), 1)
            profile.addWidget(QLabel(row[2], self.profiles_widget), 1)
            view_button = QPushButton('View', self.profiles_widget)
            edit_button = QPushButton('Edit', self.profiles_widget)
            profile.addWidget(view_button)
            profile.addWidget(edit_button)
            edit_button.clicked.connect(partial(self.edit_widget, account_id=row[0]))
            self.profiles_layout.addLayout(profile)
        conn.close()

    def edit_widget(self, account_id):
        try:
            print('Hello')
            widget = EditAccountDialog(account_id=account_id)
            print('Hello')
            if widget.exec_() == QDialog.Accepted:
                print('Not Error')
            else:
                print('Error')
        except Exception as e:
            print('Error:', e)