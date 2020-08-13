import time
import requests
import sys

from utils.exceptions import EmptyResponse
from requests.exceptions import ConnectionError


class APIWrapper:
    """A simple wrapper around the `requests` HTTP library for Python;

    Attributes:
        response_format (str): API response data format;
    """

    def __init__(self, response_format="json"):
        """Wrapper constructor;

        Args:
            response_format (str): API response data format;
        """
        self.response_format = response_format

    def __repr__(self):
        pass

    def __str__(self):
        return "<APIWrapper response_format={} >".format(self.response_format)

    def make_request(
        self, url, method="get", headers=None, callback=None, **parms
    ):
        """Method to request an API call using Python's `requests` library;

        Args:
            url (str): URL for the :class:`Request` object;
            method (str): HTTP method for the :class:`Request` object;
            headers (optional) (dict): A dictionary of HTTP Headers to send;
            parms (optional) (dict): A dcictionary, or list of tuples, to send;

        Returns:
            A dictionary containing JSON data;
        """
        request = getattr(requests, method.lower())

        if callback is None:
            callback = self._default_callback

        if headers is None:
            headers = {"user-agent": "onaroll-test/0.0.1"}

        response = request(url, headers=headers, params=parms)

        try:
            response.raise_for_status()
            return callback(response)
        except Exception as e:
            return self._with_error_handling(response, e, self.response_format)

    @staticmethod
    def _parse_response(response, response_format):
        """Parses API data to json;

        We will be using Reddit's read-only JSON API, but it's good practice to
        ensure the response content is parsed correctly. In case the JSON
        decoding fails, `response.json()` raises an exception.

        Args:
            response (Response): :class:`Response` object;
            response_format (str): API response data format;

        Returns:
            A dictionary containing JSON data;
        """
        response.parsed = response.json()
        return response

    @staticmethod
    def _with_error_handling(response, error, response_format="json"):
        """Static method for error handling;

        Args:
            response (Response): :class:`Response` object;
            error (str): Error thrown;
            response_format (str): API response data format;

        Returns:
            A object containing JSON payload;
        """

        def safe_parse(response):
            """Checks for value and/or syntax erros;

            Args:
                response (Response): :class:`Response` object;

            Retuns:
                A dictionary containing JSON data if no error exception is raised, otherwise returns :class:`Response` object;
            """
            try:
                return APIWrapper._parse_response(response, response_format)
            except (ValueError, SyntaxError) as ex:
                response.parsed = None
                return response

        if isinstance(error, requests.HTTPError):
            if response.status_code == 400:
                response = safe_parse(response)
                if response.parsed is not None:
                    parsed_response = response.parsed
                    messages = []
                    if (
                        response_format == "json"
                        and "ValidationErrors" in parsed_response
                    ):
                        messages = [
                            e["Message"]
                            for e in parsed_response["ValidationErrors"]
                        ]
                    error = requests.HTTPError(
                        "%s: %s" % (error, "\n\t".join(messages)),
                        response=response,
                    )
            elif response.status_code == 429:
                error = requests.HTTPError(
                    "{} Too many requests in the last minute.".format(error),
                    response=response,
                )

        return safe_parse(response)

    def _default_callback(self, response):
        """Default executable code passed in as an argument to `make_request()`;

        Args:
            response (Response): :class:`Response` object;

        Returns:
            A dictionary containing JSON data if no error exception is raised;

        Raises:
            `EmptyResponse` is there is no payload;
            `ValueError` if data is not parsed correctly;
        """
        if not response or not response.content:
            raise EmptyResponse("Response has no content.")

        try:
            parsed_response = self._parse_response(
                response, self.response_format
            )
        except (ValueError, SyntaxError):
            raise ValueError(
                "Invalid {} in response to {}".format(
                    self.response_format, response.content[:100]
                )
            )
        return parsed_response
