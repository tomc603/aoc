#!/usr/bin/env python3

TEST_INPUT="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def operate(fields: list, value: int, target: int) -> bool:
    """
    Compute the possible values for a list of numbers from left to right (not PEMDAS), and compare to the target value
    :param fields: List of numbers to operate with
    :param value: The current accumulated value from previous rounds
    :param target: Final desired value
    :return: True if the numbers in fields can achieve the target value
    """
    if len(fields) == 0:
        return value == target

    if value > 0:
        left, right = value, fields[0]
        fields = fields[1:]
    else:
        left, right = fields[0], fields[1]
        fields = fields[2:]

    intermediate = left * right
    if operate(fields, intermediate, target): return True

    intermediate = left + right
    if operate(fields, intermediate, target): return True

    intermediate = int(str(left) + str(right))
    if operate(fields, intermediate, target): return True


def main():
    # data = TEST_INPUT.split("\n")
    with open("input", "r") as input_file:
        data = input_file.read().split("\n")

    sums = 0
    print("")
    for line in data:
        if line == "":
            continue

        try:
            values = line.split(":")
            target = int(values[0])
            numbers = list(map(int, values[1].split()))

            if operate(numbers, 0, target):
                sums += target
        except ValueError as ex:
            print(f"Line {line} [{values}] is invalid. {ex}")
            continue

    # Part 1: 2654749936343
    # Part 2: 124060392153684
    print(f"Calibration result: {sums}")


main()
