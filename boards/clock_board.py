import time
from .board import Board
from icons.manager import IconManager
import icons.icons as icons
from utils.common_utils import write_icon, get_progress_percent


class ClockBoard(Board):
    """
    Clock board displayed on the LCD.
    """

    def display(self, lcd, context):
        """
        Displays the clock board on the LCD.

        :param lcd: the LCD object
        """
        lcd.cursor_pos = self.position
        lcd.write_string(f"{IconManager.use_icon(lcd, icons.CLOCK)} Current Time")
        return True

    def update(self, lcd, context):
        """
        Updates the clock board on the LCD.

        :param lcd: the LCD object
        """
        lcd.cursor_pos = (self.position[0] + 2, self.position[1])
        data = self.data_provider.get_data()
        lcd.write_string(data["time"])
        write_icon(lcd, icons.DOOR_2X2, (self.position[0] + 1, self.position[1] + 17))
        if "board_common_data" in context:
            context["board_common_data"]["progress"] = get_progress_percent(
                context["start_time"], time.time(), context["end_time"]
            )

        return True
