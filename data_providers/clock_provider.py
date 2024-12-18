from data_providers.base_provider import DataProvider
import time
import datetime


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
        ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        cur_datetime = datetime.datetime.fromtimestamp(time.time(), ist)
        cur_time = cur_datetime.strftime("%H:%M:%S")
        data = {"time": cur_time}
        self.set_data(data)
