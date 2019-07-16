import libration_points_calculator

for points_count in [1000, 10000, 100000]:
    for eps in [1e-5, 1e-7, 1e-9]:
        print('---------------------------------------')
        libration_points_calculator.calculate_data_dicts(libration_points_calculator.CalcTypes.NEWTON,
                                                         points_count, eps, time_logging=True, extended_graphs=True)
        print('---------------------------------------')
        libration_points_calculator.calculate_data_dicts(libration_points_calculator.CalcTypes.DICHOTOMY,
                                                         points_count, eps, time_logging=True, extended_graphs=True)
