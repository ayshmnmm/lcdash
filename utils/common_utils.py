from icons.manager import IconManager


def write_icon(lcd, icon, position):
    """Write an icon to the LCD. Includes support for larger icons spanning multiple cells.
    Icons spanning multiple cells are defined as a 2D list of cells, where each cell is an icon bitmap.

    :param lcd: the LCD object
    :param icon: the icon to write
    :param position: the position to write the icon to
    """
    # 2D list of cells
    for i, row in enumerate(icon):
        lcd.cursor_pos = (position[0] + i, position[1])
        for j, cell in enumerate(row):
            lcd.cursor_pos = (position[0] + i, position[1] + j)
            lcd.write_string(IconManager.use_icon(lcd, cell))

def get_progress_percent(start_time, current_time, end_time=None, duration=None):
    """Get the progress percentage between the start and end times. Either the end time or the duration must be provided.

    :param start_time: the start time
    :param current_time: the current time
    :param end_time: the end time
    :param duration: the duration
    :return: the progress percentage
    """
    duration = duration or end_time - start_time
    return (current_time - start_time) / duration * 100
