"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}


    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()


    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)


    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]


    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create queue
        to_visit = Queue()
        # create set for items we've already visited
        visited = set()
        # put the starting vertex into the queue
        to_visit.enqueue(starting_vertex)
        # as long as the queue isn't empty...
        while to_visit.size() > 0:
            # grab one out of the queue
            visit = to_visit.dequeue()
            # if it's not already been visited
            if visit not in visited:
                # add it to the list
                visited.add(visit)
                # and print it
                print(visit)
                # then queue all of its neighbors
                for neighbor in self.get_neighbors(visit):
                    to_visit.enqueue(neighbor)


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create stack
        to_visit = Stack()
        # create set for items we've already visited
        visited = set()
        # put the starting vertex into the stack
        to_visit.push(starting_vertex)
        # as long as the stack isn't empty...
        while to_visit.size() > 0:
            # grab one off the stack
            visit = to_visit.pop()
            # if it's not already been visited
            if visit not in visited:
                # add it to the list
                visited.add(visit)
                # and print it
                print(visit)
                # then add all neighbors to the stack
                for neighbor in self.get_neighbors(visit):
                    to_visit.push(neighbor)

    # pass in visited for future recursive calls, with default value of None
    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # print out the starting vertex
        print(starting_vertex)
        # on the first pass, create the set
        if visited is None:
            visited = set()
        # add the starting vertex to the set
        visited.add(starting_vertex)

        # check if the neighboring vertices have been visited
        for vertex in self.vertices[starting_vertex]:
            # if not, recursively call with that as the starting vertex
            if vertex not in visited:
                self.dft_recursive(vertex, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create a queue for the path 
        path = Queue()
        # create a set for the items we've visited
        visited = set()
        # the starting vertex is the first thing in the path
        path.enqueue([starting_vertex])
        # while the queue isn't empty
        # grab the first value
        while path.size() > 0:            
            p = path.dequeue()
            last_vertex = p[-1]
            # if it's not been visited, add it
            if last_vertex not in visited:
                visited.add(last_vertex)
            # check if the destination is a neighbor to the current vertex
            for neighbor in self.get_neighbors(last_vertex):
                npath = p.copy()
                npath.append(neighbor)
                # if so, return the completed path
                if neighbor == destination_vertex:
                    return npath
                path.enqueue(npath)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # create a stack for the path
        path = Stack()
        # create a set to store items we've already visited
        visited = set()
        # add the starting vertex to the path
        path.push([starting_vertex])
        # while the stack isn't empty
        # grab the last value
        while path.size() > 0:
            p = path.pop()
            last_vertex = p[-1]
            # if it hasn't been visited yet, add it to the list
            if last_vertex not in visited:
                visited.add(last_vertex)
            # check if the destination is a neighbor to the current vertex
            for neighbor in self.get_neighbors(last_vertex):
                npath = p.copy()
                npath.append(neighbor)
                # if so, return the completed path
                if neighbor == destination_vertex:
                    return npath
                path.push(npath)
                

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # print the current/starting value
        print(starting_vertex)
        # if it's the first loop, make the visited set
        if visited is None:
            visited = set()
        # if it's the first loop, make the path
        if path == None:
            path = []
        # add the starting/current vertex to the visited and path
        visited.add(starting_vertex)
        npath = [*path, starting_vertex]
        # did we find the destination? return the path
        if npath[-1] == destination_vertex:
            return npath        
        # check if the neighbors have been explored
        for neighbor in self.get_neighbors(starting_vertex):
            if neighbor not in visited:
                neighborpath = self.dfs_recursive(neighbor, destination_vertex, visited, npath)
                if neighborpath:
                    return neighborpath

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
