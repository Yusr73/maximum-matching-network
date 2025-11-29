# main.py
import sys
from PyQt5.QtWidgets import QApplication
from input_ui import NetworkGUI
from solver import solve_network
from calculations import compute_intermediates
from output_ui import OutputWindow


def main():
    app = QApplication(sys.argv)
    window = NetworkGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
