#!/usr/bin/env python3

# TODO:
#   1. Gather the page numbers for an update.
#   2. Read ordering rules.
#     2a. Ignore rules for pages not in step 1.
#   3. Check page list from step 1 against page order from step 2.
#     3a. Keep only the page number lists that are properly ordered.
#   4. Collect "middle" pages from step 3a.
#   5. Sum the middle page numbers from step 4.

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

# For each page list, process the ordering instructions and verify the page list is in the correct order.
# If the page list is in order, get the middle number.
# Sum all middle numbers


def parse_ordering(pages: list, instructions: list[tuple]) -> list:
    output = []

    for x, y in instructions:
        if x in pages and y in pages:
            # The instruction refers to pages in the update. Include them in the final ordering.
            if y not in output:
                # Y isn't in the final order rules, append it to the end
                output.append(y)

            if x not in output:
                # X isn't in the final order rules, Insert it before Y.
                output.insert(output.index(y), x)
            elif output.index(x) > output.index(y):
                # X is present in the final output, but it's past Y. Move it to Y's location.
                output.remove(x)
                output.insert(output.index(y), x)

    return output


def parse_input(s: list[str]) -> tuple:
    parse_instructions = True
    instructions = []
    updates = []

    for line in s:
        line = line.strip()
        if line == "":
            parse_instructions = False
            continue

        if parse_instructions:
            x, y = line.split("|")
            instructions.append((int(x),int(y)))
            continue
        updates.append(list(map(int, line.split(","))))

    return instructions, updates


def main():
    with open("input", "r") as input_file:
        data = input_file.readlines()

    instructions, updates = parse_input(TEST_INPUT.splitlines())
    # instructions, updates = parse_input(data)

    middle_sums = 0
    for update in updates:
        final_order = parse_ordering(update, instructions)
        if final_order == update:
            middle = update[len(update)//2]
            print(f"Page order: {update}, {middle}")
            middle_sums += middle
    print(f"Sums: {middle_sums}")


main()
