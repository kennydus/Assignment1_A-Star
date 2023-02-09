import sys
import math
import re


class CityNode:
    def __init__(self, name):
        self.name = name
        self.g_score = math.inf  # Cost so far to reach current city
        self.h_score = math.inf  # Straight line distance to destination city
        self.f_score = math.inf  # Estimated total cost of path to destination city
        self.previous = None


# Make sure the inputs are objects from cityCoordinates list.
def haversine(city1, city2):
    # Radius of the earth (miles)
    r = 3958.8

    # Radian coordinates for first city.
    c1_lat_rad = math.radians(city1[0])
    c1_long_rad = math.radians(city1[1])

    # Radian coordinates for second city.
    c2_lat_rad = math.radians(city2[0])
    c2_long_rad = math.radians(city2[1])

    # Straight line distance
    distance = 2 * r * math.asin(math.sqrt(math.sin((c2_lat_rad - c1_lat_rad) / 2) ** 2 + 
                                            (math.cos(c1_lat_rad) * math.cos(c2_lat_rad) * 
                                            math.sin((c2_long_rad - c1_long_rad) / 2) ** 2)))

    return distance


def read_file(name):
    cities = []
    with open(name, 'r') as f:
        lines = f.readlines()

        for line in lines:
            # Takes input from a text file and splits it into a list using "- , \n ( ) :" as delimiters.
            city_info = list(filter(None, re.split('-|,|\n|[(]|[)]|:', line)))
            cities.append(city_info)
    return cities


def a_star(dep_city_name, arr_city_name, city_nodes):
    unexplored_cities = []
    visited_cities = []

    # Initializing departing city node's values
    dep_city_node = city_nodes[dep_city_name]
    dep_city_node.g_score = 0
    dep_city_node.h_score = haversine(cityCoordinates[dep_city_name], cityCoordinates[arr_city_name])
    dep_city_node.f_score = dep_city_node.g_score + dep_city_node.h_score

    unexplored_cities.append(dep_city_node)

    while len(unexplored_cities) > 0:
        # Sort the unexplored_cities array so that we will pop the node with the lowest f_score.
        unexplored_cities.sort(key=lambda x: x.f_score)
        current_node = unexplored_cities.pop(0)
        for neighbor in cityMap[current_node.name]:
            # Creating neighbor node, referencing from city_nodes dictionary.
            neighbor_node = city_nodes[neighbor[0]]
            g_score = current_node.g_score + neighbor[1]
            h_score = haversine(cityCoordinates[neighbor_node.name], cityCoordinates[arr_city_name])
            f_score = g_score + h_score

            if f_score < neighbor_node.f_score:
                neighbor_node.previous = current_node
                neighbor_node.f_score = f_score
                neighbor_node.g_score = g_score
                neighbor_node.h_score = h_score

            if neighbor_node not in (visited_cities or unexplored_cities):
                unexplored_cities.append(neighbor_node)
        visited_cities.append(current_node)
        
        # If the current node is the arrival city, that means that we have found the shortest path
        # since we pop the node with the lowest f-score.
        if current_node.name == arr_city_name:
            break


# Creates an array of city names (strings) that shows the order of the path
# taken to get from the arrival city to the destination city.
def get_path(dest_city_node):
    path = []
    current_city_node = dest_city_node
    path.append(current_city_node.name)

    # First appends the arrival city name and keeps appending the previous city's name
    # until it reaches the departing city's name. The departing city does NOT have a 
    # previous city, and the loop will stop once it is added.
    while current_city_node.previous is not None:
        path.append(current_city_node.previous.name)
        current_city_node = current_city_node.previous

    return path


if __name__ == '__main__':

    # Create cityCoordinates, which is a dictionary using the city's name as a key, 
    # and an array of its coordinates as the key's value.
    cityCoordinates = {}
    coordinates_file = read_file('coordinates.txt')
    for city in coordinates_file:
        cityCoordinates[city[0]] = [float(city[1]), float(city[2])]

    # Create cityMap, which is a dictionary using the city as a key, and an array
    # of its neighboring cities with the distance to them as the key's value.
    cityMap = {}
    mapFile = read_file('map.txt')
    for city in mapFile:
        connectedCities = []
        for i in range(1, len(city), 2):
            # Each connected city's name and distance
            connectedCities.append([city[i], float(city[i + 1])])
        cityMap[city[0]] = connectedCities

    # Dictionary of cities as CityNodes.
    city_node_dict = {}
    # Create each city node, getting their names from the cityCoordinates dictionary. 
    for city in cityCoordinates:
        city_node_dict[city] = CityNode(city)

    departure_city = sys.argv[1]
    destination_city = sys.argv[2]
    if departure_city not in cityCoordinates.keys() or destination_city not in cityCoordinates.keys():
        sys.exit("""\t=======================================================
        ERROR: Departure/Destination city inputted incorrectly.
        =======================================================""")
        # print('==============================')
        # print('ERROR: Departure/Destination city inputted incorrectly.')
        # print('==============================')
        # break
    
    print('From city:', departure_city)
    print('To city:', destination_city)

    a_star(departure_city, destination_city, city_node_dict)

    path = get_path(city_node_dict[destination_city])
    print('Best Route: ', end='')
    while len(path) > 1:
        print(path.pop(), '- ', end='')
    # Print destination city outside of the loop to avoid printing an extra '-'.
    print(path.pop())

    print(f'Total distance: {city_node_dict[destination_city].g_score: .2f} mi')
