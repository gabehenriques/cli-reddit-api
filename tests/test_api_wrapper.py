"""
Tests for the api wrapper module;
"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from cli.wrapper import APIWrapper
from requests.exceptions import MissingSchema, HTTPError


class TestApiWrapper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = APIWrapper()
        cls.service_url = "https://www.reddit.com/r/popular/top.json"
        cls.response_mock = MagicMock()

    def setUp(self):
        pass

    def test_make_request_with_empty_url__should_raise_MissingSchema(self):
        service_url = ""
        with self.assertRaises(MissingSchema):
            self.api.make_request(url=service_url)

    @patch("cli.wrapper.APIWrapper._with_error_handling")
    def test_make_request_http_error__should_call_custom_error_handling_method(
        self, custom_error_handling_method
    ):
        non_existing_listing = "nonexistinglisting"
        service_url = "https://www.reddit.com/r/popular/{}.json".format(
            non_existing_listing
        )
        self.api.make_request(url=service_url)

        self.assertTrue(custom_error_handling_method.called)

    @patch("cli.wrapper.APIWrapper._default_callback")
    def test_make_request__should_call_default_callback(self, default_callback):
        self.api.make_request(url=self.service_url)

        self.assertTrue(default_callback.called)

    def test_error_handling__should_call_safe_pasrse_method(self):
        response_mock = self.response_mock
        type(response_mock).status_code = PropertyMock(return_value=400)

        error = HTTPError()
        format = "json"

        APIWrapper()._with_error_handling(response_mock, error, format)
        # self.assertTrue(safe_parse_method.called)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
