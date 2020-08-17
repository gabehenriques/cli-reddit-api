import unittest
from cli.reddit import RedditAPI


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = RedditAPI()

    def test_api_call__should_return_200(self):
        subreddit = "popular"
        response = self.api.get_subreddit_top_posts(subreddit)

        self.assertEqual(response.status_code, 200)

    def test_api_call___should_make_call_to_correct_url(self):
        subreddit = "popular"
        limit = 10
        response = self.api.get_subreddit_top_posts(subreddit, limit)
        request_url = response.request.url
        expected_url = "https://www.reddit.com/r/{}/top.json?limit={}".format(
            subreddit, limit
        )

        self.assertEqual(request_url, expected_url)

    def test_api_call_without_limit___should_limit_default_75(self):
        subreddit = "popular"
        response = self.api.get_subreddit_top_posts(subreddit)
        num_items_retrieved = len(response.parsed["data"]["children"])

        self.assertEqual(num_items_retrieved, 75)

    def test_api_call_with_limit___should_fetch_correct_number_of_items(self):
        limit = 10
        subreddit = "popular"
        response = self.api.get_subreddit_top_posts(subreddit, limit)
        num_items_retrieved = len(response.parsed["data"]["children"])

        self.assertEqual(num_items_retrieved, limit)
