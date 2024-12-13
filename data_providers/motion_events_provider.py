from data_providers.base_provider import DataProvider
import requests
from requests.auth import HTTPDigestAuth
from lxml import etree


class MotionEventsProvider(DataProvider):
    def __init__(self, url: str, username: str, password: str):
        """
        Initializes the motion events provider.

        :param url: the URL of the event stream
        :param username: the username to authenticate with
        :param password: the password to authenticate with
        :param handler: the handler to call when new data is fetched. The handler should accept a single argument, the data.
        """
        super().__init__()
        self.url = url
        self.username = username
        self.password = password

    def fetch_data(self):
        pass  # data is fetched in a custom implementation in the run method

    @staticmethod
    def parse_event(event_xml: str) -> dict:
        """
        Parses the XML event notification into a dictionary.
        :param event_xml: the XML event notification
        :return: a dictionary containing the event data
        """
        root = etree.fromstring(event_xml)
        event_data = {element.tag.split("}")[1]: element.text for element in root}
        return event_data

    def _run(self):
        print(f"Starting to run custom impl of run {self.__class__.__name__}")
        response = requests.get(
            self.url, auth=HTTPDigestAuth(self.username, self.password), stream=True
        )
        if response.status_code == 200:
            print("Connected to the event stream")
            constructed_response = ""
            for chunk in response.iter_content():
                constructed_response += chunk.decode("utf-8")
                if constructed_response.endswith("</EventNotificationAlert>"):
                    event = constructed_response[
                        constructed_response.find("<EventNotificationAlert") :
                    ]
                    constructed_response = ""
                    self.set_data(self.parse_event(event))
        else:
            raise Exception(
                f"Failed to connect to the event stream: {response.status_code}"
            )
