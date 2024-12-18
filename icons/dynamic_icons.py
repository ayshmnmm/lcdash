def rectangle_icon(
    height: int, width: int, h_align: str = "center", v_align: str = "center"
) -> tuple:
    """
    Generate a rectangular icon with given height, width, horizontal, and vertical alignment.

    :param height: The height of the rectangle (1-8).
    :param width: The width of the rectangle (1-8).
    :param h_align: Horizontal alignment of the rectangle ('left', 'center', 'right').
    :param v_align: Vertical alignment of the rectangle ('top', 'center', 'bottom').
    :return: A tuple representing the 8x8 bitmap of the icon.
    """
    if height > 8 or width > 8:
        raise ValueError("Height and width must be between 1 and 8.")

    # Calculate horizontal alignment
    if h_align == "left":
        h_shift = 0
    elif h_align == "center":
        h_shift = (8 - width) // 2
    elif h_align == "right":
        h_shift = 8 - width
    else:
        raise ValueError("h_align must be 'left', 'center', or 'right'.")

    # Calculate vertical alignment
    if v_align == "top":
        v_shift = 0
    elif v_align == "center":
        v_shift = (8 - height) // 2
    elif v_align == "bottom":
        v_shift = 8 - height
    else:
        raise ValueError("v_align must be 'top', 'center', or 'bottom'.")

    # Build the icon row by row
    icon = []
    for row in range(8):
        if v_shift <= row < v_shift + height:
            # Create a row with the rectangle's width, shifted based on horizontal alignment
            row_bits = (0b1 << width) - 1  # Create `width` bits of 1s
            icon.append(row_bits << h_shift)
        else:
            # Empty row outside the rectangle's height
            icon.append(0b00000000)

    return tuple(icon)

    # def spinner_border(steps: int) -> tuple:
    """
    Generate a spinner icon that lights up cells along the border in a clockwise direction.

    :param steps: Number of cells to light up along the border (0 to 28).
    :return: A tuple representing the 8x8 bitmap of the icon.
    """
    if steps < 0 or steps > 28:
        raise ValueError("Steps must be between 0 and 28.")

    # Initialize an empty 8x8 grid
    grid = [[0 for _ in range(8)] for _ in range(8)]

    # Define the border positions in clockwise order
    border_positions = (
        [(0, i) for i in range(8)]
        + [(i, 7) for i in range(1, 8)]  # Top row (left to right)
        + [(7, i) for i in range(6, -1, -1)]  # Right column (top to bottom)
        + [  # Bottom row (right to left)
            (i, 0) for i in range(6, 0, -1)
        ]  # Left column (bottom to top)
    )

    # Light up the border based on the steps
    for i in range(steps):
        x, y = border_positions[i]
        grid[x][y] = 1

    # Convert the grid to a tuple of bitmaps
    return tuple(int("".join(map(str, row)), 2) for row in grid)


def spinner_border(steps: int) -> tuple:
    """
    Generate a spinner icon that lights up cells along the border of an 8x5 grid in a clockwise direction.

    :param steps: Number of cells to light up along the border (0 to 24).
    :return: A tuple representing the 8x5 bitmap of the icon.
    """
    if steps < 0:
        raise ValueError("Steps must be a non-negative integer.")
    if steps > 22:
        steps = 22

    # Initialize an empty 8x5 grid
    grid = [[0 for _ in range(5)] for _ in range(8)]

    # Define the border positions in clockwise order
    border_positions = (
        [(0, i) for i in range(5)]
        + [(i, 4) for i in range(1, 8)]  # Top row (left to right)
        + [(7, i) for i in range(3, -1, -1)]  # Right column (top to bottom)
        + [  # Bottom row (right to left)
            (i, 0) for i in range(6, 0, -1)
        ]  # Left column (bottom to top)
    )

    # Light up the border based on the steps
    for i in range(steps):
        x, y = border_positions[i]
        grid[x][y] = 1

    # Convert the grid to a tuple of bitmaps
    return tuple(int("".join(map(str, row)), 2) for row in grid)
