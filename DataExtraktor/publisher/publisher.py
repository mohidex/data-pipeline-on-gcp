from abc import ABC, abstractmethod

class PubSubClient(ABC):

    @abstractmethod
    def publish_message(self, message_data: dict) -> None:
        pass
