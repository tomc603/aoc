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


def map_grid(grid: list[list[str]]) -> defaultdict[list[tuple[int, int]]]|None:
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
    antinodes = set()
    for antenna in antennas:
        for a, b in itertools.combinations(antennas[antenna], 2):
            distance = (a[0] - b[0], a[1] - b[1])

            x, y = (a[0] + distance[0], a[1] + distance[1])
            if 0<= x < rows and 0 <= y < cols:
                antinodes.add((x, y))

            x, y = (b[0] - distance[0], b[1] - distance[1])
            if 0<= x < rows and 0 <= y < cols:
                antinodes.add((x, y))

    # Debugging: Print the grid with antinodes
    # for antinode in antinodes:
    #     if grid[antinode[0]][antinode[1]] == ".":
    #         grid[antinode[0]][antinode[1]] = "#"
    # for row in grid:
    #     print(f"{row}")

    # Part 1: 327
    print(f"\nAntinodes: {len(antinodes)}")


main()
