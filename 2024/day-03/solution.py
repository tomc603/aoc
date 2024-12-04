#!/usr/bin/env python3

import re
from operator import mul

TEST="xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
instruction_re = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', flags=re.MULTILINE)


def parse_instructions(instructions: str) -> int:
    """
    Parse valid multiplication commands from the input data, and sum their products.
    :param instructions: Textual instruction input
    :return: Sum of instruction products
    """
    instructions = instruction_re.findall(instructions)

    return sum([mul(int(instruction[0]), int(instruction[1])) for instruction in instructions])


with open("input", "r") as input_file:
    data = input_file.read()

# Execute the instructions
part1 = parse_instructions(data)

# Remove instruction segments between "don't()" and "do()"
while True:
    begin = data.find("don't()")
    if begin < 0:
        # There are no stop commands, so everything remaining needs to be multiplied.
        break

    end = data.find("do()", begin)
    if end < 0:
        # There is no resuming command, so no other instructions matter.
        data = data[:begin]
        break

    data = data[:begin] + data[end + 4:]


# Execute the remaining instructions
part2 = parse_instructions(data)

print(f"Part 1 Sum: {part1}")
print(f"Part 2 Sum: {part2}")
