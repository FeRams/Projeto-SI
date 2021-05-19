from heapq import heappop, heappush
import networkx as nx
from random import randint
import collections

class DeliveryAgent:
    map_queue = collections.deque()
    delivery_route_queue = collections.deque()
    delivery_costs_queue = collections.deque()

    #
    def __init__(self):

        #generates all maps
        for i in range(0,10):
            print('Generating map', i)
            graph = nx.tutte_graph()
            self.map_queue.append(graph)

        print('\nAll maps generated.\nStarting search protocols...')

        # generates astar path for each map
        while self.map_queue:
            print('\nGetting map...')
            curr_map = self.map_queue.popleft()

            # random source and target for each graph
            length = len(curr_map.nodes)
            source = randint(0,1000) % length
            target = randint(0,1000) % length
            while (source == target):
                target = randint(0,1000) % length

            print('Finding best path...')
            curr_map = nx.astar_path(curr_map, source, target)
            curr_cost = len(curr_map)
            print('Setting delivery routes...')
            self.delivery_route_queue.append(curr_map)
            self.delivery_costs_queue.append(curr_cost)

        print('\nAll delivery routes found. \nStarting delivery...\n')
        
        while self.delivery_route_queue:
            curr_map = self.delivery_route_queue.popleft()
            print('Delivery route: ', curr_map)
            if self.delivery_costs_queue:
                cost = self.delivery_costs_queue.popleft()
            print('Delivery complete with time:', cost ,'min\n')

delivery_agent_1 = DeliveryAgent()