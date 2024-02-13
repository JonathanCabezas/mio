BOX = """\
┌─┐
│ │
└─┘
"""

TOP_LEFT_CORNER = BOX[0]
HORIZONTAL_BAR = BOX[1]
TOP_RIGHT_CORNER = BOX[2]
VERTICAL_BAR = BOX[4]
BOTTOM_LEFT_CORNER = BOX[8]
BOTTOM_RIGHT_CORNER = BOX[10]


def enclose(title, *args):
    title = f"{VERTICAL_BAR} {title} {VERTICAL_BAR}"
    total_len = len(title.format(*args))
    horizontal_enclosure = HORIZONTAL_BAR * (total_len - 2)
    return [
        (f"{TOP_LEFT_CORNER}{horizontal_enclosure}{TOP_RIGHT_CORNER}",),
        (title, *args),
        (f"{BOTTOM_LEFT_CORNER}{horizontal_enclosure}{BOTTOM_RIGHT_CORNER}",),
    ]
