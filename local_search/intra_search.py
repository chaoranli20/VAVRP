# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from builtins import range

C_EPS = 1e-10
S_EPS = 1e-10
class LSOPT:
    FIRST_ACCEPT = 1
    BEST_ACCEPT = 2
ROUTE_ORDER_SENSITIVE_OPERATORS = set()

def do_2opt_move(route, D, strategy=LSOPT.FIRST_ACCEPT, best_delta=None):
    rN = len(route)
    best_move = None
    if not best_delta:
        best_delta = 0
    accept_move = False
    for i in range(0,rN-1):
        for j in range(i+1,rN-1):
            a = route[i]
            b = route[i+1]
            c = route[j]
            d = route[j+1]

            delta = D[a,c] + D[b,d] \
                     -D[a,b]-D[c,d]
                     
            if delta+S_EPS<best_delta:
                best_move = (i,j)
                best_delta = delta
                if strategy==LSOPT.FIRST_ACCEPT:
                    accept_move = True
                    break # j loop
        if accept_move:
            break # i loop
                
    if best_move:
        i,j = best_move
        return route[:i+1]+route[j:i:-1]+route[j+1:], best_delta
    return None, None

# 查看一个节点是否能移到这条路径的其他地方  
def do_relocate_move(route, D, strategy=LSOPT.FIRST_ACCEPT, best_delta=None):
    rN = len(route)
    best_move = None
    if not best_delta:
        best_delta = 0
    accept_move = False
    for i in range(1,rN-1):
        for j in range(1,rN):
            if i==j or j==i-1:
                continue
            
            a = route[i-1]
            b = route[i]
            c = route[i+1]
            
            d = route[j-1]
            e = route[j]
            
            if d==b or e==b:
                continue
            
            delta = -D[a,b]-D[b,c]+D[a,c]\
                     -D[d,e]+D[d,b]+D[b,e]
                                          
            if delta+S_EPS<best_delta:
                best_move = (i,j)
                best_delta = delta
                if strategy==LSOPT.FIRST_ACCEPT:
                    accept_move = True
                    break # j loop                
        if accept_move:
            break # i loop
                
    if best_move:
        i,j = best_move
        if i<j:
            return route[:i]+route[i+1:j]+[route[i]]+route[j:], best_delta
        else:
            return route[:j]+[route[i]]+route[j:i]+route[i+1:], best_delta
            
    return None, None

# 查看一条路径上的两个节点能否交换
def do_exchange_move(route, D, strategy=LSOPT.FIRST_ACCEPT, best_delta=None):
    rN = len(route)
    best_move = None
    if not best_delta:
        best_delta = 0
    accept_move = False
    for i in range(1,rN-1):
        for j in range(i+1,rN-1):
            if i==j:
                continue
            a = route[i-1]
            b = route[i]
            c = route[i+1]
            
            d = route[j-1]
            e = route[j]
            f = route[j+1]
            
            if c==e:
                delta = -D[a,b]-D[b,e]-D[e,f]\
                         +D[a,e]+D[e,b]+D[b,f]
            else:
                delta = -D[a,b]-D[b,c]+D[a,e]+D[e,c]\
                         -D[d,e]-D[e,f]+D[d,b]+D[b,f]

            if delta+S_EPS<best_delta:
                best_move = (i,j)
                best_delta = delta
                
                if strategy==LSOPT.FIRST_ACCEPT:
                    accept_move = True
                    break # j loop
        if accept_move:
            break # i loop
                
    if best_move:
        i,j = best_move
        return route[:i]+[route[j]]+route[i+1:j]+[route[i]]+route[j+1:], best_delta
    return None, None
