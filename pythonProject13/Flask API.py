import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit, QDialog, QFormLayout, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Определение модели базы данных
Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    description = Column(Text)
    russian_license = Column(String)
    phone_number = Column(String)
    vin = Column(String)
    status = Column(String)
    comments = Column(Text)
    full_name = Column(String)
    passport_number = Column(String)


# Создание базы данных и сессии
engine = create_engine('sqlite:///inventory.db')

# Удаление и повторное создание базы данных (для разработки)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class AddEditItemDialog(QDialog):
    def __init__(self, item=None):
        super().__init__()
        self.item = item
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Edit Item' if self.item else 'Add Item')
        self.setWindowIcon(QIcon('edit.png' if self.item else 'add.png'))
        self.setGeometry(100, 100, 400, 400)

        self.layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.layout.addRow('Item Name:', self.name_input)

        self.quantity_input = QLineEdit(self)
        self.layout.addRow('Quantity:', self.quantity_input)

        self.price_input = QLineEdit(self)
        self.layout.addRow('Price:', self.price_input)

        self.description_input = QTextEdit(self)
        self.layout.addRow('Description:', self.description_input)

        self.russian_license_input = QLineEdit(self)
        self.layout.addRow('Russian License:', self.russian_license_input)

        self.phone_number_input = QLineEdit(self)
        self.layout.addRow('Phone Number:', self.phone_number_input)

        self.vin_input = QLineEdit(self)
        self.layout.addRow('VIN:', self.vin_input)

        self.status_input = QLineEdit(self)
        self.layout.addRow('Status:', self.status_input)

        self.comments_input = QTextEdit(self)
        self.layout.addRow('Comments:', self.comments_input)

        self.full_name_input = QLineEdit(self)
        self.layout.addRow('Full Name:', self.full_name_input)

        self.passport_number_input = QLineEdit(self)
        self.layout.addRow('Passport Number:', self.passport_number_input)

        self.save_button = QPushButton('Save Item', self)
        self.save_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.save_button.clicked.connect(self.save_item)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        if self.item:
            self.load_item_data()

    def load_item_data(self):
        self.name_input.setText(self.item.name)
        self.quantity_input.setText(str(self.item.quantity))
        self.price_input.setText(str(self.item.price))
        self.description_input.setText(self.item.description)
        self.russian_license_input.setText(self.item.russian_license)
        self.phone_number_input.setText(self.item.phone_number)
        self.vin_input.setText(self.item.vin)
        self.status_input.setText(self.item.status)
        self.comments_input.setText(self.item.comments)
        self.full_name_input.setText(self.item.full_name)
        self.passport_number_input.setText(self.item.passport_number)

    def save_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        description = self.description_input.toPlainText()
        russian_license = self.russian_license_input.text()
        phone_number = self.phone_number_input.text()
        vin = self.vin_input.text()
        status = self.status_input.text()
        comments = self.comments_input.toPlainText()
        full_name = self.full_name_input.text()
        passport_number = self.passport_number_input.text()

        if not name or not quantity or not price:
            QMessageBox.warning(self, 'Error', 'Name, Quantity, and Price fields are required')
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Quantity must be an integer and Price must be a float')
            return

        if self.item:
            self.item.name = name
            self.item.quantity = quantity
            self.item.price = price
            self.item.description = description
            self.item.russian_license = russian_license
            self.item.phone_number = phone_number
            self.item.vin = vin
            self.item.status = status
            self.item.comments = comments
            self.item.full_name = full_name
            self.item.passport_number = passport_number
        else:
            new_item = Item(
                name=name,
                quantity=quantity,
                price=price,
                description=description,
                russian_license=russian_license,
                phone_number=phone_number,
                vin=vin,
                status=status,
                comments=comments,
                full_name=full_name,
                passport_number=passport_number
            )
            session.add(new_item)

        session.commit()

        self.accept()


class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Inventory Management System')
        self.setWindowIcon(QIcon('inventory.png'))
        self.setGeometry(100, 100, 1200, 800)

        self.layout = QVBoxLayout()

        self.title_label = QLabel('Inventory Management System')
        self.title_label.setFont(QFont('Arial', 20))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.add_button = QPushButton('Add Item', self)
        self.add_button.setIcon(QIcon('add.png'))
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; height: 40px;")
        self.add_button.clicked.connect(self.open_add_item_dialog)
        self.layout.addWidget(self.add_button)

        self.table = QTableWidget(self)
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Quantity', 'Price', 'Description', 'Russian License', 'Phone Number', 'VIN', 'Status',
             'Comments', 'Full Name', 'Passport Number', 'Edit'])
        self.table.setStyleSheet("QTableWidget {font-size: 14px;}")
        self.layout.addWidget(self.table)

        self.update_table()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_add_item_dialog(self):
        dialog = AddEditItemDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

    def open_edit_item_dialog(self, item):
        dialog = AddEditItemDialog(item)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

    def update_table(self):
        items = session.query(Item).all()
        self.table.setRowCount(len(items))

        for i, item in enumerate(items):
            self.table.setItem(i, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(i, 1, QTableWidgetItem(item.name))
            self.table.setItem(i, 2, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(i, 3, QTableWidgetItem(str(item.price)))
            self.table.setItem(i, 4, QTableWidgetItem(item.description))
            self.table.setItem(i, 5, QTableWidgetItem(item.russian_license))
            self.table.setItem(i, 6, QTableWidgetItem(item.phone_number))
            self.table.setItem(i, 7, QTableWidgetItem(item.vin))
            self.table.setItem(i, 8, QTableWidgetItem(item.status))
            self.table.setItem(i, 9, QTableWidgetItem(item.comments))
            self.table.setItem(i, 10, QTableWidgetItem(item.full_name))
            self.table.setItem(i, 11, QTableWidgetItem(item.passport_number))

            edit_button = QPushButton('Edit')
            edit_button.setStyleSheet("background-color: #FFA500; color: white;")
            edit_button.clicked.connect(lambda _, item=item: self.open_edit_item_dialog(item))
            self.table.setCellWidget(i, 12, edit_button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InventoryApp()
    ex.show()
    sys.exit(app.exec_())
