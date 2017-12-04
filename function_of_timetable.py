from ortools.constraint_solver import pywrapcp


def assign_to_different_time(data_list, avoid_date_list):
    solver = pywrapcp.Solver('time_scheduler')

    # 솔버 변수 선언
    sequence_data_list = list()
    for data in data_list:
        duration_var = solver.FixedDurationIntervalVar(data.get('range_from'),
                                                       data.get('range_to'),
                                                       data.get('duration'),
                                                       False,
                                                       data.get('name'))
        # 각각의 범위 값들이 특정 값을 포함하지 않도록 제약
        for avoid in avoid_date_list:
            solver.Add(duration_var.AvoidsDate(avoid))
        sequence_data_list.append(duration_var)

    # 솔버 제약조건 추가 (최대 범위 내에서 데이터들이 겹치지 않도록 효R율적으로 채우기)
    disjunctive_constraint = solver.DisjunctiveConstraint(sequence_data_list, 'duration')
    sequence_var = disjunctive_constraint.SequenceVar()
    solver.Add(disjunctive_constraint)
    obj_var = solver.Max([data.EndExpr() for data in sequence_data_list])
    objective_monitor = solver.Minimize(obj_var, 1)

    # solver 가 풀어내는것에 대한 옵션
    sequence_phase = solver.Phase([sequence_var], solver.SEQUENCE_SIMPLE)
    vars_phase = solver.Phase([obj_var], solver.CHOOSE_RANDOM, solver.ASSIGN_RANDOM_VALUE)
    main_phase = solver.Compose([sequence_phase, vars_phase])

    # 솔류션 모음
    collector = solver.AllSolutionCollector()

    # Add the interesting variables to the SolutionCollector.
    collector.Add([sequence_var])
    collector.AddObjective(obj_var)

    for j in range(0, sequence_var.Size()):
        interval = sequence_var.Interval(j)
        collector.Add(interval.StartExpr().Var())
        collector.Add(interval.EndExpr().Var())

    # Solve the problem.
    sequence = [seq for seq in range(sequence_var.Size())]
    if solver.Solve(main_phase, [objective_monitor, collector]):
        solution_num = 0
        sequence = collector.ForwardSequence(solution_num, sequence_var)
        seq_size = len(sequence)

        for j in range(0, seq_size):
            t = sequence_var.Interval(sequence[j])
            data_list[sequence[j]]['start_time'] = collector.Value(solution_num, t.StartExpr().Var())
            data_list[sequence[j]]['end_time'] = collector.Value(solution_num, t.EndExpr().Var())
    return sequence


if __name__ == "__main__":
    subject_data_list = [{'duration': 2, 'name': '-2--0-', 'range_from': 0, 'range_to': 26},
                         {'duration': 3, 'name': '-3--1-', 'range_from': 0, 'range_to': 26},
                         {'duration': 6, 'name': '-6--2-', 'range_from': 0, 'range_to': 26},
                         {'duration': 4, 'name': '-4--3-', 'range_from': 0, 'range_to': 26},
                         {'duration': 5, 'name': '-5--4-', 'range_from': 0, 'range_to': 26},
                         {'duration': 2, 'name': '-2--5-', 'range_from': 0, 'range_to': 26},
                         {'duration': 7, 'name': '-7--6-', 'range_from': 0, 'range_to': 26},
                         {'duration': 2, 'name': '-2--7-', 'range_from': 0, 'range_to': 26},
                         ]
    seq_num = assign_to_different_time(subject_data_list, [12, 13, 14])
    for i in seq_num:
        print(subject_data_list[i])
