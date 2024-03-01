import sys
import heapq

class RouteFinder:
    def __init__(self, connections, heuristic=None):
        self.connections = connections
        self.heuristic = heuristic

    def search(self, origin, destination):
        if self.heuristic:
            return self.informed_search(origin, destination)
        else:
            return self.uninformed_search(origin, destination) 

    def uninformed_search(self, origin, destination):
        frontier = [(0, origin, [origin])]
        closed = set()
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 1  # Initialize nodes_generated to 1
        while frontier:
            cost, current_city, path = heapq.heappop(frontier)
            nodes_popped += 1
            if current_city == destination:
                return path, nodes_popped, nodes_expanded, nodes_generated
            if current_city in closed:
                continue  # Skip further processing for this node
            closed.add(current_city)
        # Generate successors
            if current_city in self.connections:
            # Increment nodes_expanded only when a node's successors are generated
                nodes_expanded += 1
                for neighbor, distance in self.connections[current_city]:
                # Generate successor
                    new_cost = cost + distance
                    heapq.heappush(frontier, (new_cost, neighbor, path + [neighbor]))
                    nodes_generated += 1
                    #print("Adding", neighbor, "to fringe with cost", new_cost)
        return None, nodes_popped, nodes_expanded, nodes_generated

    def informed_search(self, origin, destination):
        frontier = [(self.heuristic.get(origin, float('inf')), 0, origin, [origin])]
        closed = set()
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 1  # Initialize nodes_generated to 1

        while frontier:
            _, g_cost, current_city, path = heapq.heappop(frontier)
            nodes_popped += 1

            if current_city == destination:
                return path, nodes_popped, nodes_expanded, nodes_generated

            if current_city in closed:
                continue

            closed.add(current_city)
            nodes_expanded += 1  # Increment nodes_expanded when a node is expanded

        # Generate successors
            if current_city in self.connections:
                for neighbor, distance in self.connections[current_city]:
                    new_g_cost = g_cost + distance
                    new_f_cost = new_g_cost + self.heuristic.get(neighbor, float('inf'))
                    heapq.heappush(frontier, (new_f_cost, new_g_cost, neighbor, path + [neighbor]))
                    nodes_generated += 1  # Increment for each newly generated successor

        return None, nodes_popped, nodes_expanded, nodes_generated


def read_input(filename):
    connections = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == 'END OF INPUT':
                break
            source, dest, distance = line.split()
            distance = float(distance)
            connections.setdefault(source, []).append((dest, distance))
            connections.setdefault(dest, []).append((source, distance))
    return connections

def read_heuristic(heuristic_filename):
    heuristic = {}
    with open(heuristic_filename, 'r') as file:
        for line in file:
            city, cost = line.split()
            heuristic[city] = float(cost)
    return heuristic

def find_route(input_filename, origin_city, destination_city, heuristic_filename=None):
    connections = read_input(input_filename)
    heuristic = None
    if heuristic_filename:
        heuristic = read_heuristic(heuristic_filename)
    route_finder = RouteFinder(connections, heuristic)
    route, nodes_popped, nodes_expanded, nodes_generated = route_finder.search(origin_city, destination_city)
    
    if route:
        print("Nodes Popped:", nodes_popped)
        print("Nodes Expanded:", nodes_expanded)
        print("Nodes Generated:", nodes_generated)
        print("Distance:", sum(connections[route[i]][j][1] for i in range(len(route) - 1) for j in range(len(connections[route[i]])) if connections[route[i]][j][0] == route[i + 1]), "km")
        print("Route:")
        for i in range(len(route) - 1):
            current_city = route[i]
            next_city = route[i + 1]
            distance = next(connection[1] for connection in connections[current_city] if connection[0] == next_city)
            print(current_city, "to", next_city + ",", distance, "km")
    else:
        print("Nodes Popped:", nodes_popped)
        print("Nodes Expanded:", nodes_expanded)
        print("Nodes Generated:", nodes_generated)
        print("Distance: infinity")
        print("Route:")
        print("None")

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python find_route.py input_filename origin_city destination_city [heuristic_filename]")
    else:
        input_filename = sys.argv[1]
        origin_city = sys.argv[2]
        destination_city = sys.argv[3]
        heuristic_filename = sys.argv[4] if len(sys.argv) == 5 else None
        find_route(input_filename, origin_city, destination_city, heuristic_filename)



   



