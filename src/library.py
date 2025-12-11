from input_ui import NetworkGUI

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QApplication, QSpacerItem, QSizePolicy, QGraphicsView, QGraphicsScene, QGraphicsTextItem
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer
import sys


class ORLibraryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operational Research Problems Library")
        self.showMaximized()



        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        # === Cover Photo ===
        self.cover = QLabel()
        self.cover.setAlignment(Qt.AlignCenter)
        self.cover.setStyleSheet("background: transparent; border: none;")

        cover_pixmap = QPixmap(
            r"C:\Bureau\Documenten\RT3\Info\Recherche operationnelle\project\ro-matching\screenshots\cover.png"
        )
        # scale to full screen width, fixed height
        self.cover.setPixmap(cover_pixmap.scaled(
            self.screen().size().width(), 220,
            Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        self.cover.setFixedHeight(220)
        layout.addWidget(self.cover)

        # === Sparkling Title ===
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(self.view)

        self.title_item = QGraphicsTextItem("Operational Research Problems Library")
        font = QFont("Lucida Handwriting", 36, QFont.Bold)   # handwritten style

        self.title_item.setFont(font)
        self.title_item.setDefaultTextColor(QColor("#2e7d32"))
        self.scene.addItem(self.title_item)

        rect = self.title_item.boundingRect()
        self.title_item.setPos((self.screen().size().width() - rect.width())/2, 30)

        # Animate glow
        self.colors = [
            QColor("#0d47a1"),  # deep navy blue
            QColor("#1565c0"),  # strong blue
            QColor("#1976d2"),  # medium blue
            QColor("#1e88e5"),  # lighter blue
            QColor("#2196f3"),  # bright blue
            QColor("#42a5f5"),  # soft sky blue
            QColor("#64b5f6"),  # lighter sky blue
            QColor("#90caf9"),  # pale blue

        ]
        self.color_index = 0

        # start with the first blue instead of green
        self.title_item.setDefaultTextColor(self.colors[0])

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_glow)
        self.timer.start(200)  # faster variation (200 ms)

        # === Buttons Section ===
        button_row = QHBoxLayout()
        button_row.setSpacing(50)

        labels_text = [
            "Planning of road and railway routes to be added.",
            "Assign connections without interference.",
            "Optimization of fund transfers between banks/currencies.",
            "Determine the minimal number of monitoring nodes required."
        ]

        for i in range(4):
            box = QVBoxLayout()
            box.setSpacing(30)

            icon = QLabel()
            icon_path = fr"C:\Bureau\Documenten\RT3\Info\Recherche operationnelle\project\ro-matching\screenshots\problem{i + 1}.png"
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                icon.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon.setAlignment(Qt.AlignCenter)
            icon.setStyleSheet("background: transparent; border: none;")
            box.addWidget(icon)

            btn = QPushButton(f"Problem {i + 1}")
            btn.setFixedSize(180, 55)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1976d2;
                    color: white;
                    font-weight: bold;
                    border-radius: 16px;
                    font-size: 20px;
                    font-family: Garamond;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
            """)
            box.addWidget(btn, alignment=Qt.AlignCenter)

            # --- Hook Button 2 to launch NetworkGUI ---
            if i == 1:  # second button (Problem 2)
                btn.clicked.connect(self.open_network_gui)

            label = QLabel(labels_text[i])
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            label.setFont(QFont("Garamond", 16, QFont.Normal))
            label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;                /* deep ink blue */
                    background-color: rgba(255, 255, 255, 180); /* parchment-like semi-transparent */
                    border-radius: 8px;
                    padding: 6px 10px;
                }
            """)
            box.addWidget(label)

            button_row.addLayout(box)

        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addLayout(button_row)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def animate_glow(self):
        """Cycle through close shades of blue for a gradual lightening effect."""
        self.title_item.setDefaultTextColor(self.colors[self.color_index])
        self.color_index = (self.color_index + 1) % len(self.colors)

    def open_network_gui(self):
        """Launch the NetworkGUI window when Button 2 is clicked."""
        self.network_window = NetworkGUI()  # keep reference
        self.network_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ORLibraryWindow()
    window.show()
    sys.exit(app.exec_())
