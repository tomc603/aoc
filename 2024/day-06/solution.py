#!/usr/bin/env python3
import copy

# Overview:
# Move the guard through the grid until they reach an edge
# If the guard reaches an obstacle, they turn 90 degrees right


TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
TEST_POSITIONS = 41


# Everything is in up, right, down, left order
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
AVATARS = ["^", ">", "v", "<"]


def avatar_to_direction(avatar: str) -> tuple[int,int]:
    """
    Convert the guard's avatar into a direction tuple.

    :param avatar: Character describing which direction the guard is facing
    :return: Tuple of row, column direction values
    """
    return DIRECTIONS[AVATARS.index(avatar)]


def direction_to_avatar(direction: tuple[int, int]) -> str:
    """
    Convert a direction value into a character describing the guard's direction.

    :param direction: Tuple of row, column direction values
    :return: Character depicting the direction the guard is facing
    """
    return AVATARS[DIRECTIONS.index(direction)]


def find_avatar(grid: list) -> tuple[int, int]:
    """
    Find the guard's avatar in the grid's characters.

    :param grid: Layout of the map data
    :return: Guard's row, col position in the map
    """
    for i in range(len(grid)):
        for a in AVATARS:
            try:
                j = grid[i].index(a)
                return i, j
            except ValueError:
                pass
        # for j in range(len(grid[0])):
        #     if grid[i][j] in AVATARS:
        #         return i, j

    # There is no avatar on the grid, this is an error
    # By returning -1, -1 the guard will start outside the bounds of the grid
    # which will result in an empty position list
    return -1, -1


def choose_direction(current: tuple[int, int]) -> tuple[int, int]:
    """
    Rotate the guard's direction clockwise.

    :param current: The current direction value for the guard
    :return: Tuple containing the next direction value for the guard
    """
    return DIRECTIONS[(DIRECTIONS.index(current) + 1) % len(DIRECTIONS)]


def get_path(grid: list) -> set[tuple[int, int]]:
    """
    Walk the specified grid, returning the traversed path when we reach the edge of the grid.

    :param grid: A list of a list of characters representing the floor plan of the lab
    :return: Set of row, column pairs traversed in the lab
    """
    cur_row, cur_col = find_avatar(grid)
    guard = grid[cur_row][cur_col]
    direction = avatar_to_direction(guard)
    rows = len(grid)
    cols = len(grid[0])
    positions = set()

    while True:
        # Shorthand variables to clarity
        next_row = cur_row + direction[0]
        next_col = cur_col + direction[1]
        # guard = direction_to_avatar(direction)

        # If we're outside the grid bounds, return the list of positions
        if not (0 <= cur_row < rows and 0 <= cur_col < cols):
            return positions

        # Check the next space in the current direction for an in-bounds obstacle
        if next_row < rows and next_col < cols and grid[next_row][next_col] == "#":
            direction = choose_direction(direction)
            continue

        # Add the current position to the visited positions
        positions.add((cur_row, cur_col))
        cur_row = next_row
        cur_col = next_col


def will_loop(grid: list[list[str]], obs_row, obs_col) -> bool:
    """
    Place an obstacle at the specified row, col position, then walk the grid checking for loops

    :param grid: Lab floor plan to walk
    :param obs_row: New obstacle row position
    :param obs_col: New obstacle column position
    :return: True if a loop is detected, otherwise false.
    """
    # Make a copy of the original grid to operate on
    test_grid = copy.deepcopy(grid)

    cur_row, cur_col = find_avatar(test_grid)
    direction = avatar_to_direction(test_grid[cur_row][cur_col])
    rows = len(test_grid)
    cols = len(test_grid[0])

    # We can't modify the guard's position or they'll notice the paradox
    if (obs_row, obs_col) == (cur_row, cur_col):
        return False

    # If the target already has an obstacle, modifying it won't cause a loop
    if test_grid[obs_row][obs_col] == "#":
        return False

    # Place the new obstacle in the lab floor plan.
    test_grid[obs_row][obs_col] = "#"

    seen = set()
    while True:
        # Shorthand variables to clarity
        next_row = cur_row + direction[0]
        next_col = cur_col + direction[1]

        # If we've already visited this location in the same direction, we're in a loop
        if (cur_row, cur_col, direction) in seen:
            return True

        # Add the current location and heading to the visited set
        seen.add((cur_row, cur_col, direction))

        # If we're outside the grid bounds, we haven't found a loop
        if not (0 <= next_row < rows and 0 <= next_col < cols):
            return False

        # Check the next space in the current direction for an in-bounds obstacle
        if test_grid[next_row][next_col] == "#":
            direction = choose_direction(direction)
            continue

        # Move to the next location
        cur_row = next_row
        cur_col = next_col


def main():
    grid = []

    # data = TEST_INPUT.splitlines()
    with open("input", "r") as input_file:
        data = input_file.readlines()
    for line in data:
        grid.append(list(line.strip()))

    positions = get_path(grid)
    # Part 1: 4939
    print(f"Number of unique positions visited: {len(positions)}")

    # Part 2: 1434
    count = 0
    for position in positions:
        count += will_loop(grid, position[0], position[1])
    print(f"Loops: {count}")


main()
