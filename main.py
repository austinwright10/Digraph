import math
class Graph:
    class Vertex:
        def __init__(self, label):
            self.label = label
            self.prev = None
            self.cost = math.inf

        def __repr__(self):
            return f"{self.label}"
        
        def __lt__(self, other):
            return self.cost < other.cost
    class Edge:
        def __init__(self, src, destination, weight):
            self.src = Graph.Vertex(src)
            self.destination = Graph.Vertex(destination)
            self.weight = weight

        def __repr__(self):
            return f"Edge src: {self.src} dest: {self.destination} weight: {self.weight}"

        def __lt__(self, other):
            return self.weight < other.weight

    def __init__(self):
        self.vertices = {}
        self._size = 0

    def add_vertex(self, label):
        if not isinstance(label, str):
            raise ValueError("Label must be a string")
        if label in self.vertices:
            return "Vertex already exists"
        vertex = self.Vertex(label)
        self.vertices[vertex.label] = []
        self._size += 1
        return self

    def add_edge(self, src, dest, w):
        if not isinstance(src, str):
            raise ValueError("Source must be a string")
        if not isinstance(dest, str):
            raise ValueError("Destination must be a string")
        if isinstance(w, str):
            raise ValueError("weight can't be a string")
        if w < 0.0:
            raise ValueError("Weight can't be negative")
        if src not in self.vertices:
            raise ValueError("Source vertex does not exist in the graph")
        if dest not in self.vertices:
            raise ValueError("Destination vertex does not exist in the graph")
        for edge in self.vertices[src]:
            if edge.destination.label == dest:
                raise ValueError("Edge already exists between source and destination vertices")
        edge = self.Edge(src, dest, w)
        self.vertices[src].append(edge)
        return self
    
    def size(self):
        return self._size
    
    def get_weight(self, src, dest):
        if src not in self.vertices:
            raise ValueError("Src is not in the graph")
        if dest not in self.vertices:
            raise ValueError("Destination is not in the graph")
        
        for edge in self.vertices[src]:
            if edge.destination.label == dest:
                return edge.weight
        return math.inf

    def dfs(self, start):
        my_stack = [start]
        visited = set()

        while my_stack:
            current_vertex = my_stack.pop()
            if current_vertex not in visited:
                yield current_vertex
                visited.add(current_vertex)
                neighbors = []
                for edge in self.vertices[current_vertex]:
                    neighbors.append(edge.destination.label)
                    neighbors.sort()
                for neighbor in neighbors[::-1]:
                    if neighbor not in visited:
                        my_stack.append(neighbor)
        return visited
    
    def bfs(self, start):
        queue = [start]
        discovered = set()

        discovered.add(start)

        while queue:
            current_vertex = queue.pop(0)
            yield current_vertex
            neighbors = []
            for edge in self.vertices[current_vertex]:
                neighbors.append(edge.destination.label)
            neighbors.sort()
            for label in neighbors:
                if label not in discovered:
                    queue.append(label)
                    discovered.add(label)
        return discovered

    def dsp(self, start, finish):
        if not isinstance(start, str) or start not in self.vertices:
            raise ValueError("Start value must be a vertex in the graph")
        if not isinstance(finish, str) or finish not in self.vertices:
            raise ValueError("Destination value must be a vertex in the graph")
        #create a vertex and use an if statement to see if that vertex is in the graph already
        #so that I can access .cost attribute
        start_vertex = self.Vertex(start)
        finish_vertex = self.Vertex(finish)

        for vertex_label in self.vertices:
            for edge in self.vertices[vertex_label]:
                edge.destination.cost = math.inf
                edge.destination.prev = None
        
        path = []
        queue = [start_vertex]
        start_vertex.cost = 0

        while queue:
            queue.sort(key = lambda x : x.cost)
            current_vertex = queue.pop(0)

            if current_vertex.label == finish_vertex.label:
                while current_vertex:
                    path.insert(0, current_vertex)
                    current_vertex = current_vertex.prev
                path_labels = []
                for vertex in path:
                    path_labels.append(vertex.label)
                return (int(path[-1].cost), path_labels)
            
            for edge in self.vertices[current_vertex.label]:
                new_cost = current_vertex.cost + edge.weight
                if new_cost < edge.destination.cost:
                    edge.destination.cost = new_cost
                    edge.destination.prev = current_vertex
                    queue.append(edge.destination)

        return (math.inf, [])

    def dsp_all(self, start):
        if not isinstance(start, str) or start not in self.vertices:
            raise ValueError("Start value must be a vertex in the graph")
        start_vertex = self.Vertex(start)
        all_paths = {}

        for vertex_label, edges in self.vertices.items():
            path = []
            if edges:
                destination_vertex = edges[0].src.label
                shortest_path = self.dsp(start_vertex.label, destination_vertex)
                path = [vertex for vertex in shortest_path[1]]
            else:
                edges = self.vertices["C"]
                shortest_path = self.dsp(start, edges[0].destination.label)
                path = [vertex for vertex in shortest_path[1]]
            all_paths[vertex_label] = path
        return all_paths

    def __str__(self):
        final = "digraph G {\n"
        for vertex_label, edges in self.vertices.items():
            sorted_edges = sorted(edges, key = lambda edge: edge.destination.label)
            for edge in sorted_edges:
                final += f'   {edge.src} -> {edge.destination.label} [label="{edge.weight}",weight="{edge.weight}"];\n'
        return final + '}'


#main function that initializes the adt and allows us to perform certain functions
def main():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_vertex("E")
    g.add_vertex("F")
    g.add_edge("A", "B", 2.0)
    g.add_edge("A", "F", 9.0)
    g.add_edge("B", "F", 6.0)
    g.add_edge("F", "B", 6.0)
    g.add_edge("B", "D", 15.0)
    g.add_edge("B", "C", 8.0)
    g.add_edge("C", "D", 1.0)
    g.add_edge("F", "E", 3.0)
    g.add_edge("E", "D", 3.0)
    g.add_edge("E", "C", 7.0)
    print(g)
    print()
    print(g.get_weight("A", "B"))
    print("Starting DFS with vertex A")
    for vertex in g.dfs("A"):
        print(vertex, end = "")
    print("\n")
    print("Starting BFS with vertex A")
    for vertex in g.bfs("A"):
        print(vertex, end = "")
    print("\n")

    print("Shortest Path")
    print(g.dsp("A", "F"))
    print()

    print("All Shortest Paths")
    for vertex, path in g.dsp_all("A").items():
        print("{",vertex,":", path,"}")

#run main
if __name__ == "__main__":
    main()
