#!/usr/bin/env python3

import itertools
from collections import defaultdict

TEST_INPUT="""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

TEST_LOCATIONS=14


def map_grid(grid: list[list[str]]) -> defaultdict[list]:
    """
    Walk the grid area searching for antenna frequencies.
    :param grid: The city play, with antenna locations
    :return: Dictionary of locations by frequency
    """
    antennas = defaultdict(list)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            frequency = grid[i][j]
            if not frequency == ".":
                antennas[frequency].append((i, j))

    return antennas


def main():
    # data = TEST_INPUT.strip().split("\n")
    data = open("input", "r").read().strip().split("\n")

    grid = []
    for line in data:
        grid.append(list(line))

    rows = len(grid)
    cols = len(grid[0])
    antennas = map_grid(grid)

    # Debugging: Print antenna sites
    # for antenna in antennas:
    #     print(f"{antenna}: {antennas[antenna]}")

    antinodes = set()
    for antenna in antennas:
        for a, b in itertools.combinations(antennas[antenna], 2):
            # For part 2, antipoles extend to the end of the grid
            # and include antenna sites
            slope = (b[0] - a[0], b[1]-a[1])

            # Add the antenna sites themselves
            antinodes.add(a)
            antinodes.add(b)

            # Negative slope
            (x, y) = (a[0] - slope[0], a[1] - slope[1])
            while True:
                if not (0<= x < rows and 0 <= y < cols):
                    break
                if grid[x][y] == "." or grid[x][y] == antenna:
                    antinodes.add((x, y))
                    grid[x][y] = "#"
                (x, y) = (x - slope[0], y - slope[1])

            # Positive slope
            (x, y) = (b[0] + slope[0], b[1] + slope[1])
            while True:
                if not (0<= x < rows and 0 <= y < cols):
                    break
                if grid[x][y] == "." or grid[x][y] == antenna:
                    antinodes.add((x, y))
                    grid[x][y] = "#"
                (x, y) = (x + slope[0], y + slope[1])

    # Debugging: Print the grid with antinodes
    # for antinode in antinodes:
    #     if grid[antinode[0]][antinode[1]] == ".":
    #         grid[antinode[0]][antinode[1]] = "#"
    for row in grid:
        print(f"{row}")

    # Part 1: 327
    # Part 2: 1233
    print(f"Antinodes: {len(antinodes)}")


main()
