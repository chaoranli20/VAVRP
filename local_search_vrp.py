from heuristics_init.nearest_neighbor import nearest_neighbor_init
from utils import read_txt, compute_distance_martix, normalize_solution, print_results, visualize_results, sol2routes, objf, totald
from local_search.inter_search import do_1point_move, do_2point_move
from local_search.intra_search import do_2opt_move, do_exchange_move, do_relocate_move
from local_search.do_local_search import do_local_search

import os
import time

class LSOPT:
    FIRST_ACCEPT = 1
    BEST_ACCEPT = 2

ls_inter_ops = [do_1point_move, do_2point_move]
ls_intra_ops = [do_2opt_move, do_exchange_move, do_relocate_move]

if __name__ == '__main__':
    path = "./data"
    for i in range(len(os.listdir(path))):

        print("*********************processing vrpnc{}.txt*********************".format(i+1))
        data_path = path + "/vrpnc{}.txt".format(i+1)
        config, location_array, demands= read_txt(data_path)
        distance_matrix = compute_distance_martix(location_array)
        print("Vehicle Capacity: %d" % config[1])

        # init
        end = time.time()
        init_solution = nearest_neighbor_init(
            D = distance_matrix, d = demands, C = config[1], initialize_routes_with="farthest")
        sol = normalize_solution(init_solution)
        print_results(sol, distance_matrix, demands, "initial")
        used_time = time.time() - end
        routes = sol2routes(sol)
        objective = objf(sol, distance_matrix)
        total_load = totald(sol, demands)
        jpg_path = "./results_init" + "/vrpnc{}.jpg".format(i+1)
        description = "初始化"
        visualize_results(demands, routes, objective, total_load, location_array, used_time, jpg_path, description)

        # inter
        sol = do_local_search(ls_inter_ops, sol,  D = distance_matrix, d = demands, C = config[1], \
            operator_strategy=LSOPT.FIRST_ACCEPT, max_iterations=None)
        sol = normalize_solution(sol)
        print_results(sol, distance_matrix, demands, "after_inter_search")
        used_time = time.time() - end
        routes = sol2routes(sol)
        objective = objf(sol, distance_matrix)
        total_load = totald(sol, demands)
        jpg_path = "./results_after_inter_search" + "/vrpnc{}.jpg".format(i+1)
        description = "路径间搜索"
        visualize_results(demands, routes, objective, total_load, location_array, used_time, jpg_path, description)

        # intra
        sol = do_local_search(ls_intra_ops, sol, D = distance_matrix, d = demands, C = config[1], \
            operator_strategy=LSOPT.FIRST_ACCEPT, max_iterations=None)
        print_results(sol, distance_matrix, demands, "after_intra_search")
        used_time = time.time() - end
        routes = sol2routes(sol)
        objective = objf(sol, distance_matrix)
        total_load = totald(sol, demands)
        jpg_path = "./results_after_intra_search" + "/vrpnc{}.jpg".format(i+1)
        description = "路径内搜索"
        visualize_results(demands, routes, objective, total_load, location_array, used_time, jpg_path, description)
