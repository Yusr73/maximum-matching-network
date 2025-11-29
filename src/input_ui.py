import sys
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QComboBox, QCheckBox, QLineEdit, QSpinBox,
    QSizePolicy, QSpacerItem, QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QIntValidator
from PyQt5.QtCore import Qt


class NetworkGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.device_combos = []
        self.setWindowTitle("Wireless Network Optimization")
        self.setWindowState(Qt.WindowMaximized)
        self.setFont(QFont("Roboto", 11))

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(20)
        central.setLayout(layout)

        # === TOP SECTION: Tables + Icons ===
        top = QHBoxLayout()
        top.setSpacing(40)
        layout.addLayout(top)

        # === USER SECTION ===
        user_layout = QVBoxLayout()
        user_layout.setSpacing(12)

        self.user_icon = QLabel()
        self.user_icon.setFixedSize(160, 160)
        self.user_icon.setAlignment(Qt.AlignCenter)
        self.user_icon.setPixmap(
            QPixmap(r"C:/Bureau/Documenten/RT3/Info/Recherche operationnelle/project/ro-matching/screenshots/Copilot_20251127_214136-removebg-preview.png")
            .scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        user_layout.addWidget(self.user_icon, alignment=Qt.AlignCenter)
        # label above the user table
        user_label = QLabel("Users Table")
        user_label.setAlignment(Qt.AlignCenter)
        user_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #283593;
                margin-bottom: 6px;
            }
        """)
        user_layout.addWidget(user_label)

        self.user_table = QTableWidget(0, 5)
        self.user_table.setHorizontalHeaderLabels(["Name", "Priority", "X", "Y", "Device type"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: #f3e5f5;
                font-family: Roboto;
                border: 1px solid #7e57c2; 
            }
            QHeaderView::section {
                background-color: #7e57c2;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
        """)

        user_layout.addWidget(self.user_table)

        user_buttons = QHBoxLayout()
        self.add_user_btn = QPushButton("Add User")
        self.add_user_btn.setStyleSheet(self.green_button())
        self.remove_user_btn = QPushButton("Remove Last User")
        self.remove_user_btn.setStyleSheet(self.red_button())
        self.edit_user_btn = QPushButton("Save Changes")
        self.edit_user_btn.setStyleSheet(self.edit_button_style())

        user_buttons.addWidget(self.add_user_btn)
        user_buttons.addWidget(self.remove_user_btn)
        user_buttons.addWidget(self.edit_user_btn)
        user_layout.addLayout(user_buttons)

        top.addLayout(user_layout)

        # === AP SECTION ===
        ap_layout = QVBoxLayout()
        ap_layout.setSpacing(12)

        self.ap_icon = QLabel()
        self.ap_icon.setFixedSize(160, 160)
        self.ap_icon.setAlignment(Qt.AlignCenter)
        self.ap_icon.setPixmap(
            QPixmap(
                r"C:\Bureau\Documenten\RT3\Info\Recherche operationnelle\project\ro-matching\screenshots\image-removebg-preview.png")
            .scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        ap_layout.addWidget(self.ap_icon, alignment=Qt.AlignCenter)
        # Add a label above the AP table
        ap_label = QLabel("Access Points Table")
        ap_label.setAlignment(Qt.AlignCenter)
        ap_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #283593;
                margin-bottom: 6px;
            }
        """)
        ap_layout.addWidget(ap_label)

        self.ap_table = QTableWidget(0, 5)
        self.ap_table.setHorizontalHeaderLabels(["Name", "Capacity", "Channel", "X", "Y"])
        self.ap_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ap_table.verticalHeader().setVisible(False)
        self.ap_table.setStyleSheet("""
            QTableWidget {
                background-color: #e8eaf6;
                font-family: Roboto;
                border: 1px solid #5c6bc0; /* sharp edges */
            }
            QHeaderView::section {
                background-color: #5c6bc0;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
        """)
        ap_layout.addWidget(self.ap_table)

        ap_buttons = QHBoxLayout()
        self.add_ap_btn = QPushButton("Add AP")
        self.add_ap_btn.setStyleSheet(self.green_button())
        self.remove_ap_btn = QPushButton("Remove Last AP")
        self.remove_ap_btn.setStyleSheet(self.red_button())
        self.edit_ap_btn = QPushButton("Save Changes")
        self.edit_ap_btn.setStyleSheet(self.edit_button_style())

        ap_buttons.addWidget(self.add_ap_btn)
        ap_buttons.addWidget(self.remove_ap_btn)
        ap_buttons.addWidget(self.edit_ap_btn)
        ap_layout.addLayout(ap_buttons)

        top.addLayout(ap_layout)

        # === SETTINGS SECTION (inline, centered) ===
        settings = QHBoxLayout()
        settings.setSpacing(16)

        wifi_label = QLabel("WiFi Band:")
        wifi_label.setStyleSheet("QLabel { color: #283593; font-weight: 600; }")
        self.wifi_band = QComboBox()
        self.wifi_band.addItems(["2.4 GHz", "5 GHz"])
        self.wifi_band.setStyleSheet(self.dropdown_style())

        env_label = QLabel("Environment Type:")
        env_label.setStyleSheet("QLabel { color: #283593; font-weight: 600; }")
        self.env_type = QComboBox()
        self.env_type.addItems(["Indoor","Urban", "Outdoor"])
        self.env_type.setStyleSheet(self.dropdown_style())

        self.power_checkbox = QCheckBox("Include Power Consumption in Optimization")
        self.power_checkbox.setStyleSheet("""
            QCheckBox {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a5d6a7, stop:1 #66bb6a);
                color: white;
                padding: 6px 10px;
                border-radius: 14px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px; height: 18px;
                border-radius: 10px;
                border: 1px solid #2e7d32;
                background: white;
            }
            QCheckBox::indicator:checked { background: #2e7d32; }
        """)
        self.power_checkbox.stateChanged.connect(self.toggle_device_combos)
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1565c0, stop:1 #ab47bc);
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 14px;
            }
            QPushButton:hover { background-color: #6a1b9a; }
        """)

        settings.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        settings.addWidget(wifi_label)
        settings.addWidget(self.wifi_band)
        settings.addWidget(env_label)
        settings.addWidget(self.env_type)
        settings.addWidget(self.power_checkbox)
        settings.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        settings.addWidget(self.calculate_btn)
        settings.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(settings)

        # === Connections (functional buttons) ===
        self.add_user_btn.clicked.connect(self.add_user_row)
        self.remove_user_btn.clicked.connect(self.remove_user_row)
        self.edit_user_btn.clicked.connect(self.save_user_table)
        self.add_ap_btn.clicked.connect(self.add_ap_row)
        self.remove_ap_btn.clicked.connect(self.remove_ap_row)
        self.edit_ap_btn.clicked.connect(self.save_ap_table)

        # Start with editing enabled
        self.user_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.ap_table.setEditTriggers(QAbstractItemView.AllEditTriggers)

    # === Styles ===
    def edit_button_style(self):
        return """
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #7e57c2, stop:1 #42a5f5);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #5e35b1; }
        """

    def green_button(self):
        return """
           QPushButton {
               background-color: #4caf50;
               color: white;
               border: none;
               border-radius: 12px;
               padding: 8px 16px;
               font-weight: bold;
           }
           QPushButton:hover { background-color: #388e3c; }
           """

    def red_button(self):
        return """
           QPushButton {
               background-color: #f44336;
               color: white;
               border: none;
               border-radius: 12px;
               padding: 8px 16px;
               font-weight: bold;
           }
           QPushButton:hover { background-color: #d32f2f; }
           """

    def dropdown_style(self):
        return """
           QComboBox {
               background-color: #ffffff;
               border: 1px solid #90caf9;
               border-radius: 10px;
               padding: 6px 8px;
               min-width: 140px;
           }
           QComboBox QAbstractItemView {
               background-color: #ffffff;
               border: 1px solid #90caf9;
               selection-background-color: #bbdefb;
           }
           """

        # === Table logic ===
    def add_user_row(self):
        row = self.user_table.rowCount()
        self.user_table.insertRow(row)

        # Name (text box)
        name_edit = QLineEdit()
        self.user_table.setCellWidget(row, 0, name_edit)

        # Priority (dropdown)
        priority_combo = QComboBox()
        priority_combo.addItems(["Low", "Medium", "High"])
        self.user_table.setCellWidget(row, 1, priority_combo)

        # X coordinate
        x_edit = QLineEdit()
        x_edit.setValidator(QIntValidator())
        self.user_table.setCellWidget(row, 3, x_edit)

        # Y coordinate
        y_edit = QLineEdit()
        y_edit.setValidator(QIntValidator())
        self.user_table.setCellWidget(row, 4, y_edit)

        # Device type (dropdown)
        device_combo = QComboBox()
        device_combo.addItems(["IoT Sensor", "Wearable", "Smartphone", "Tablet", "Laptop"])
        device_combo.setEnabled(False)  # start disabled until energy checkbox is checked
        self.user_table.setCellWidget(row, 5, device_combo)

        # Keep reference
        self.device_combos.append(device_combo)

    def remove_user_row(self):
        row = self.user_table.rowCount()
        if row > 0:
            self.user_table.removeRow(row - 1)

    def add_ap_row(self):
        row = self.ap_table.rowCount()
        self.ap_table.insertRow(row)

        # Name (text box)
        name_edit = QLineEdit()
        self.ap_table.setCellWidget(row, 0, name_edit)

        # Capacity (stepper input)
        capacity_spin = QSpinBox()
        capacity_spin.setRange(1, 1000)  # adjust as needed
        self.ap_table.setCellWidget(row, 1, capacity_spin)

        # Channel (stepper input)
        channel_spin = QSpinBox()
        channel_spin.setRange(1, 165)  # typical WiFi channels
        self.ap_table.setCellWidget(row, 2, channel_spin)

        # Range (numeric text box)
        range_edit = QLineEdit()
        range_edit.setValidator(QIntValidator())
        self.ap_table.setCellWidget(row, 3, range_edit)

        # X coordinate (numeric text box)
        x_edit = QLineEdit()
        x_edit.setValidator(QIntValidator())
        self.ap_table.setCellWidget(row, 4, x_edit)

        # Y coordinate (numeric text box)
        y_edit = QLineEdit()
        y_edit.setValidator(QIntValidator())
        self.ap_table.setCellWidget(row, 5, y_edit)

    def remove_ap_row(self):
        row = self.ap_table.rowCount()
        if row > 0:
            self.ap_table.removeRow(row - 1)

    def toggle_device_combos(self, state):
        enabled = state == Qt.Checked
        for combo in self.device_combos:
            combo.setEnabled(enabled)

    def save_user_table(self):
        users_data = []
        for row in range(self.user_table.rowCount()):
            name = self.user_table.cellWidget(row, 0).text()
            priority = self.user_table.cellWidget(row, 1).currentText()
            mandatory = self.user_table.cellWidget(row, 2).layout().itemAt(0).widget().isChecked()
            x = self.user_table.cellWidget(row, 3).text()
            y = self.user_table.cellWidget(row, 4).text()
            device = self.user_table.cellWidget(row, 5).currentText()

            users_data.append({
                "Name": name,
                "Priority": priority,
                "Mandatory": mandatory,
                "X": int(x) if x else None,
                "Y": int(y) if y else None,
                "Device": device
            })

        QMessageBox.information(self, "Success", "User table changes saved successfully!")
        return users_data

    def save_ap_table(self):
        aps_data = []
        for row in range(self.ap_table.rowCount()):
            name = self.ap_table.cellWidget(row, 0).text()
            capacity = self.ap_table.cellWidget(row, 1).value()
            channel = self.ap_table.cellWidget(row, 2).value()
            range_val = self.ap_table.cellWidget(row, 3).text()
            x = self.ap_table.cellWidget(row, 4).text()
            y = self.ap_table.cellWidget(row, 5).text()

            aps_data.append({
                "Name": name,
                "Capacity": capacity,
                "Channel": channel,
                "Range": int(range_val) if range_val else None,
                "X": int(x) if x else None,
                "Y": int(y) if y else None
            })

        QMessageBox.information(self, "Success", "AP table changes saved successfully!")
        return aps_data

    def get_global_settings(self):
        settings = {
            "WifiBand": self.band_combo.currentText(),
            "EnvironmentType": self.env_combo.currentText(),
            "IncludePowerConsumption": self.power_checkbox.isChecked()
        }
        return settings


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkGUI()
    window.show()
    sys.exit(app.exec_())
