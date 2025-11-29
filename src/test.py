# test.py
from PyQt5.QtWidgets import QApplication
import sys

from calculations import compute_intermediates
from solver import solve_network
from output_ui import OutputWindow

# === Users with varied priorities and devices ===
users = [
    {"Name": "U1", "Priority": "High", "X": 0, "Y": 0, "Device": "Laptop"},
    {"Name": "U2", "Priority": "High", "X": 1, "Y": 2, "Device": "Smartphone"},
    {"Name": "U3", "Priority": "Medium", "X": 4, "Y": 0, "Device": "Tablet"},
    {"Name": "U4", "Priority": "Medium", "X": 3, "Y": 3, "Device": "Wearable"},
    {"Name": "U5", "Priority": "Low", "X": 5, "Y": 2, "Device": "IoT Sensor"},
    {"Name": "U6", "Priority": "Low", "X": 6, "Y": 0, "Device": "Laptop"}
]

# === APs with different capacities and channels ===
aps = [
    {"Name": "AP1", "Capacity": 2, "Channel": 1, "X": 0, "Y": 1},
    {"Name": "AP2", "Capacity": 2, "Channel": 1, "X": 3, "Y": 0},
    {"Name": "AP3", "Capacity": 3, "Channel": 2, "X": 5, "Y": 1}
]

# === Global settings ===
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
