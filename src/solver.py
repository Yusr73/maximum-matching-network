# solver.py
from gurobipy import Model, GRB, quicksum

def solve_network(intermediates, aps_data):
    """
    Solve the AP-user assignment using Gurobi with hierarchical priorities
    and energy minimization at each level.
    """

    # Unpack intermediates
    E = intermediates["E"]
    c = intermediates["c"]
    I = intermediates["I"]
    M = intermediates["M"]
    U_H, U_M, U_L = intermediates["U_H"], intermediates["U_M"], intermediates["U_L"]

    # === Create model ===
    m = Model("AP_Assignment")
    m.setParam('OutputFlag', 0)
    m.setParam('Threads', 1)

    # Variables
    x = {(u, a): m.addVar(vtype=GRB.BINARY, name=f"x_{u}_{a}") for (u, a) in E}
    m.update()

    # === Constraints ===
    # 1. Exclusivity: each user ≤ 1 AP
    for u in set(u for u,_ in E):
        m.addConstr(quicksum(x[(u,a)] for (uu,a) in E if uu == u) <= 1)

    # 2. AP capacity
    aps = {a["Name"]: a["Capacity"] for a in aps_data}
    for a in aps:
        m.addConstr(quicksum(x[(u,a)] for (u,aa) in E if aa == a) <= aps[a])

    # 3. Interference
    for a1, a2 in I:
        m.addConstr(
            quicksum(x[(u,a1)] for (u,aa) in E if aa==a1) +
            quicksum(x[(u,a2)] for (u,aa) in E if aa==a2)
            <= M[(a1,a2)]
        )

    # === Priority-wise optimization ===
    def optimize_priority(users_set):
        if not users_set:
            return 0

        # Step 1 — maximize the number of connected users
        m.setObjective(quicksum(x[(u,a)] for (u,a) in E if u in users_set), GRB.MAXIMIZE)
        m.optimize()
        if m.status != GRB.OPTIMAL:
            return None

        Z_opt = m.ObjVal

        # Fix the count
        m.addConstr(quicksum(x[(u,a)] for (u,a) in E if u in users_set) == Z_opt)

        # Step 2 — minimize energy
        if c:
            m.setObjective(quicksum(c[(u,a)] * x[(u,a)] for (u,a) in E if u in users_set), GRB.MINIMIZE)
            m.optimize()
            if m.status != GRB.OPTIMAL:
                return None

        # === Freeze the chosen assignments (IMPORTANT) ===
        for (u,a) in E:
            if u in users_set:
                val = x[(u,a)].X
                if val is not None and val > 0.5:
                    m.addConstr(x[(u,a)] == 1)

        return Z_opt

    # High → Medium → Low
    optimize_priority(U_H)
    optimize_priority(U_M)
    optimize_priority(U_L)

    # === Extract solution ===
    assignments = {a: [] for a in aps}
    if m.status == GRB.OPTIMAL:
        for (u,a) in E:
            if x[(u,a)].X > 0.5:
                assignments[a].append(u)
        status = "Optimal"
    elif m.status == GRB.INFEASIBLE:
        assignments = {}
        status = "Infeasible"
    else:
        assignments = {}
        status = f"Solver status: {m.status}"

    return assignments, status
