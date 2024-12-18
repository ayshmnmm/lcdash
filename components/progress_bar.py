from boards.board import Board
import config
from icons.dynamic_icons import rectangle_icon, spinner_border
from icons.manager import IconManager


class ProgressSpinner(Board):
    def __init__(
        self,
        position=config.BOARD_DEFAULT_POSITION,
        size=config.BOARD_DEFAULT_SIZE,
        update_interval=config.BOARD_DEFAULT_UPDATE_INTERVAL,
        duration=config.BOARD_DEFAULT_DURATION,
        width=1,
        reverse=False,
    ):
        """
        Initialize a rectangular progress spinner. Progress is calculated on the context dictionary with the key "progress".
        The value of "progress" should be a percentage value between 0 and 100.

        :param position: the position of progress bar on the LCD
        :param size: the size of the progress bar (rows, columns)
        :param update_interval: the update interval for the progress bar
        :param duration: the duration of the progress bar
        :param width: the width of the progress bar
        :param reverse: the direction of the progress bar
        """
        super().__init__(position, size, None, update_interval, duration)
        self.width = width
        self.cell_height = 8
        self.prev_icon = None

    def display(self, lcd, context):
        """
        Display the progress bar on the LCD.

        :param lcd: the LCD object
        :param context: the context dictionary
        """
        return True

    def update(self, lcd, context):
        """
        Update the progress bar on the LCD.

        :param lcd: the LCD object
        :param context: the context dictionary
        """
        # check for progress in context if not then in context["board_common_data"] and if not then 0
        progress_percentage = int(context.get("progress", context.get("board_common_data", {}).get("progress", 0)))
        lcd.cursor_pos = self.position
        total_height = self.size[0]*self.cell_height
        # lcd.write_string(f"{progress_percentage}")
        scaled_progress = round((progress_percentage / 100) * (23))
        big_cells, small_cell = divmod(scaled_progress, self.cell_height)
        # print(f"big_cells: {big_cells}, small_cell: {small_cell} for progress: {progress_percentage} ({scaled_progress})")
        # for i in range(big_cells):
        #     lcd.cursor_pos = (self.position[0] + i, self.position[1])
        #     lcd.write_string(IconManager.use_icon(lcd, rectangle_icon(self.cell_height, self.width, h_align="left", v_align="top")))
        # if small_cell>2:
        #     lcd.cursor_pos = (self.position[0] + big_cells, self.position[1])
        #     lcd.write_string(IconManager.use_icon(lcd, rectangle_icon(small_cell, self.width, h_align="left", v_align="top")))
        if self.prev_icon is not None:
            IconManager.clear_icon(self.prev_icon)
        lcd.write_string(IconManager.use_icon(lcd, spinner_border(scaled_progress)))
        self.prev_icon = spinner_border(scaled_progress)
        return True
