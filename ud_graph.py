# Course: CS261 - Data Structures
# Author: Joel Swenddal
# Assignment: 6
# Description: Undirected Graph Implementation -- using Adjacency List

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []

        return None

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return None

        if u not in self.adj_list:
            self.add_vertex(u)

        if v not in self.adj_list:
            self.add_vertex(v)

        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)

        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

        return None

    def remove_edge(self, v: str, u: str) -> None:
        """
        Takes two vertices remove edge between them
        from the graph. 
        """
        if v == u:
            return None

        elif v not in self.adj_list or u not in self.adj_list:
            return None

        elif v not in self.adj_list[u]:
            return None

        else:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

        return None

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """

        if v in self.adj_list:

            # if list is empty
            if not self.adj_list[v]:
                self.adj_list.pop(v)
                return None
            # not empty
            for node in self.adj_list[v]:
                self.adj_list[node].remove(v)
            self.adj_list.pop(v)

        return None

    def get_vertices(self) -> list:
        """
        Return list of vertices in the graph (any order)
        """

        if not self.adj_list:
            return []

        return self.adj_list.keys()

    def get_edges(self) -> list:
        """
        Return list of edges in the graph (any order).
        Edges are represented as tuples with two elements
        (the two adjacent vertices).
        """
        node_list = self.get_vertices()
        edge_list = []

        if not node_list:
            return node_list

        for node in node_list:
            for edge in self.adj_list[node]:
                if self.adj_list[node]:
                    edge_tup = (node, edge) if node < edge else (edge, node)
                if edge_tup not in edge_list:
                    edge_list.append(edge_tup)

        return edge_list

    def is_valid_path(self, path: list) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if not path:
            return True

        if len(path) == 1:
            if path[0] in self.adj_list.keys():
                return True
            else:
                return False

        index = 0
        current = path[index]
        next = path[index + 1]

        while index < len(path)-1:
            current = path[index]
            next = path[index + 1]
            if next not in self.adj_list[current]:
                return False

            index += 1

        return True

    def dfs(self, v_start, v_end=None) -> list:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        path_list = []

        if v_start not in self.adj_list:
            return path_list

        if v_end not in self.adj_list:
            v_end = None

        if v_end == v_start:
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

            sorted_list = sorted(self.adj_list[current], reverse=True)

            for neighbor in sorted_list:

                if neighbor not in path_list:
                    stack.append(neighbor)

        return path_list

    def bfs(self, v_start, v_end=None) -> list:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        path_list = []

        if v_start not in self.adj_list:
            return path_list

        if v_end not in self.adj_list:
            v_end = None

        if v_end == v_start:
            path_list.append(v_start)
            return path_list

        # push starting vertice into queue
        current = v_start
        queue = deque(current)

        # while queue not empty
        while queue and current != v_end:
            current = queue.popleft()
            if current not in path_list:
                path_list.append(current)

            sorted_list = sorted(self.adj_list[current], reverse=False)

            for neighbor in sorted_list:

                if neighbor not in path_list:
                    queue.append(neighbor)

        return path_list

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        visited_dict = {}
        vertices = self.get_vertices()
        # visited dictionary to track visited vertices
        # initialize all to False
        for each in vertices:
            visited_dict[each] = False

        connected_count = 0

        # check each vertice
        for each in vertices:
            # if it has not yet been visited, run dfs + update
            #  the visits dict
            if visited_dict[each] == False:
                self.dfs_helper(each, visited_dict)
                connected_count += 1

        return connected_count

    def dfs_helper(self, v_start, visited_dict) -> None:
        """
        DFS helper function count_connected_components.
        Takes a starting point and a list of bools indicating
        vertices that have been visited. Updates dict to True
        for any vertices visited during the dfs.
        """

        visited_dict[v_start] = True
        path_list = []

        if v_start not in self.adj_list:
            return None

        # push starting vertice onto stack
        current = v_start
        stack = [current]

        # while stack not empty
        while stack:
            current = stack.pop()
            if current not in path_list:
                path_list.append(current)
                visited_dict[current] = True

            for neighbor in self.adj_list[current]:

                if neighbor not in path_list:
                    stack.append(neighbor)

        return None

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    """

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
    """
