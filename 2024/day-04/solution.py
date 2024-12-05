#!/usr/bin/env python3
import itertools

MATCH_STRING = "XMAS"
MATCH_LENGTH = len(MATCH_STRING)

ORDINALS = [-1, 0, 1]

TEST_STRING = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

TEST_MATCHES = 18


def match_word(grid, rows, cols, match, idx, x_pos, y_pos, x_dir, y_dir) -> bool:
    """
    Recursively search the grid in the direction specified for the specified value
    :param grid: two-dimensional array to search
    :param rows: Number of rows remaining to search
    :param cols: Number of columns remaining to search
    :param match: string value to search for
    :param idx: Current character of match to search for
    :param x_pos: Row position to search for the idx'th character of the search string
    :param y_pos: Column position to search for the idx'th character of the search string
    :param x_dir: Row direction to search for the search string (-1, 0, 1)
    :param y_dir: Column direction to search for the search string (-1, 0, 1)
    :return: Boolean value of search success or failure
    """

    # The search string index has reached the length of the search string
    # We successfully found the entire search string
    if idx == len(match):
        return True

    # If we are within the grid boundaries and we currently have a matching character,
    # continue the search at the next (row, column) pair, in the current search direction
    # for the next character in the search string
    if 0 <= x_pos < rows and 0 <= y_pos < cols and match[idx] == grid[x_pos][y_pos]:
        return match_word(grid, rows, cols, match, idx + 1, x_pos + x_dir, y_pos + y_dir, x_dir, y_dir)

    # We don't have a matching character, and we haven't exhausted the search string
    return False


def search(grid, match) -> int:
    """
    Iteratively call the match_word function for every search direction for every (row, column) in the grid
    :param grid: two-dimensional array to search
    :param match: string value to search for
    :return: Number of instances of the search string found in the grid
    """
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == match[0]:
                for x_dir, y_dir in [(x,y) for x in ORDINALS for y in ORDINALS if (x,y) != (0,0)]:
                    if match_word(grid, rows, cols, match, 0, row, col, x_dir, y_dir):
                        count += 1

    return count

def find_xmas(grid) -> int:
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows - 2):
        for col in range(cols - 2):
            left_diagonal = grid[row][col] + grid[row+1][col+1] + grid[row+2][col+2]
            right_diagonal = grid[row][col+2] + grid[row+1][col+1] + grid[row+2][col]
            if (
                    (left_diagonal == "MAS" or left_diagonal == "SAM") and
                    (right_diagonal == "MAS" or right_diagonal == "SAM")
            ):
                count += 1

    return count


with open("input", "r") as input_file:
    data = input_file.readlines()

part1_count = search(data, MATCH_STRING)
print(f"Part 1: {part1_count}")

part2_count = find_xmas(data)
print(f"Part 2: {part2_count}")
