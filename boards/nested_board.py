from typing import Iterable
from boards.board import Board
import config


class NestedBoard(Board):
    def __init__(
        self,
        position=config.BOARD_DEFAULT_POSITION,
        size=config.BOARD_DEFAULT_SIZE,
        data_provider=None,
        update_interval=config.BOARD_DEFAULT_UPDATE_INTERVAL,
        duration=config.BOARD_DEFAULT_DURATION,
        boards: Iterable[Board] = [],
    ):
        """
        Initialize a nested board with a list of boards. To share data between the boards, set the board_common_data attribute in the context dictionary.

        :param position: the position of the board on the LCD
        :param size: the size of the board
        :param data_provider: the data provider for the board
        :param update_interval: the update interval for the board
        :param duration: the duration of the board
        :param boards: the list of boards to display
        """
        super().__init__(position, size, data_provider, update_interval, duration)
        self.boards = boards
        self.board_common_data = {}

    def display(self, lcd, context):
        """
        Display the nested board on the LCD.

        :param lcd: the LCD object
        :param context: the context dictionary
        """
        for board in self.boards:
            context["board_common_data"] = self.board_common_data
            board.display(lcd, context)
        return True

    def update(self, lcd, context):
        """
        Update the nested board on the LCD.

        :param lcd: the LCD object
        :param context: the context dictionary
        """
        for board in self.boards:
            context["board_common_data"] = self.board_common_data
            board.update(lcd, context)
        return True
