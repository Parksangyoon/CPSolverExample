from __future__ import print_function
from ortools.constraint_solver import pywrapcp


def n_queens(n):
    # Creates the solver.
    solver = pywrapcp.Solver("n-queens")
    # Creates the variables.
    # The array index is the column, and the value is the row.
    queens = [solver.IntVar(0, n - 1, "x%i" % i) for i in range(n)]
    # Creates the constraints.

    # All rows must be different.
    solver.Add(solver.AllDifferent(queens))

    # All columns must be different because the indices of queens are all different.

    # No two queens can be on the same diagonal.
    solver.Add(solver.AllDifferent([queens[i] + i for i in range(n)]))
    solver.Add(solver.AllDifferent([queens[i] - i for i in range(n)]))

    db = solver.Phase(queens,
                      solver.CHOOSE_FIRST_UNBOUND,
                      solver.ASSIGN_MIN_VALUE)
    solver.NewSearch(db)

    return [queens, solver]


def print_n_queens(queens, solver, n):
    # Iterates through the solutions, displaying each.
    num_solutions = 0

    while solver.NextSolution():
        # Displays the solution just computed.
        board = ""
        for i in range(n): board += " _"
        board += "\n"
        for i in range(n):
            board += "|"
            for j in range(n):
                if queens[j].Value() == i:
                    # There is a queen in column j, row i.
                    board += "Q|"
                    # print("Q", end="|")
                else:
                    board += "_|"
                    # print("_", end="|")
            board += "\n"
        print(board)
        num_solutions += 1

    solver.EndSearch()

    print()
    print("Solutions found:", num_solutions)
    print("Time:", solver.WallTime(), "ms")
