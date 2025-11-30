import random
from PyQt5.QtWidgets import (
    QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout,
    QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsPixmapItem
)
from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap
from PyQt5.QtCore import Qt


class TopologyWindow(QWidget):
    def __init__(self, users, aps, assignments, intermediates):
        super().__init__()
        self.setWindowTitle("Network Topology")
        self.showMaximized()

        layout = QVBoxLayout(self)
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        layout.addWidget(self.view)

        self.draw_topology(users, aps, assignments, intermediates)

    def random_color(self):
        """Generate a random pastel-like color for grouping."""
        return QColor(random.randint(80, 200), random.randint(80, 200), random.randint(80, 200))

    def draw_topology(self, users, aps, assignments, intermediates):
        s = 100  # scale factor: 1 unit = 100 px
        user_dict = {u["Name"]: u for u in users}

        # Get real coverage radius from intermediates
        D_max = intermediates.get("D_max", 30)
        ap_radius_px = D_max * s

        # Load icons
        ap_icon = QPixmap(r"C:\Bureau\Documenten\RT3\Info\Recherche operationnelle\project\ro-matching\screenshots\image-removebg-preview.png")
        user_icon = QPixmap(r"C:\Bureau\Documenten\RT3\Info\Recherche operationnelle\project\ro-matching\screenshots\Copilot_20251127_214136-removebg-preview.png")

        # Scale icons bigger
        ap_icon = ap_icon.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        user_icon = user_icon.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Assign a random color per AP
        ap_colors = {ap["Name"]: self.random_color() for ap in aps}

        # Draw APs
        for ap in aps:
            name = ap["Name"]
            x, y = ap["X"] * s, ap["Y"] * s

            # Coverage circle
            circle = QGraphicsEllipseItem(x - ap_radius_px, y - ap_radius_px,
                                          2 * ap_radius_px, 2 * ap_radius_px)
            circle.setBrush(QBrush(QColor(225, 190, 231, 40)))  # semi-transparent
            circle.setPen(QPen(QColor("#6a1b9a"), 2))
            self.scene.addItem(circle)

            # AP square
            square_size = 60
            rect = QGraphicsRectItem(x - square_size/2, y - square_size/2, square_size, square_size)
            rect.setBrush(QBrush(ap_colors[name]))
            rect.setPen(QPen(Qt.black, 2))
            self.scene.addItem(rect)

            # AP icon
            ap_item = QGraphicsPixmapItem(ap_icon)
            ap_item.setPos(x - ap_icon.width()/2, y - ap_icon.height()/2)
            self.scene.addItem(ap_item)

            # AP name above
            name_text = QGraphicsTextItem(name)
            name_text.setDefaultTextColor(Qt.black)
            name_text.setPos(x - square_size/2, y - square_size/2 - 20)
            self.scene.addItem(name_text)

            # Channel below
            channel_text = QGraphicsTextItem(f"Ch {ap['Channel']}")
            channel_text.setDefaultTextColor(Qt.black)
            channel_text.setPos(x - square_size/2, y + square_size/2 + 5)
            self.scene.addItem(channel_text)

        # Draw users
        for user in users:
            uname = user["Name"]
            x, y = user["X"] * s, user["Y"] * s

            # Check if assigned
            assigned_ap = None
            for ap_name, user_list in assignments.items():
                if uname in user_list:
                    assigned_ap = ap_name
                    break

            if assigned_ap:
                # User square with AP color
                square_size = 40
                rect = QGraphicsRectItem(x - square_size/2, y - square_size/2, square_size, square_size)
                rect.setBrush(QBrush(ap_colors[assigned_ap]))
                rect.setPen(QPen(Qt.black, 1))
                self.scene.addItem(rect)

            # User icon
            user_item = QGraphicsPixmapItem(user_icon)
            user_item.setPos(x - user_icon.width()/2, y - user_icon.height()/2)
            self.scene.addItem(user_item)

            # User label above (name)
            label = QGraphicsTextItem(uname)
            label.setDefaultTextColor(Qt.black)
            label.setPos(x - user_icon.width()/2, y - user_icon.height()/2 - 20)
            self.scene.addItem(label)

            # Priority label below
            priority_text = QGraphicsTextItem(user.get("Priority", ""))
            priority_text.setDefaultTextColor(QColor("#424242"))
            priority_text.setPos(x - user_icon.width()/2, y + user_icon.height()/2 + 5)
            self.scene.addItem(priority_text)
