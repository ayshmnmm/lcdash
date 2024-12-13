from data_providers.base_provider import DataProvider
import time


class ClockProvider(DataProvider):
    """
    Clock provider that fetches the current time.
    """

    def fetch_data(self):
        """
        Fetches the current time.
        """
        cur_datetime = time.localtime(time.time())
        cur_time = time.strftime("%H:%M:%S", cur_datetime)
        data = {"time": cur_time, "datetime": cur_datetime}
        self.set_data(data)
