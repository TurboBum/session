from PyQt5.QtWidgets import QDialog, QDateEdit, QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton, QGroupBox, QFormLayout, QMessageBox


class RegistrationDialog(QDialog):
    def __init__(self):
        super(RegistrationDialog, self).__init__()

        self.setWindowTitle("Регистрация пациента")

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.first_name_edit = QLineEdit()
        form_layout.addRow(QLabel("Имя:"), self.first_name_edit)

        self.last_name_edit = QLineEdit()
        form_layout.addRow(QLabel("Фамилия:"), self.last_name_edit)

        self.middle_name_edit = QLineEdit()
        form_layout.addRow(QLabel("Отчество:"), self.middle_name_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        form_layout.addRow(QLabel("Дата рождения:"), self.date_edit)

        self.contact_info_edit = QLineEdit()
        form_layout.addRow(QLabel("Контактная информация:"), self.contact_info_edit)

        self.medical_history_edit = QLineEdit()
        form_layout.addRow(QLabel("Медицинская история:"), self.medical_history_edit)

        layout.addLayout(form_layout)

        confirm_button = QPushButton("Подтвердить")
        confirm_button.clicked.connect(self.confirm_registration)
        layout.addWidget(confirm_button)

    def confirm_registration(self):
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        middle_name = self.middle_name_edit.text()
        date_of_birth = self.date_edit.date().toString("dd.MM.yyyy")
        contact_info = self.contact_info_edit.text()
        medical_history = self.medical_history_edit.text()

        # TODO: Сохранить информацию пациента в базе данных

        QMessageBox.information(self, "Регистрация пациента", f"Пациент {last_name} {first_name} {middle_name} успешно зарегистрирован!")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Расписание приема пациентов")
        self.resize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Создаем форму для фильтра расписания
        filter_group_box = QGroupBox("Фильтры")
        filter_form_layout = QFormLayout()
        filter_group_box.setLayout(filter_form_layout)
        layout.addWidget(filter_group_box)

        filter_form_layout.addRow(QLabel("Период:"), QComboBox())
        filter_form_layout.addRow(QLabel("Направление специалистов:"), QComboBox())
        filter_form_layout.addRow(QLabel("Фамилия врача:"), QLineEdit())

        # Создаем календарь для выбора даты
        calendar = QCalendarWidget()
        layout.addWidget(calendar)

        # Создаем таблицу для отображения расписания
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Врач", "Дата", "Время", "Событие"])
        layout.addWidget(table)

        # Создаем кнопку для сохранения расписания
        save_button = QPushButton("Сохранить")
        layout.addWidget(save_button)

        # Добавляем разделение прав доступа
        user_role = "Регистратура"  # Устанавливаем роль пользователя

        if user_role == "Администратор":
            add_patient_button = QPushButton("Добавить пациента")
            layout.addWidget(add_patient_button)

            issue_referral_button = QPushButton("Выдать направление")
            issue_referral_button.clicked.connect(self.issue_referral)
            layout.addWidget(issue_referral_button)

            manage_documents_button = QPushButton("Управление документами")
            manage_documents_button.clicked.connect(self.manage_documents)
            layout.addWidget(manage_documents_button)

        elif user_role == "Регистратура":
            add_patient_button = QPushButton("Добавить пациента")
            add_patient_button.clicked.connect(self.add_patient)
            layout.addWidget(add_patient_button)

            issue_referral_button = QPushButton("Выдать направление")
            issue_referral_button.clicked.connect(self.issue_referral)
            layout.addWidget(issue_referral_button)

            manage_documents_button = QPushButton("Управление документами")
            manage_documents_button.clicked.connect(self.manage_documents)
            layout.addWidget(manage_documents_button)

    def add_patient(self):
        # Действия при нажатии кнопки "Добавить пациента"
        dialog = RegistrationDialog()
        dialog.exec_()


    def issue_referral(self):
        # Действия при нажатии кнопки "Выдать направление"
        QMessageBox.information(self, "Выдать направление", "Функция выдачи направления")

    def manage_documents(self):
        # Действия при нажатии кнопки "Управление документами"
        QMessageBox.information(self, "Управление документами", "Функция управления документами")


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
