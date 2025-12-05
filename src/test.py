# test.py
from PyQt5.QtWidgets import QApplication
import sys

from calculations import compute_intermediates
from solver import solve_network
from output_ui import OutputWindow

users = [
    {"Name": "U1", "Priority": "High", "X": 1, "Y": 9, "Device": "Laptop"},
    {"Name": "U2", "Priority": "Medium", "X": 2, "Y": 2, "Device": "Smartphone"},
    {"Name": "U3", "Priority": "Low", "X": 3, "Y": 7, "Device": "Tablet"},

    {"Name": "U4", "Priority": "High", "X": 5, "Y": 1, "Device": "Laptop"},
    {"Name": "U5", "Priority": "Medium", "X": 5, "Y": 8, "Device": "Wearable"},
    {"Name": "U6", "Priority": "Low", "X": 6, "Y": 3, "Device": "Smartphone"},

    {"Name": "U7", "Priority": "High", "X": 8, "Y": 6, "Device": "Tablet"},
    {"Name": "U8", "Priority": "Medium", "X": 8, "Y": 2, "Device": "Laptop"},
    {"Name": "U9", "Priority": "Low", "X": 9, "Y": 8, "Device": "IoT Sensor"},

    {"Name": "U10", "Priority": "Medium", "X": 4, "Y": 5, "Device": "Smartphone"}
]

aps = [
    {"Name": "AP1", "Capacity": 3, "Channel": 1,  "X": 2,  "Y": 9},
    {"Name": "AP2", "Capacity": 3, "Channel": 1,  "X": 5,  "Y": 4},
    {"Name": "AP3", "Capacity": 2, "Channel": 6,  "X": 7,  "Y": 1},
    {"Name": "AP4", "Capacity": 3, "Channel": 11, "X": 9,  "Y": 7}
]
settings = {
    "WifiBand": "2.4 GHz",
    "EnvironmentType": "Indoor",
    "IncludePowerConsumption": False
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
