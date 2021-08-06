# Course: CS261 - Data Structures
# Author: Joel Swenddal
# Assignment: 6
# Description: Directed Graph Implementation -- using Adjacency Matrix

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph. Returns
        an integer representing the updated number of
        integers in the graph.
        """
        self.v_count += 1

        new_node = [0 for each in range(0, self.v_count)]

        self.adj_matrix.append(new_node)

        if self.v_count > 1:
            for node in self.adj_matrix:
                if len(node) < self.v_count:
                    for index in range(len(node), self.v_count):
                        node.append(0)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Takes a source vertice, destination vertice, and weight
        and adds a directional edge from the first to the second with
        the indicated weight.
        """
        if (src >= self.v_count) or (dst >= self.v_count) or (weight < 1) or (src == dst):
            return None

        self.adj_matrix[src][dst] = weight

        return None

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Takes a source and destination vertice and
        removes the edge between them if it exists
        in the graph and if both vertices exist.
        """
        if (src < 0) or (dst < 0) or (src == dst) or (src >= self.v_count) or (dst >= self.v_count):
            return None

        self.adj_matrix[src][dst] = 0

        return None

    def get_vertices(self) -> list:
        """
        Returns a list of the vertices of the graph.
        """
        vertices = [x for x in range(0, self.v_count)]
        return vertices

    def get_edges(self) -> list:
        """
        Returns a list of the edges of the graph. Each
        edge is represented as a tuple with the first element
        being the source node index, the second being the
        destination node index, and the third being the
        weight of the edge.
        """

        node_index = 0
        edge_index = 0
        result_list = []

        for node_index in range(0, self.v_count):
            for edge_index in range(0, self.v_count):
                if self.adj_matrix[node_index][edge_index] > 0:
                    edge_tup = (node_index, edge_index,
                                self.adj_matrix[node_index][edge_index])
                    result_list.append(edge_tup)

        return result_list

    def is_valid_path(self, path: list) -> bool:
        """
        Takes a list of vertices and returns True
        if the sequence of vertices represents a valid
        path in the graph. An empty path is considered
        valid in this scenario.
        """
        # if path is empty
        if not path:
            return True

        path_length = len(path)

        # if a path node is not in the graph
        for node in path:
            if node < 0 or node >= self.v_count:
                return False
        # if only one node in path
        if path_length == 1:
            return True

        current = 0
        next = current + 1

        # track through each node in path
        # if there is an edge in a node's
        # list pointing to the next node,
        # then continue, otherwise False
        # there is no edge between those nodes
        while next < len(path):
            step = path[current]
            next_step = path[next]
            if self.adj_matrix[step][next_step] <= 0:
                return False
            current += 1
            next += 1

        return True

    def dfs(self, v_start, v_end=None) -> list:
        """
        Takes an starting vertice (v_start) and
        an optional ending vertice (v_end) and
        performs a depth-first search. Returns a
        list of vertices in the order they were
        visited.
        """
        path_list = []

        if v_start < 0 or v_start >= self.v_count:
            return path_list

        if v_end is None or v_end < 0 or v_end >= self.v_count:
            v_end = None

        if v_start == v_end:
            path_list.append(v_start)
            return path_list

        # push starting vertice onto stack
        current = v_start
        stack = [current]

        # while stack not empty
        while stack and current != v_end:
            current = stack.pop()

            if current not in path_list:
                path_list.append(current)

            # if there is a neighbor not yet in path list, push to
            # stack in descending order (so they pop in ascending order)
            for index in range(len(self.adj_matrix[current])-1, -1, -1):
                if self.adj_matrix[current][index] >= 1:
                    neighbor = index
                    if neighbor not in path_list:
                        stack.append(neighbor)

        return path_list

    def bfs(self, v_start, v_end=None) -> list:
        """
        Takes an starting vertice (v_start) and
        an optional ending vertice (v_end) and
        performs a breadth-first search. Returns a
        list of vertices in the order they were
        visited.
        """
        path_list = []

        if v_start < 0 or v_start >= self.v_count:
            return path_list

        if v_end is None or v_end < 0 or v_end >= self.v_count:
            v_end = None

        if v_start == v_end:
            path_list.append(v_start)
            return path_list

        # push starting vertice onto queue (using deque)
        current = v_start
        queue = deque([current])

        # while queue not empty
        while queue and current != v_end:
            current = queue.popleft()
            if current not in path_list:
                path_list.append(current)

         # if there is a neighbor not yet in path list, push to
            # queue in ascending order (so they pop ascending)
            for index in range(0, len(self.adj_matrix[current])):
                if self.adj_matrix[current][index] >= 1:
                    neighbor = index
                    if neighbor not in path_list:
                        queue.append(neighbor)

        return path_list

    def has_cycle(self):
        """
        Returns True if there is at least one cycle
        in the graph. Otherwise, returns False.
        """
        explored_list = []
        currently_explored_list = []
        for index in range(0, self.v_count):
            explored_list.append(False)
            currently_explored_list.append(False)

        for index in range(0, self.v_count):
            # returns true if graph has a cycle
            if explored_list[index] == False:
                if self.has_cycle_rec(index, explored_list, currently_explored_list) == True:
                    return True

        return False

    def has_cycle_rec(self, current, explored_list, currently_explored_list):
        """Recursive helper for has_cycle() method. Takes
        a current vertice, a list of explored vertices, and
        a list of vertices currently being explored. This
        is using a recursive, depth-first search approach."""
        # current node marked as explored
        explored_list[current] = True
        # current node marked as currently being explored
        currently_explored_list[current] = True
        neighbor_list = []

        # identify descendants
        for index in range(0, len(self.adj_matrix[current])):
            if self.adj_matrix[current][index] > 0:
                neighbor_list.append(index)

        # if descendant has been visited and also is being explored, then
        # there is a cycle
        for neighbor in neighbor_list:
            if explored_list[neighbor] == False:
                if self.has_cycle_rec(neighbor, explored_list, currently_explored_list) == True:
                    return True

            elif currently_explored_list[neighbor] == True:
                return True
        # mark as not currently being explored
        currently_explored_list[current] = False
        return False

    def dijkstra(self, src: int) -> list:
        """
        Takes a source vertex and calculates the shortest path
        from a given vertex to all other vertices in the graph.
        Returns a list showing the shortest path to each
        vertex from the source. In returned list, the value at
        index 0 is the length of the shortest path from the source
        vertex to index 0, the value at index 1 is the length of 
        the path to index 1, etc. If a value is not reachable from
        the source, the returned value is 'inf'.
        """
        # fill a dictionary with keys representing each
        # vertex in graph (0...graph_length - 1), and values
        # representing calculated distances from the source
        # (initialized to float('inf'))
        visited_dict = {vertex: float('inf')
                        for vertex in range(0, self.v_count)}
        # enter the src node into the visited dictionary with
        # distance 0
        visited_dict[src] = 0
        # push the source node into the priority queue
        heap = [(0, src)]

        while len(heap) > 0:
            # pop the lowest valued distance from the priority queue
            current_distance, current_node = heapq.heappop(heap)

            # processing a node - if the current distance is less
            # than the saved one (in the visited dictionary)
            if current_distance <= visited_dict[current_node]:
                # identify the descendant neighbors and their distances
                # from the current node
                for index in range(0, self.v_count):
                    neighbor_distance = self.adj_matrix[current_node][index]
                    if neighbor_distance > 0:
                        neighbor = index
                        # identify what the new distance to the descendant
                        # neighbor would be
                        new_distance = current_distance + neighbor_distance
                        # if the new distance is less than the one on record
                        # for the descendant neighbor, enter the new lower
                        # distance in the visited dict for the neighbor,
                        # then push it into the priority queue
                        if new_distance < visited_dict[neighbor]:
                            visited_dict[neighbor] = new_distance
                            heapq.heappush(heap, (new_distance, neighbor))

        distances_list = list(visited_dict.values())

        return distances_list


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0, 99)]
    for src, dst, *weight in edges_to_add:
        g.add_edge(src, dst, *weight)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
