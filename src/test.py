# test.py
from PyQt5.QtWidgets import QApplication
import sys

from calculations import compute_intermediates
from solver import solve_network
from output_ui import OutputWindow

users = [
    {"Name": "U1", "Priority": "High", "X": 0, "Y": 0, "Device": "Laptop"},
    {"Name": "U2", "Priority": "High", "X": 1, "Y": 1, "Device": "Smartphone"},
    {"Name": "U3", "Priority": "Medium", "X": 2, "Y": 0, "Device": "Tablet"},
    {"Name": "U4", "Priority": "Medium", "X": 3, "Y": 1, "Device": "Wearable"},
    {"Name": "U5", "Priority": "Medium", "X": 4, "Y": 0, "Device": "Smartphone"},
    {"Name": "U6", "Priority": "Low", "X": 5, "Y": 1, "Device": "IoT Sensor"},
    {"Name": "U7", "Priority": "Low", "X": 6, "Y": 0, "Device": "Laptop"},
    {"Name": "U8", "Priority": "Low", "X": 7, "Y": 1, "Device": "Tablet"},
    {"Name": "U9", "Priority": "Low", "X": 8, "Y": 0, "Device": "Smartphone"},
]

aps = [
    {"Name": "AP1", "Capacity": 3, "Channel": 1, "X": 0, "Y": 1},
    {"Name": "AP2", "Capacity": 2, "Channel": 1, "X": 3, "Y": 0},
    {"Name": "AP3", "Capacity": 3, "Channel": 2, "X": 6, "Y": 1},
    {"Name": "AP4", "Capacity": 2, "Channel": 3, "X": 8, "Y": 0},
]

settings = {
    "WifiBand": "2.4 GHz",
    "EnvironmentType": "Indoor",
    "IncludePowerConsumption": True
}



# === Run pipeline ===
intermediates = compute_intermediates(users, aps, settings)
assignments, status = solve_network(intermediates, aps)

# === Prepare messages for the output window ===
messages = [
    f"Solver status: {status}",
    f"High priority satisfied: {len([u for a in assignments.values() for u in a if u in intermediates['U_H']])}/{len(intermediates['U_H'])}",
    f"Medium priority satisfied: {len([u for a in assignments.values() for u in a if u in intermediates['U_M']])}/{len(intermediates['U_M'])}",
    f"Low priority satisfied: {len([u for a in assignments.values() for u in a if u in intermediates['U_L']])}/{len(intermediates['U_L'])}"
]

# === Launch GUI to display results ===
app = QApplication(sys.argv)
window = OutputWindow(users, aps, settings, assignments, messages=messages)
window.show()
sys.exit(app.exec_())
