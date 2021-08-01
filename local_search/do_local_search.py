from local_search.routedata import RouteData
from utils import is_sorted
from local_search.inter_search import do_1point_move

from collections import defaultdict
from inspect import getargspec
from itertools import permutations

C_EPS = 1e-10
S_EPS = 1e-10
class LSOPT:
    FIRST_ACCEPT = 1
    BEST_ACCEPT = 2
ROUTE_ORDER_SENSITIVE_OPERATORS = set()
ROUTE_ORDER_SENSITIVE_OPERATORS.add(do_1point_move)

def do_local_search(ls_ops, sol, D, d, C, operator_strategy, max_iterations=None):
    current_sol = sol
    route_datas = RouteData.from_solution(sol, D, d)
    route_data_idxs = list(range(len(route_datas)))

    at_lsop_optimal = defaultdict(set) # 在某种路径组合下某个操作已经最优
    customer_to_at_lsopt_optimal = defaultdict(list) # 关于每条路径，记录已经达到最优的相关路径
    
    iteration = 0
    improving_iteration = True
    while improving_iteration:
        improving_iteration = False # 某轮迭代中是否有提升   
        ls_op_idx = 0
        while ls_op_idx<len(ls_ops):
            ls_op = ls_ops[ls_op_idx]
            ls_op_args = getargspec(ls_op)[0]
            route_count = ls_op_args.index('D')
            op_order_sensitive = ls_op in ROUTE_ORDER_SENSITIVE_OPERATORS
            
            best_delta = None # 记录当前最好的变化值
            best_result = None # 记录车辆路径中哪个车辆的路径换为什么
            
            no_improving_lsop_found = set() # 某种邻域操作下没有改进余地的route集合               
            for route_indices in permutations(route_data_idxs,route_count): # 对所有的路径组合方式
                # 如果对顺序不敏感，并且route_indices不sorted
                if (not op_order_sensitive) and (not is_sorted(route_indices)):
                    continue
                # 如果没有改进余地
                if ls_op in at_lsop_optimal[route_indices]:
                    continue

                if route_count==1:
                    op_params = [route_datas[route_indices[0]].route,
                                 D, operator_strategy]
                else:
                    op_params = [route_datas[ri] for ri in route_indices]+\
                                 [D, d, C, operator_strategy]
                result = ls_op(*op_params) # 改变后的第一条路径的RouteData，改变后的第二条路径的RouteData，路径长度变化量

                delta = result[-1]
                if delta is None:
                    no_improving_lsop_found.update((route_indices,))
                else:
                    if route_count==1:
                        if best_result is None:
                            best_result = []
                            best_delta = 0
                        
                        old_rd = route_datas[route_indices[0]]
                        new_rd = RouteData(result[0],old_rd.cost+delta,old_rd.demand)
                        best_result.append( (route_indices[0], new_rd) )
                        best_delta+=delta
                    else:
                        if (best_result is None) or (delta+S_EPS<best_delta):
                            best_result = zip(route_indices, result[:-1])
                            best_delta = delta
                    
                    if operator_strategy==LSOPT.FIRST_ACCEPT:
                        break # 结束路径循环
                # 所有路径组合循环结束
                        
            # 做记录，防止多次对某对路径进行邻域操作
            for ris in no_improving_lsop_found:
                at_lsop_optimal[ris].add(ls_op)
                for ri in ris:
                    customer_to_at_lsopt_optimal[ri].append(ris)

            if best_result is not None:    
                improving_iteration = True
                for ri, new_rd in best_result:
                    route_datas[ri] = new_rd
                    # 路径已被修改，允许邻域操作重新对路径进行检查
                    for ris in customer_to_at_lsopt_optimal[ri]:
                        at_lsop_optimal[ris].clear()
                        
                    # 检查路径是否为空
                    if len(new_rd.route)<=2:
                        route_data_idxs.remove(ri)
    
            ls_op_idx += 1    
            # 邻域操作循环
        
        iteration+=1
        if max_iterations and iteration>=max_iterations:
            break # 迭代循环

    current_sol = RouteData.to_solution(route_datas)
    return current_sol