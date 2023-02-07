import math
import re


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def haversine(city1, city2):
    pass


def readFile(name):
    cities = []
    with open(name, 'r') as f:
        lines = f.readlines()

        for line in lines:
            # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
            # https://stackoverflow.com/questions/15879810/python-splitting-a-complex-string-including-parentheses-and
            # take the input from a txt and split it in a list if it contains "- ( ) \n :"
            city_info = list(filter(None, re.split('-|,|\n|[(]|[)]|:', line)))

            # print(f'{city_destination}')
            cities.append(city_info)

    print(f'{cities}')
    return cities


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    cityCoordinates = {}
    coordinates = readFile('coordinates.txt')
    for city in coordinates:
        cityCoordinates[city[0]] = [float(city[1]), float(city[2])]

    print(cityCoordinates)
    print('==========================')


    cityMap = {}
    mapFile = readFile('map.txt')
    for city in mapFile:
        connectedCities = []
        for i in range(1, len(city), 2):
            connectedCities.append([city[i], float(city[i + 1])])
        cityMap[city[0]] = connectedCities

    print(cityMap)
