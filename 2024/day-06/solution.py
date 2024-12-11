#!/usr/bin/env python3

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


def move_guard(grid: list) -> list[tuple[int, int]]:
    """
    Walk the specified grid, returning the traversed path when we reach the edge of the grid.

    :param grid: A list of a list of characters representing the floor plan of the lab
    :return: List of row, column pairs traversed in the lab
    """
    cur_row, cur_col = find_avatar(grid)
    guard = grid[cur_row][cur_col]
    direction = avatar_to_direction(guard)
    rows = len(grid)
    cols = len(grid[0])
    positions = list()

    while True:
        # Shorthand variables to clarity
        next_row = cur_row + direction[0]
        next_col = cur_col + direction[1]
        # guard = direction_to_avatar(direction)

        # If we're outside the bounds, break out of the loop and return the list of positions
        if not (0 <= cur_row < rows and 0 <= cur_col < cols):
            return positions

        # Check the next space in the current direction for an in-bounds obstacle
        if next_row < rows and next_col < cols and grid[next_row][next_col] == "#":
            direction = choose_direction(direction)
            continue

        positions.append((cur_row, cur_col))
        cur_row += direction[0]
        cur_col += direction[1]


def main():
    grid = []

    # data = TEST_INPUT.splitlines()
    with open("input", "r") as input_file:
        data = input_file.readlines()
    for line in data:
        grid.append(list(line.strip()))

    positions = move_guard(grid)
    print(f"Number of unique positions visited: {len(set(positions))}")


main()
