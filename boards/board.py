from abc import ABC, abstractmethod
from RPLCD.i2c import CharLCD
import config


class Board(ABC):
    """
    Base class for all boards displayed on the LCD.
    Each board is a self-contained entity that can be displayed on the LCD.
    """

    def __init__(
        self,
        position: tuple[int, int] = config.BOARD_DEFAULT_POSITION,
        size: tuple[int, int] = config.BOARD_DEFAULT_SIZE,
        data_provider=None,
        update_interval: int = config.BOARD_DEFAULT_UPDATE_INTERVAL,
        duration: int = config.BOARD_DEFAULT_DURATION,
    ):
        """
        Initializes the board.
        """
        self.position: tuple[int, int] = (
            position  # position of top-left corner of the board on the LCD
        )
        self.size: tuple[int, int] = size  # board size (rows, columns)
        self.data_provider = data_provider  # data provider for the board
        self.update_interval: int = (
            update_interval  # to call the display method every display_interval ms
        )
        self.duration: int = duration  # duration of the board in seconds

    @abstractmethod
    def display(self, lcd: CharLCD, context: dict) -> bool:
        """
        Displays the initial state of the board on the LCD. Called once when the board is brought into view.

        :param lcd: the LCD object
        :param context: the context dictionary containing data like start time, end time, etc.
        :return: True if the board should continue to be displayed, False otherwise. Return False immediately if the board
        is not to be displayed at all.
        """
        pass

    @abstractmethod
    def update(self, lcd: CharLCD, context: dict) -> bool:
        """
        Updates the board on the LCD. This method is called every update_interval ms.

        :param lcd: the LCD object
        :param context: the context dictionary containing data like start time, end time, etc.
        :return: True if the board should continue to be displayed, False otherwise
        """
        pass
