# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from builtins import range

from local_search.routedata import RouteData

C_EPS = 1e-10
S_EPS = 1e-10
class LSOPT:
    FIRST_ACCEPT = 1
    BEST_ACCEPT = 2
ROUTE_ORDER_SENSITIVE_OPERATORS = set()

def do_1point_move(route1_data, route2_data, D, d=None,
                      C=None,
                      strategy=LSOPT.FIRST_ACCEPT,
                      best_delta = None):

    if route1_data==route2_data:
        return None,None,None

    route1, r1_l, r1_d = route1_data
    route2, r2_l, r2_d = route2_data
    
    if not best_delta:
        best_delta = 0
    best_move = None
    accept_move = False# 根据策略选择是否接受解
    
    for i in range(1,len(route1)-1):
        remove_after = route1[i-1]
        to_move = route1[i]
        remove_before = route1[i+1]
        
        remove_delta = D[remove_after,remove_before]\
                      -D[remove_after,to_move]\
                      -D[to_move,remove_before] # 第一条路径删除某个点后的路径长度变化量
        
        # 检查第二条路径插入某点是否到达能力上限
        if C and r2_d+d[to_move]-C_EPS>C:
            continue
        # 未到达能力上限，检查第二条路径中每个位置
        for j in range(1,len(route2)): # 在哪个位置之前加路径点
            insert_after = route2[j-1]
            insert_before = route2[j]
            
            
            insert_delta = D[insert_after,to_move]+D[to_move,insert_before]\
                          -D[insert_after,insert_before]
            
            delta = remove_delta+insert_delta
            if delta+S_EPS<best_delta: # 如果找到了一个好的改进方法                 
                best_delta = delta
                best_move = (i, j, remove_delta, insert_delta)
                if strategy==LSOPT.FIRST_ACCEPT:
                    accept_move=True
                    # break j-loop
                    break
        # break i-loop
        if accept_move:
            break
        
    if best_move:
        i, j, remove_delta, insert_delta = best_move
        to_move = route1[i] 
        return (RouteData(route1[:i]+route1[i+1:], r1_l+remove_delta,
                 None if not C else r1_d-d[to_move]),
                RouteData(route2[:j]+[to_move]+route2[j:], r2_l+insert_delta,
                 None if not C else r2_d+d[to_move]),
                remove_delta+insert_delta)
                
    return None,None,None

# 两条路径交换节点
def do_2point_move(route1_data, route2_data, D, d=None,
                   C=None,
                   strategy=LSOPT.FIRST_ACCEPT,
                   best_delta = None):                 
    
    # 路径列表，当前cost，当前运输量
    route1, r1_l, r1_d = route1_data
    route2, r2_l, r2_d = route2_data
    
    if not best_delta:
        best_delta = 0
    best_move = None # 记录(i, j, route1_delta, route2_delta)
    accept_move = False
    
    for i in range(1,len(route1)-1):
        to_swap1 = route1[i]

        swap1_after = route1[i-1]
        swap1_before = route1[i+1]     


        for j in range(1,len(route2)-1):
            to_swap2 = route2[j]
            

            if C and (r1_d-d[to_swap1]+d[to_swap2]-C_EPS>C or
                      r2_d-d[to_swap2]+d[to_swap1]-C_EPS>C):
                continue
            
            swap2_after = route2[j-1]
            swap2_before = route2[j+1]    
            
            route1_delta = -D[swap1_after,to_swap1]\
                           -D[to_swap1,swap1_before]\
                           +D[swap1_after,to_swap2]\
                           +D[to_swap2,swap1_before]
            route2_delta = -D[swap2_after,to_swap2]\
                           -D[to_swap2,swap2_before]\
                           +D[swap2_after,to_swap1]\
                           +D[to_swap1,swap2_before]
                        
            delta = route1_delta+route2_delta
            if delta+S_EPS<best_delta:                    
                best_delta = delta
                best_move = (i, j, route1_delta, route2_delta)
                if strategy==LSOPT.FIRST_ACCEPT:
                    accept_move=True
                    break # j loop
        if accept_move:
            break # i loop
        
    if best_move:
        i, j, route1_delta, route2_delta = best_move
        to_swap1 = route1[i] 
        to_swap2 = route2[j] 
        return (RouteData(route1[:i]+[to_swap2]+route1[i+1:],
                 r1_l+route1_delta,
                 None if not C else r1_d-d[to_swap1]+d[to_swap2]),
                RouteData(route2[:j]+[to_swap1]+route2[j+1:],
                 r2_l+route2_delta,
                 None if not C else r2_d-d[to_swap2]+d[to_swap1]),
                          
                route1_delta+route2_delta)
                
    return None,None,None
        
