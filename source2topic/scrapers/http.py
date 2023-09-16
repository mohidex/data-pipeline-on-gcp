import requests

class Request:
    def __init__(self, url, method="GET", headers=None, data=None, callback=None, meta=None, **kwargs):
        """
        Create a new request object.

        Args:
            url (str): The URL to make the request to.
            method (str, optional): The HTTP method to use for the request (default is "GET").
            headers (dict, optional): The HTTP request headers to be used for this request.
            data (dict or str, optional): The request data (for POST, PUT, etc. requests).
            callback (callable, optional): The callback function to be called when the response is received.
            meta (dict, optional): Additional metadata associated with the request.
        """
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.data = data
        self.callback = callback
        self.meta = meta or {}
        self.kwargs = kwargs

    def __call__(self) -> requests.Response:
        """
        Make the actual HTTP request.

        Returns:
            requests.Response: The HTTP response.
        """
        return requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            data=self.data,
            **self.kwargs
        )