#! /usr/bin/env python3
import sys
import time
import numpy as np
import heapq
import threading
import random

#HELPER FUNCTIONS 
 
#Dijkstra's shortest path algorithm: good to use it for finding shortest path from one source node to all other nodes of graph with weights
#that are not negative
def shortest_path_algorithm(nodes,graph_adj_list, T, max_val):
    n=max_val+1

    #results to be returned
    top_source_node=0; #arbitrarily set as 0 -> to be changed iteratively as algorithm runs
    count_influence=0; #starts with no influences

    #loop thorough and do dijkstra's on every possible vertices in nodes
    for vertex in nodes:

       #INITIALIZATION=========================================================================================================
        #starting node
        start=vertex

        #track visited nodes
        visited=[False]*n #keeps track of all visted nodes: initialized as False because no other node has been visited yet

        #keep track of node and their corresponding distances from source
        time_distance=[float('inf')] *n #initial distance of all nodes with reference to source is INF -> to access time_distance of node3 from current node: time_distance[node3]
        time_distance[int(start)]=0 #initialize starting node with distance=0

        #Use min heap to extract next min time distance node from wave front
        heap=[]
        heapq.heappush(heap, (0,int(start))) #insert first element of heap as the start source and its distance: heapq sorts according to first element of tuple

        #explore all possible nodes until heap is completed exhausted of all resources
        while heap:
            #pop smallest distance from heap
            (distance,current)=heapq.heappop(heap)

            #check if node has already been visited
            if visited[current]:
                continue
                
            #mark current node as visited
            visited[current]=True

            # #Iterate over the neighboring nodes of current node
            # for neighbor in range(n):
            #     #Check if the neighbor exists. If it does add it to the heap for the next iteration
            #     if graph_adj_list[current][neighbor]>0:
            #         #calculate distance to neighbor node
            #         tentative_distance = distance + graph_adj_list[current][neighbor]

            #         #check if the tentatively calculated distance is smaller than the current distance
            #         if tentative_distance< time_distance[neighbor]:
            #             #update distance for this neighbor and push neighbor node onto heap
            #             time_distance[neighbor]=tentative_distance
            #             heapq.heappush(heap, (tentative_distance, neighbor))
                        
            # Iterate over the neighboring nodes of current node
            if current not in graph_adj_list:
                continue

            for neighbor, weight in graph_adj_list[current]:
                # calculate distance to neighbor node
                tentative_distance = distance + weight

                # check if the tentatively calculated distance is smaller than the current distance
                #print(neighbor)
                #print("length of distancce array" ,len(time_distance))
                if tentative_distance < time_distance[neighbor]:
                    # update distance for this neighbor and push neighbor node onto heap
                    time_distance[neighbor] = tentative_distance
                    heapq.heappush(heap, (tentative_distance, neighbor))
        #Update current best source node with most spread 
        # print(T)
        #print(time_distance)
        count_of_nodes_influenced=0;
        for distance_of_node in time_distance:
            if distance_of_node>=0:
                if distance_of_node<float(T):
                    count_of_nodes_influenced=count_of_nodes_influenced + 1
        #update only if current count is greater than previous count_influence
        if count_of_nodes_influenced>count_influence:
            count_influence=count_of_nodes_influenced
            top_source_node=start

        #maxheap to track spread of all vertexes
        # heapq.heappush(maxheap,(-count_of_nodes_influenced,current))
        # print(maxheap)

    #return top_source_node and count_influence by random probability
    # neg_spread, current_best_node=heapq.heappop(maxheap)
    # pos_spread_best=-neg_spread
    # most_influential.append(current_best_node)

    # while maxheap:
    #     neg_spread, current_best_node=heapq.heappop(maxheap)
    #     if(-neg_spread!=pos_spread_best):
    #         break
    #     else:
    #         most_influential.append((-neg_spread,current_best_node))

    # #randomly choose most influential
    # random_num=random.randint(0,len(most_influential)-1)
    # return most_influential[random_num][1], most_influential[random_num][0]
    return top_source_node,count_influence

#creates adjaceny matrix and create return set of nodes
def create_graph_matrix (input_text_file, graph_matrix):
    file = open(input_text_file, "r")

    #initialize set
    set_of_v =set()

    #populate adjacency matrix
    for line in file:
        elements =line.split()
        #sets ensure no dup's
        set_of_v.add(int(elements[0]))
        
        graph_matrix[int(elements[0])][int(elements[1])]=elements[2]

    return set_of_v

#creates adjacnecy List
def create_adjacency_list(input_text_file):
    adjacency_list = {}# using dictionary to store 
    set_of_v=set()
    max_value_of_nodes=0
    with open(input_text_file, 'r') as file:
        for line in file:
            elements = line.split()
            vertex = int(elements[0])
            edge = int(elements[1])
            weight = float(elements[2])
            if vertex not in adjacency_list:
                adjacency_list[vertex] = []
            adjacency_list[vertex].append((edge, weight))

            #adda nodes into 
            set_of_v.add(int(elements[0]))
            max_value_of_nodes=max(vertex,edge,max_value_of_nodes)
    return adjacency_list,set_of_v,max_value_of_nodes

#main of program
input_text_file= sys.argv[1] 
T=sys.argv[2]

#initialization
graph_adj_list, nodes, max_val= create_adjacency_list(input_text_file)

#time start:
start_time=time.time()
#algorithm 
top_source_node,spread=shortest_path_algorithm(nodes,graph_adj_list, T, max_val)
#time end:
end_time=time.time()

#results
print("TOP-1 INFLUENCER: " + str(top_source_node) + " SPREAD: " + str(spread) + " TIME: " + str(end_time - start_time))


#sources:
#https://www.askpython.com/python/array/initialize-a-python-array
#https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
