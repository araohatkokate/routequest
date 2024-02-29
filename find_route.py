# import sys
# import heapq

# class RouteFinder:
#     def __init__(self, connections):
#         self.connections = connections

#     def uninformed_search(self, origin, destination):
#         frontier = [(origin, [origin])]
#         explored = set()
#         nodes_popped = 0
#         while frontier:
#             current_city, path = frontier.pop(0)
#             nodes_popped += 1
#             if current_city == destination:
#                 return path, nodes_popped, len(explored) + len(frontier) + 1
#             explored.add(current_city)
#             if current_city in self.connections:
#                 for neighbor, _ in self.connections[current_city]:
#                     if neighbor not in explored:
#                         frontier.append((neighbor, path + [neighbor]))
#                         explored.add(neighbor)
#         return None, nodes_popped, len(explored) + len(frontier)

#     def informed_search(self, origin, destination, heuristic):
#         frontier = [(0, origin, [origin])]
#         explored = set()
#         nodes_popped = 0
#         while frontier:
#             _, current_city, path = heapq.heappop(frontier)
#             nodes_popped += 1
#             if current_city == destination:
#                 return path, nodes_popped, len(explored) + len(frontier) + 1
#             explored.add(current_city)
#             if current_city in self.connections:
#                 for neighbor, distance in self.connections[current_city]:
#                     if neighbor not in explored:
#                         h = heuristic(neighbor)
#                         heapq.heappush(frontier, (path[-1] + distance + h, neighbor, path + [neighbor]))
#                         explored.add(neighbor)
#         return None, nodes_popped, len(explored) + len(frontier)

# def read_input(filename):
#     connections = {}
#     with open(filename, 'r') as file:
#         for line in file:
#             if line.strip() == 'END OF INPUT':
#                 break
#             source, dest, distance = line.split()
#             distance = float(distance)
#             connections.setdefault(source, []).append((dest, distance))
#             connections.setdefault(dest, []).append((source, distance))
#     return connections

# def read_heuristic(filename):
#     heuristic = {}
#     with open(filename, 'r') as file:
#         for line in file:
#             city, h_value = line.split()
#             heuristic[city] = float(h_value)
#     return heuristic

# def find_route(input_filename, origin_city, destination_city, heuristic_filename=None):
#     connections = read_input(input_filename)
#     route_finder = RouteFinder(connections)
    
#     if heuristic_filename:
#         heuristic = read_heuristic(heuristic_filename)
#         heuristic_func = lambda city: heuristic.get(city, float('inf'))
#         route, nodes_popped, nodes_generated = route_finder.informed_search(origin_city, destination_city, heuristic_func)
#     else:
#         route, nodes_popped, nodes_generated = route_finder.uninformed_search(origin_city, destination_city)
    
#     if route:
#         print("Nodes Popped:", nodes_popped)
#         print("Nodes Expanded:", len(route) - 1)
#         print("Nodes Generated:", nodes_generated)
#         print("Distance:", sum(connections[route[i]][j][1] for i in range(len(route) - 1) for j in range(len(connections[route[i]])) if connections[route[i]][j][0] == route[i + 1]), "km")
#         print("Route:")
#         for i in range(len(route) - 1):
#             print(route[i], "to", route[i + 1], ",", next(connection[1] for connection in connections[route[i]] if connection[0] == route[i + 1]), "km")
#     else:
#         print("Nodes Popped:", nodes_popped)
#         print("Nodes Expanded:", 0)
#         print("Nodes Generated:", nodes_generated)
#         print("Distance: infinity")
#         print("Route:")
#         print("None")

# if __name__ == "__main__":
#     if len(sys.argv) < 4 or len(sys.argv) > 5:
#         print("Usage: python find_route.py input_filename origin_city destination_city [heuristic_filename]")
#     else:
#         input_filename = sys.argv[1]
#         origin_city = sys.argv[2]
#         destination_city = sys.argv[3]
#         heuristic_filename = None if len(sys.argv) == 4 else sys.argv[4]
#         find_route(input_filename, origin_city, destination_city, heuristic_filename)

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
        explored = set()
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 0
        while frontier:
            cost, current_city, path = heapq.heappop(frontier)
            if current_city != destination:  # Check if the popped node is not the destination
                nodes_popped += 1
            if current_city == destination:
                return path, nodes_popped, nodes_expanded, nodes_generated
            if current_city not in explored:
                explored.add(current_city)
                nodes_expanded += 1
                if current_city in self.connections:
                    for neighbor, distance in self.connections[current_city]:
                        if neighbor not in explored:
                            new_cost = cost + distance
                            heapq.heappush(frontier, (new_cost, neighbor, path + [neighbor]))
                            nodes_generated += 1
        return None, nodes_popped, nodes_expanded, nodes_generated

    def informed_search(self, origin, destination):
        frontier = [(self.heuristic.get(origin, float('inf')), origin, [origin])]
        explored = set()
        nodes_popped = 0
        nodes_expanded = 0
        nodes_generated = 0
        while frontier:
            _, current_city, path = heapq.heappop(frontier)
            nodes_popped += 1
            if current_city == destination:
                return path, nodes_popped, nodes_expanded, nodes_generated
            if current_city not in explored:
                explored.add(current_city)
                nodes_expanded += 1
                if current_city in self.connections:
                    for neighbor, distance in self.connections[current_city]:
                        if neighbor not in explored:
                            new_cost = self.heuristic.get(neighbor, float('inf')) + distance
                            heapq.heappush(frontier, (new_cost, neighbor, path + [neighbor]))
                            nodes_generated += 1
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