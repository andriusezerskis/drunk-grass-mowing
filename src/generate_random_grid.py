# Generate a random grid with the specified width and height
"""
example grid:
8
8
-
-0.5 -0.4 -0.4 -0.3 -0.3 -0.2 -0.2 -0.2
-0.5 -0.4 -0.4 -0.3 -0.3 -0.2 -0.2 -0.2
-0.5 -0.4 -0.4 -0.3 -0.3 -0.3 -0.4 -0.3
-0.65 -0.6 -0.4 -0.4 -0.5 -0.4 -0.4 -0.4
-0.6 -0.6 -0.4 -0.5 -0.5 -0.5 -0.6 -0.6
-0.7 -0.7 -0.6 -0.6 -0.6 -0.6 -0.6 -0.6
-0.7 -0.8 -0.7 -0.7 -0.6 -0.6 -0.7 -0.5
-0.8 -0.7 -0.8 -0.9 -0.7 -0.7 -0.6 -0.5
-
- - - - - - - -
- - A - - - - -
- - - A - A A -
- - A A - - A -
- - A A - - - -
- - - - - - - -
- - C - F - - -
- - C - F - - -

-----

first is width, second is height, then a blank line,
then height lines of width float numbers (heights between -1 and 1),
then a blank line, then height lines of width symbols ( - for no entity, or the symbol of an entity)

"""

import random

width = 500
height = 500

# create file if not exists
with open("../assets/grids/test_sid.map", "w") as f:
    f.write(f"{height}\n")
    f.write(f"{width}\n")
    f.write("-\n")
    for y in range(height):
        line = []
        for x in range(width):
            # h = random.uniform(-1, 1)
            h = 0.5
            line.append(f"{h:.2f}")
        f.write(" ".join(line) + "\n")
    f.write("-\n")
    for y in range(height):
        line = []
        for x in range(width):
            r = random.random()
            # if r < 0.05:
            #     line.append("A")
            # elif r < 0.08:
            #     line.append("C")
            # elif r < 0.1:
            #     line.append("F")
            # elif r < 0.15:
            #     line.append("H")
            # else:
            line.append("-")
        f.write(" ".join(line) + "\n")