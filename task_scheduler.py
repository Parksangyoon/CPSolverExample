from __future__ import print_function
from ortools.constraint_solver import pywrapcp

WEEK = ["월요일", "화요일", "수요일", "목요일", "금요일"]


def task_scheduler():
    # Create the solver.
    solver = pywrapcp.Solver('job_shop')
    # Define data.
    # 요일
    week = [[0, 1, 2],
            [0, 2, 1],
            [1, 2],
            [0, 1],
            ]

    # 시간
    processing_times = [[3, 2, 2],
                        [2, 1, 4],
                        [4, 3],
                        [3, 3],
                        ]

    jobs_count = processing_times.__len__()
    all_jobs = range(0, jobs_count)

    week_count = 3
    all_week = range(0, week_count)

    # Computes horizon.
    horizon = 0
    for i in all_week:
        horizon += sum(processing_times[i])
    # Creates jobs.
    all_tasks = {}
    for i in all_jobs:
        for j in range(0, len(week[i])):
            all_tasks[(i, j)] = solver.FixedDurationIntervalVar(0, horizon, processing_times[i][j], False,
                                                                '(Subject_%i_%i) ' % (i, j))

    # Creates sequence variables and add disjunctive constraints.
    all_sequences = []
    # all_week_jobs = []
    for i in all_week:
        week_jobs = []
        for j in all_jobs:
            for k in range(0, len(week[j])):
                if week[j][k] == i:
                    week_jobs.append(all_tasks[(j, k)])
        disj = solver.DisjunctiveConstraint(week_jobs, 'week %i' % i)
        all_sequences.append(disj.SequenceVar())
        solver.Add(disj)

    # Add conjunctive constraints.
    for i in all_jobs:
        for j in range(0, len(week[i]) - 1):
            solver.Add(all_tasks[(i, j + 1)].StartsAfterEnd(all_tasks[(i, j)]))

    # Set the objective.
    obj_var = solver.Max([all_tasks[(i, len(week[i])-1)].EndExpr() for i in all_jobs])
    objective_monitor = solver.Minimize(obj_var, 1)
    # Create search phases.
    sequence_phase = solver.Phase([all_sequences[i] for i in all_week], solver.SEQUENCE_DEFAULT)
    vars_phase = solver.Phase([obj_var], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    main_phase = solver.Compose([sequence_phase, vars_phase])
    # Create the solution collector.
    collector = solver.LastSolutionCollector()

    # Add the interesting variables to the SolutionCollector.
    collector.Add(all_sequences)
    collector.AddObjective(obj_var)

    for i in all_week:
        sequence = all_sequences[i]
        sequence_count = sequence.Size()
        for j in range(0, sequence_count):
            t = sequence.Interval(j)
            collector.Add(t.StartExpr().Var())
            collector.Add(t.EndExpr().Var())
    # Solve the problem.
    disp_col_width = 10

    if solver.Solve(main_phase, [objective_monitor, collector]):
        print("\nOptimal Schedule Length:", collector.ObjectiveValue(0), "\n")
        sol_line = ""
        sol_line_tasks = ""
        print("Optimal Schedule", "\n")

        for i in all_week:
            seq = all_sequences[i]
            sol_line += WEEK[i] + ": "
            sol_line_tasks += WEEK[i] + ": "
            sequence = collector.ForwardSequence(0, seq)
            seq_size = len(sequence)
            for j in range(0, seq_size):
                t = seq.Interval(sequence[j])
                # Add spaces to output to align columns.
                sol_line_tasks += t.Name() + " " * (disp_col_width - len(t.Name()))

            for j in range(0, seq_size):
                t = seq.Interval(sequence[j])
                sol_tmp = "[" + str(collector.Value(0, t.StartExpr().Var())) + ","
                sol_tmp += str(collector.Value(0, t.EndExpr().Var())) + "] "
                # Add spaces to output to align columns.
                sol_line += sol_tmp + " " * (disp_col_width - len(sol_tmp))

            sol_line += "\n"
            sol_line_tasks += "\n"

        print(sol_line_tasks)
        print("Time Intervals for Tasks\n")
        print(sol_line)
