from operator import itemgetter
from collections import deque
C_EPS = 1e-10
S_EPS = 1e-10

class _PeekQueue: 
    def __init__(self, l):
        self.posleft = -1
        self.posright = 0
        self.l = list(l)
        
    def __len__(self):
        return len(self.l)-(self.posleft+1)+(self.posright)

    def __getitem__(self, idx):
        if idx>=len(self):
            raise IndexError
        return self.l[self.posleft+1+idx]
        
    def peekleft(self):
        if len(self)==0:
            raise IndexError
        return self.l[self.posleft+1]

    def popleft(self):
        if len(self)==0:
            raise IndexError
        self.posleft+=1
        return self.l[self.posleft]    
    
    def peekright(self):
        if len(self)==0:
            raise IndexError
        return self.l[self.posright-1]

    def popright(self):
        if len(self)==0:
            raise IndexError
        self.posright-=1
        return self.l[self.posright]

def get_seed_node(seed_mode, node_nearest_neighbors, served):
    seed_node = None
    while True:
        if seed_mode=='closest':
            seed_node  = node_nearest_neighbors[0].popleft()[0]
        elif seed_mode=='farthest':
            seed_node  = node_nearest_neighbors[0].popright()[0]
        if not served[seed_node]:
            break 
    return seed_node 

def nearest_neighbor_init(D, d, C, initialize_routes_with="farthest"):
    N = len(D)
    node_nearest_neighbors = [None]*N
    for i in range(N):
        node_nearest_neighbors[i] = _PeekQueue( sorted(enumerate(D[i][:]),
                                                        key=itemgetter(1)) ) # 按D[i][:]中元素大小排序
        node_nearest_neighbors[i].popleft() # self.posleft=0  

    served = [False]*N
    served[0]=True
    
    sol = [0]
    route_nodes = None # 某条路线的路径点
    prev_added = None # 上一个被添加的点
    route_demands = 0.0 # 某条路线的承载量
    
    try:      
        while True:

            if not route_nodes:
                seed_node =  get_seed_node(initialize_routes_with, node_nearest_neighbors, served) # 找一个没有被服务过的点作为初始点
                route_nodes = deque()
                route_nodes.append(seed_node)
                prev_added = seed_node
                if C: route_demands = d[seed_node]
                served[seed_node]=True 
            else:        
                prev_node = prev_added
                nn_node = None # 最近的没有被服务过的点
                while True: # 找一个最近的没有被服务过的点
                    nn_node = node_nearest_neighbors[prev_node].peekleft()[0]
                    if served[nn_node]:
                        node_nearest_neighbors[prev_node].popleft()
                    else:
                        break
                                    
                constraints_violated = (C and route_demands+d[nn_node]-C_EPS>C)
                if constraints_violated:
                    current_route = [0]+list(route_nodes)+[0]
                    sol.extend( current_route[1:] )
                    route_nodes = None
                else:
                    if C:
                        route_demands += d[nn_node]
                        route_nodes.append(nn_node)
                    prev_added = nn_node
                    served[nn_node]=True

                    node_nearest_neighbors[prev_node].popleft()
            
    except (IndexError) as e:
        if route_nodes:
            sol.extend(route_nodes)
            sol.append(0)
      
    return sol