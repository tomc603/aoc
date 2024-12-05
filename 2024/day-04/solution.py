#!/usr/bin/env python3

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


def find_str(grid, match: str) -> int:
    """
    Find a string in a two-dimensional array of characters in any of the 8 possible directions.
    The string may be forwards of backwards.
    :param grid: two-dimensional array to search
    :param match: string value to search for
    :return: Number of instances of the search string found in the grid
    """
    count = 0
    rows = len(grid)
    cols = len(grid[0]) - 1
    match_len = len(match)
    bidi_match = [match, match[::-1]]

    for row in range(rows):
        for col in range(cols):
            right, down, right_diag, left_diag = "", "", "", ""

            for i in range(match_len):
                if col+i < cols: right += grid[row][col+i]
                if row+i < rows: down += grid[row+i][col]
                if row+i < rows and col+i < cols: left_diag += grid[row+i][col+i]
                if row + i < rows and (col+match_len) - (i+1) < cols: right_diag += grid[row+i][(col+match_len) - (i + 1)]

            if right in bidi_match: count += 1
            if down in bidi_match: count +=1
            if left_diag in bidi_match: count += 1
            if right_diag in bidi_match: count += 1

    return count


def find_xmas(grid) -> int:
    """
    Find "XMAS" forwards and backwards in an X pattern
    :param grid:
    :return:
    """
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
            ): count += 1

    return count


with open("input", "r") as input_file:
    data = input_file.readlines()

part1_recursive = search(data, MATCH_STRING)
print(f"Part 1 recursive: {part1_recursive}")

part1_forward = find_str(data, MATCH_STRING)
print(f"Part 1 non-recursive: {part1_forward}")

part2_count = find_xmas(data)
print(f"Part 2: {part2_count}")
