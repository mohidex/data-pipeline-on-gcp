from google.cloud import pubsub_v1
import json
from typing import Any

class GooglePubSubClient(PubSubClient):
    def __init__(self, project_id: str, topic_id: str) -> None:
        """
        Initialize the Google Cloud Pub/Sub client.

        Args:
            project_id (str): The Google Cloud project ID.
            topic_id (str): The ID of the Pub/Sub topic to publish messages to.
        """
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish_message(self, message_data: dict) -> Any:
        """
        Publish a message to the specified Pub/Sub topic.

        Args:
            message_data (dict): The dictionary containing the message data to be published.

        Returns:
            Any: The ID of the published message.
        """
        # Convert the message data to a JSON string
        message_data_json = json.dumps(message_data)
        # Encode the message data to bytes
        message_data_bytes = message_data_json.encode('utf-8')
        # Publish the message to the Pub/Sub topic
        future = self.publisher.publish(self.topic_path, data=message_data_bytes)
        # Get the message ID
        message_id = future.result()
        return message_id
