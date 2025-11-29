# output_ui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from calculations_ui import CalculationsWindow
from calculations import compute_intermediates


class OutputWindow(QWidget):
    def __init__(self, users, aps, settings, assignments):
        super().__init__()
        self.users = users
        self.aps = aps
        self.settings = settings
        self.assignments = assignments

        self.setWindowTitle("Optimization Result")
        self.setFixedSize(700, 500)

        layout = QVBoxLayout(self)


        # === Styled Table ===
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Access Point", "Assigned Users"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        # Fancy stylesheet
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f3e5f5;
                border: 2px solid #7e57c2;
                border-radius: 12px;
                font-family: Roboto;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1565c0, stop:1 #ab47bc);
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
            QTableWidget::item {
                padding: 6px;
            }
        """)

        # Populate table
        self.table.setRowCount(len(assignments))
        for row, (ap, users) in enumerate(assignments.items()):
            ap_item = QTableWidgetItem(ap)
            ap_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, ap_item)

            users_item = QTableWidgetItem(", ".join(users))
            users_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, users_item)

        layout.addWidget(self.table)

        # === Buttons ===
        button_layout = QHBoxLayout()

        self.intermediate_btn = QPushButton("Show Intermediate Calculations")
        self.intermediate_btn.setStyleSheet(self.button_style())
        self.intermediate_btn.clicked.connect(self.show_intermediates)

        self.topology_btn = QPushButton("Show Topology")
        self.topology_btn.setStyleSheet(self.button_style())

        button_layout.addWidget(self.intermediate_btn)
        button_layout.addWidget(self.topology_btn)

        layout.addLayout(button_layout)

    def button_style(self):
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1565c0, stop:1 #ab47bc);
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 14px;
            }
            QPushButton:hover { background-color: #6a1b9a; }
        """

    def show_intermediates(self):
        try:
            intermediates = compute_intermediates(self.users, self.aps, self.settings)
            self.calculations_window = CalculationsWindow(intermediates)
            self.calculations_window.show()
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Intermediate calculation failed:\n{e}")

