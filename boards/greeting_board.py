import time
from .board import Board
import config

class GreetingBoard(Board):
    """
    Greeting board displayed on the LCD.
    """

    def __init__(self,
                position: tuple[int, int] = config.BOARD_DEFAULT_POSITION,
                size: tuple[int, int] = config.BOARD_DEFAULT_SIZE,
                data_provider = None,
                update_interval: int = config.BOARD_DEFAULT_UPDATE_INTERVAL,
                duration: int = config.BOARD_DEFAULT_DURATION):
            """
            Initializes the board.
            """
            super().__init__(position, size, data_provider, update_interval, duration)
            self.dot = 0

    def display(self, lcd, context):
        """
        Displays the greeting board on the LCD.

        :param lcd: the LCD object
        :param remaining_time: the remaining time in milliseconds
        """
        lcd.cursor_pos = self.position
        lcd.write_string("Hello, world!")
        lcd.cursor_pos = (self.position[0] + 1, self.position[1])
        lcd.write_string(f"thinking")
        return True

    def update(self, lcd, context):
        """
        Updates the greeting board on the LCD.

        :param lcd: the LCD object
        """
        lcd.cursor_pos = (self.position[0] + 1, self.position[1] + 8)
        lcd.write_string(f"{'.' * self.dot}")
        lcd.write_string(f"{' ' * (3 - self.dot)}")
        self.dot = (self.dot + 1) % 4
        lcd.cursor_pos = (self.position[0] + 3, self.position[1])
        lcd.write_string(f"{round(context['end_time'] - time.time())}s left")
        return True
    