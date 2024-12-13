from .board import Board

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
        lcd.write_string("Clock board")
        return True
        

    def update(self, lcd, context):
        """
        Updates the clock board on the LCD.

        :param lcd: the LCD object
        """
        lcd.cursor_pos = (self.position[0] + 2, self.position[1])
        data = self.data_provider.get_data()
        lcd.write_string(data["time"])
        return True
