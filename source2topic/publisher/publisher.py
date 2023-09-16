from abc import ABC, abstractmethod

class IPubSubClient(ABC):

    @abstractmethod
    def publish_message(self, message_data: dict) -> None:
        pass
