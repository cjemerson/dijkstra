# dijkstra.py
#
# Charles Emerson
# December 13, 2019
# 
# Module for determining shortest path to every vertex given an adjacency list 

import sys
import heapq
from collections import namedtuple

def dijkstra(adjacency_list, source_vertex, cull_distance = sys.maxsize):
    """
    Implementation of Dijkstra's Algorithm for finding shortest
    path to all vertices in a graph.

    Parameters
    ----------
    adjacency_list (dict of int : (dict of int : int))
        Maps vertices to a dictionary of neighboring vertices as
        keys and whose data is the distance between them with.
        *** Distances must be non-negative. ***
    source_vertex (int)
        The vertex to start the algorithm (distance zero vertex)
    cull_distance (int) *optional, defaults to sys.maxsize
        The maximum distance desired to traverse plus 1
        (Represents infinite distance)

    Returns
    -------
    dict(int : int)
        A dictionary whose keys are the reachable vertices of the
        adjacency list and data is the distance required to reach
        that vertex from the source vertex.
    """
    pq = []         # Priority Queue (Min-Heap) holding vertices to traverse
    distance = {}   # Distance Map (Return Value)
    count = 0       # Counter for Creating Unique IDs
    valid_ids = {}  # Maps Vertices to Their Valid ID

    # Named tuple to be used in the priority queue
    DistVtxId = namedtuple('DistVtxId', 'distance vertex id')


    ### SETUP

    # Add each vertex in the adjacency list to the priority queue
    for vertex in adjacency_list.keys():

        id = count # Unique ID for each vertex in the priority queue
        count += 1
        temp = None # <- for name scope

        if (vertex == source_vertex):
            # Source vertex gets distance zero from itself
            temp = DistVtxId(0, vertex, id)

            # Add the source vertex to the final result
            distance[source_vertex] = 0
        else:
            # Non-Source vertices start at infinite distance
            temp = DistVtxId(cull_distance, vertex, id)

        # Push the vertex onto the priority queue
        heapq.heappush(pq, temp)
        valid_ids[vertex] = temp.id

        # Add this vertex's initial distance to the return value
        distance[vertex] = temp.distance


    ### TRAVERSAL

    # Iterates (at most) the number of vertices times
    for i in range(0, len(adjacency_list)):

        # Get the lowest edge distance from the priority queue
        u_star = heapq.heappop(pq)

        # Ignore this element if it does not have a valid ID
        # Occurs when the priority of a vertex has been "updated"
        if (valid_ids[u_star.vertex] != u_star.id):
            continue

        # For every neighboring vertex
        for vertex, edge_weight in adjacency_list[u_star.vertex].items():
            new_distance = u_star.distance + edge_weight
            old_distance = distance[vertex]

            # If we can reach the neighbor covering less distance from
            # the source
            if (new_distance < old_distance):
                distance[vertex] = new_distance

                # (Effectively) Update the priority (distance) of the
                # vertex in the priority queue
                temp = DistVtxId(new_distance, vertex, count)
                heapq.heappush(pq, temp)
                valid_ids[temp.vertex] = temp.id
                count += 1

    # Cull the vertices that were unreachable (or farther away from
    # the source than the cull_distance)
    distance = {vtx : dist for vtx, dist in distance.items() if dist != cull_distance}    

    return distance
