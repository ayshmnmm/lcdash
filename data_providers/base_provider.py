from abc import ABC, abstractmethod
import threading
import time

class DataProvider(ABC):
    def __init__(self, update_interval: float = 30):
        """
        Initializes the data provider. Avoid initializing multiple data providers with the same parameters.

        :param update_interval: the interval at which to fetch data in seconds
        """
        self._data: dict = {}
        self.lock = threading.Lock()
        self.running: bool = True
        self.update_interval: float = update_interval

    @abstractmethod
    def fetch_data(self):
        """
        Fetch and process data. This method is unique to each provider.
        """
        pass

    def get_data(self):
        """
        Returns the latest data in a thread-safe way.
        """
        with self.lock:
            return self._data.copy()
        
    def set_data(self, data):
        """
        Sets the data in a thread-safe way.
        """
        with self.lock:
            self._data = data

    def start(self):
        """Starts the data-fetching thread."""
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """Continuously fetch data while running."""
        print(f"Starting {self.__class__.__name__} provider")
        # TODO: catch exceptions and handle retries
        while self.running:
            self.fetch_data()
            time.sleep(self.update_interval)

    def stop(self):
        """Stops the data-fetching thread."""
        self.running = False
        print(f"Stopping {self.__class__.__name__} provider")