import numpy as np
from itertools import groupby
from matplotlib import pyplot as plt

def read_txt(path):
    f = open(path, "r")
    config = list(map(int, f.readline().split()))
    data_list = []
    for line in f:
        data_list.append(list(map(int, line.split())))
    f.close()
    data_list[0].append(0)
    location_array = np.array(data_list)[:, 0:2]
    demands = np.array(data_list)[:, 2]
    return config, location_array, demands

def compute_distance_martix(location_array):
    num_joints = location_array.shape[0]
    distance_matrix = np.zeros((num_joints, num_joints), dtype=np.int)
    for i in range(num_joints):
        for j in range(i):
            distance_matrix[i][j] = round(np.linalg.norm(location_array[i] - location_array[j]))
    distance_matrix += distance_matrix.T
    return distance_matrix

def visualize_results(demands, routes, total_distance, total_load, location_array, used_time, jpg_path, description):
    num_routes = len(routes)
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    plt.scatter(x=location_array[:, 0], y=location_array[:, 1], s=demands, c='r')
    #plt.title('{}, 总距离: {}, 总负载: {}, 路径数: {}, 时间: {:.2f}s'.format(description, total_distance, total_load, num_routes, used_time), fontsize=10)
    for i in range(len(routes)):
        plt.plot(location_array[routes[i], 0], location_array[routes[i], 1])
    #plt.axis('off')
    plt.xticks(c='w')
    plt.yticks(c='w')
    plt.savefig(jpg_path)
    plt.cla()


def routes2sol(routes):
    if not routes:
        return None
    
    sol = [0]
    for r in routes:
        if r:
            if r[0]==0:
                sol += r[1:]
            else:
                sol += r
            if sol[-1]!=0:
                sol += [0]
    return sol

def sol2routes(sol):
    # 转化为route的list，移除空路径
    if not sol or len(sol)<=2: return []
    return [[0]+list(r)+[0] for x, r in groupby(sol, lambda z: z == 0) if not x]

def objf(sol, D):
    # 计算路径长度
    return sum(( D[sol[i-1],sol[i]] for i in range(1,len(sol))))

def totald(sol, d):
    # 计算总负载量
    if d is None: return 0
    return sum( d[n] for n in sol )

def is_sorted(l):
    return all(l[i] <= l[i+1] for i in range(len(l)-1))

def _list_trim(l, e):
    """ works like string trimming but for lists """
    trimmed = list(l)
    while len(trimmed)>0 and trimmed[0]==e:
        del trimmed[0]
    while len(trimmed)>0 and trimmed[-1]==e:
        del trimmed[-1]
    return trimmed
    
def _list_split(l, e):
    return [list(group) for k, group in groupby(l, lambda x:x==e) if not k]  

def normalize_solution(sol):
    # 使从原点出发后到终点的第一个点小于回到原点前的最后一个点
    # 使各车辆从原点出发后到达的第一个点从小到大排列    
    if hasattr(sol[0], '__len__'):
        routes = [_list_trim(route, 0) for route in sol]
    else:
        routes = _list_split(sol, 0)
    nroutes = []

    for route in routes:
        if route[-1]<route[0]:
            nroutes.append( list( reversed(route) ) )
        else:
            nroutes.append( list(route) )
    
    nroutes.sort()
    
    nsol = [0]
    for nroute in nroutes:
        nsol += nroute + [0]
    
    return nsol

def print_results(sol, D, d, sol_type):
    routes = sol2routes(sol)
    objective = objf(sol, D)
    print("The solution of {} is: ".format(sol_type))
    for route_idx, route in enumerate(routes):
        print("Route #%d : %s, carry %d"%(route_idx+1, route, totald(route, d)))
    print("The objective of {} is: {}".format(sol_type, objective))