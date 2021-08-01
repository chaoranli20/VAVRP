# -*- coding: utf-8 -*-
import utils

class RouteData:
    def __init__(self, route=None, cost=0.0, demand=0.0):
        self.route = [0,0] if (route is None) else route
        self.cost = cost
        self.demand = demand
        
    def __iter__(self):
        for e in (self.route,self.cost,self.demand):
            yield e
     
    @staticmethod
    def from_solution(solution, D, d):
        routes = utils.sol2routes(solution)
        route_datas = []
        for r in routes:
            r_cost = utils.objf(r, D)
            r_demand = sum([d[node] for node in r]) if d is not None else 0
            route_datas.append( RouteData(r, r_cost, r_demand) )   
        return route_datas

    @staticmethod
    def to_solution(route_datas):
        return [0]+[n for rd in route_datas for n in rd.route[1:]]

        
        
        
        