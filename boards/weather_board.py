import time
from boards.board import Board
from icons.manager import IconManager
import icons.icons as icons

class WeatherBoard(Board):
    """
    Weather board displayed on the LCD.
    """

    def display(self, lcd, context):
        """
        Displays the weather board on the LCD.

        :param lcd: the LCD object
        """
        lcd.cursor_pos = self.position
        lcd.write_string("Weather")
        return True

    def update(self, lcd, context):
        """
        Updates the weather board on the LCD.

        :param lcd: the LCD object
        """
        lcd.cursor_pos = (self.position[0] + 2, self.position[1])
        data = self.data_provider.get_data()
        if data and "locality_weather_data" in data:
            lcd.write_string(f'{data["locality_weather_data"]["temperature"]}{chr(223)}C')
            last_updated = time.gmtime(time.time() - data["last_updated"])
            if last_updated.tm_hour > 0:
                last_updated = f"{last_updated.tm_hour}h"
            elif last_updated.tm_min > 0:
                last_updated = f"{last_updated.tm_min}m"
            else:
                last_updated = f"{last_updated.tm_sec}s"
            # make last_updated string right-aligned with fixed length
            last_updated = IconManager.use_icon(lcd, icons.DOWNLOAD) + " " + last_updated
            last_updated = last_updated.rjust(5)
            lcd.cursor_pos = (self.position[0] + 3, self.size[1] - len(last_updated)+1)
            lcd.write_string(last_updated)
        return True
    