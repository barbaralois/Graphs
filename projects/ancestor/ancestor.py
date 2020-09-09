from util import Stack, Queue

class Graph:
    def __init__(self):
        self.vertices = {}


    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()


    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)


    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]


    def bft(self, starting_vertex):
        to_visit = Queue()
        visited = set()
        to_visit.enqueue(starting_vertex)
        while to_visit.size() > 0:
            visit = to_visit.dequeue()
            if visit not in visited:
                visited.add(visit)
                print(visit)
                for neighbor in self.get_neighbors(visit):
                    to_visit.enqueue(neighbor)


    def dft(self, starting_vertex):
        to_visit = Stack()
        visited = set()
        to_visit.push(starting_vertex)
        while to_visit.size() > 0:
            visit = to_visit.pop()
            if visit not in visited:
                visited.add(visit)
                print(visit)
                for neighbor in self.get_neighbors(visit):
                    to_visit.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        print(starting_vertex)
        if visited is None:
            visited = set()
        visited.add(starting_vertex)
        for vertex in self.vertices[starting_vertex]:
            if vertex not in visited:
                self.dft_recursive(vertex, visited)

    def bfs(self, starting_vertex, destination_vertex):
        path = Queue()
        visited = set()
        path.enqueue([starting_vertex])
        while path.size() > 0:            
            p = path.dequeue()
            last_vertex = p[-1]
            if last_vertex not in visited:
                visited.add(last_vertex)
            for neighbor in self.get_neighbors(last_vertex):
                npath = p.copy()
                npath.append(neighbor)
                if neighbor == destination_vertex:
                    return npath
                path.enqueue(npath)

    def dfs(self, starting_vertex, destination_vertex):
        path = Stack()
        visited = set()
        path.push([starting_vertex])
        while path.size() > 0:
            p = path.pop()
            last_vertex = p[-1]
            if last_vertex not in visited:
                visited.add(last_vertex)
            for neighbor in self.get_neighbors(last_vertex):
                npath = p.copy()
                npath.append(neighbor)
                if neighbor == destination_vertex:
                    return npath
                path.push(npath)
                

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None, path=None):
        print(starting_vertex)
        if visited is None:
            visited = set()
        if path == None:
            path = []
        visited.add(starting_vertex)
        npath = [*path, starting_vertex]
        if npath[-1] == destination_vertex:
            return npath        
        for neighbor in self.get_neighbors(starting_vertex):
            if neighbor not in visited:
                neighborpath = self.dfs_recursive(neighbor, destination_vertex, visited, npath)
                if neighborpath:
                    return neighborpath

def earliest_ancestor(ancestors, starting_node):
    # make the graph
    graph = Graph()

    # go over the data and create nodes
    for pair in ancestors:
        # if the 1st value doesn't exist, add it
        if pair[0] not in graph.vertices:
            graph.add_vertex(pair[0])
        # if the 2nd value doesn't exist, add it
        if pair[1] not in graph.vertices:
            graph.add_vertex(pair[1])
        # connect the vertices
        graph.add_edge(pair[1], pair[0])

    # create a queue and add the starting node
    queue = Queue()
    queue.enqueue([starting_node])
    # keep track of the current longest path
    longest_path = []

    # while the queue isn't empty
    while queue.size() > 0:
        vertex_path = queue.dequeue()

        # if the current path is equal to the prior longest, keep the one with the smaller numerical value
        if len(vertex_path) == len(longest_path) and vertex_path[-1] < longest_path[-1]:
            longest_path = vertex_path
        # if the current path is longer than prior longest, replace it
        if len(vertex_path) > len(longest_path):
            longest_path = vertex_path
        
        # add the neighbors to the queue
        for neighbors in graph.get_neighbors(vertex_path[-1]):
            temp_path = vertex_path.copy()
            temp_path.append(neighbors)
            queue.enqueue(temp_path)
        
        # if the longest path isn't greater than 1, it didn't find any parents
    if len(longest_path) <= 1:
        # so return -1 (per the README)
        return -1
    # if it did find parents, return the path after finishing the loop
    else:
        return longest_path[-1]
