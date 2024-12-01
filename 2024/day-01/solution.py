#!/usr/bin/env python


input_file = open("input", "r")
data=input_file.readlines()
input_file.close()

left = []
right = []
for l, r in [line.split() for line in data]:
    # There's an easier way to do this, I just can't think of it.
    left.append(int(l))
    right.append(int(r))

left.sort()
right.sort()

dist = sum(map(lambda l, r: abs(l-r), left, right))
sim = sum(map(lambda l: l * right.count(l), left))
print(f"Difference: {dist}")
print(f"Similarity: {sim}")
