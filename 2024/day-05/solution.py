#!/usr/bin/env python3

from _collections import defaultdict


TEST_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def valid(pages: list, instructions: dict) -> bool:
    for i in range(len(pages)):
        # Get an index into the current page as the instructions key.
        for j in range(i + 1, len(pages)):
            # Get the following page as a value in the instructions
            if pages[j] not in instructions[pages[i]]:
                # The next page in the update sequence doesn't match the instruction set
                return False

    # All pages are in order of the instructions
    return True


def parse_input(s: list[str]) -> tuple:
    parse_instructions = True
    instructions = defaultdict(set)
    updates = []

    for line in s:
        line = line.strip()
        if line == "":
            parse_instructions = False
            continue

        if parse_instructions:
            x, y = map(int, line.split("|"))
            instructions[x].add(y)
            continue
        updates.append(list(map(int, line.split(","))))

    return instructions, updates


def repair_update(update: list, instructions: defaultdict[list]) -> list:
    update_rules = defaultdict(set)

    # Build a rule set for the pages in this update
    for page in update:
        # Filter for the intersecting page from the rules
        update_rules[page] = instructions[page] & set(update)

    # Sort the page order using the filtered rules
    repaired_order = sorted(update_rules, key=lambda k: len(update_rules[k]), reverse=True)

    return repaired_order


def main():
    with open("input", "r") as input_file:
        data = input_file.readlines()

    # instructions, updates, d = parse_input(TEST_INPUT.splitlines())
    instructions, updates = parse_input(data)

    part1_sum = 0
    part2_sum = 0
    for update in updates:
        if valid(update, instructions):
            part1_sum += update[len(update)//2]
        else:
            repaired = repair_update(update, instructions)
            part2_sum += repaired[len(repaired)//2]

    print(f"Part 1: {part1_sum}")
    print(f"Part 2: {part2_sum}")


main()
