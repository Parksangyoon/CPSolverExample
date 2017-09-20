from __future__ import print_function
from ortools.constraint_solver import pywrapcp


def cp_solver():
    # Creates the solver.
    solver = pywrapcp.Solver("simple_example")
    # Creates the variables.
    num_vals = 20
    x = solver.IntVar(0, num_vals - 1, "x")
    y = solver.IntVar(0, num_vals - 1, "y")
    z = solver.IntVar(0, num_vals - 1, "z")
    # Create the constraints.

    # ex 1
    # solver.Add(x + 2*y <= 14)
    # solver.Add(3*x - y >= 0)
    # solver.Add(x - y <= 2)

    # ex 2
    solver.Add(x <= 5)
    solver.Add(x >= -5)
    solver.Add(y <= 5)
    solver.Add(y >= -5)

    # Create the decision builder.
    db = solver.Phase([x, y, z], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    solver.Solve(db)
    count = 0

    while solver.NextSolution():
        count += 1
        print("So3lution", count, '\n')
        print("x = ", x.Value())
        print("y = ", y.Value())
        print("z = ", z.Value())
        print()
        print("Number of solutions:", count)
