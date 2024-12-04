#!/usr/bin/env python3

import re
from operator import mul

TEST="xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


data = open("input", "r").read()
instruction_re = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
instructions = instruction_re.findall(data)

results = sum([mul(int(instruction[0]), int(instruction[1])) for instruction in instructions])
print(f"Sum: {results}")
