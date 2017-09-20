from __future__ import print_function
from ortools.linear_solver import pywraplp


def linear_optimization(constraint_list, objective_data):
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver('LinearExample', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create the two variables and let them take on any value.
    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

    # constraint format should be ax + by <= c
    for constraint_data in constraint_list:
        constraint = solver.Constraint(-solver.infinity(), constraint_data.get("c"))
        constraint.SetCoefficient(x, constraint_data.get("a"))
        constraint.SetCoefficient(y, constraint_data.get("b"))

    # Objective format should be ax + by.
    objective = solver.Objective()
    objective.SetCoefficient(x, objective_data.get("a"))
    objective.SetCoefficient(y, objective_data.get("b"))
    objective.SetMaximization()

    # Solve the system.
    solver.Solve()
    opt_solution = 3 * x.solution_value() + 4 * y.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)
