# Wireless Network Optimization Application

This project provides a graphical tool for modeling, solving, and visualizing wireless network optimization problems. The application supports integer and mixed linear programming formulations, enabling optimization of user-to-Access Point (AP) assignments based on priorities, capacities, and optionally energy consumption.

---

## Table of Contents

- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Interface Screenshots](#interface-screenshots)  
- [Project Structure](#project-structure)  

---

## Features

- **User and AP management**: Add, remove, and edit users and APs through intuitive tables.  
- **Global settings**: Configure WiFi band, environment type, and optional energy-aware optimization.  
- **Solver integration**: Optimizations solved using Gurobi via a threaded interface for non-blocking execution.  
- **Visualization**:  
  - Network topology with zoomable graphics  
  - AP coverage areas and interference  
  - User-to-AP assignments with priority and energy information  
- **Intermediate calculations**: Display distance, energy, and interference matrices for analysis.  
- **Predefined test cases**: Load and test scenarios quickly with JSON input files.

---

## Installation

1. **Clone the repository**
   
   git clone https://github.com/yourusername/wireless-network-optimization.git
   cd wireless-network-optimization
   
Install dependencies
pip install -r requirements.txt
Requirements include:

PyQt5

Gurobi Python API

Setup Gurobi license
Follow Gurobi installation instructions for your OS. Ensure the license is active.

Usage
Launch the application:
python main.py
Input users and APs
Use the tables to add new users and APs with coordinates, capacity, channel, and priority.

Set global options
Select WiFi band, environment type, and whether to include energy optimization.

Run solver
Click Calculate to assign users to APs. The optimization runs in a separate thread to keep the interface responsive.

View results

Summary table: Users assigned per AP, capacities used, average priority.

Intermediate calculations: Distances, energy costs, interference matrices.

Topology view: Zoomable map of network coverage and assignments.

Predefined examples
Load scenarios from the test_cases folder and quickly visualize results.

Interface Screenshots
<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/ed8b3f56-2f01-4f1d-8443-c7512bfd2071" />
<img width="705" height="539" alt="image" src="https://github.com/user-attachments/assets/2efb6538-9dc1-414e-a90c-2d336690ba4b" />
<img width="1919" height="1010" alt="image" src="https://github.com/user-attachments/assets/8b802ed7-f3e1-4732-85ae-7f72886d59e4" />
<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/decab091-fc7f-4476-8608-c76354733ab1" />
<img width="698" height="540" alt="image" src="https://github.com/user-attachments/assets/26c27814-5b57-471c-8613-45a61f65f4dc" />

Project Structure
.
├── main.py                  # Main GUI entry point
├── input_ui.py              # Input interface (users, APs, settings)
├── output_ui.py             # Results window
├── calculations_ui.py       # Intermediate calculations window
├── topology_ui.py           # Network topology visualization
├── predefinedExamples_ui.py # Predefined test cases window
├── solver_thread.py         # QThread wrapper for solver
├── solver.py                # Network optimization logic
├── calculations.py          # Preprocessing & intermediate computations
├── test_cases/              # JSON test cases
├── screenshots/             # Example screenshots for README
└── README.md                # Project documentation
This README provides installation instructions, usage details, and visual reference for all main features of the application.









