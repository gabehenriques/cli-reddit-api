from cli.wrapper import APIWrapper
from utils.cache.backend.base import Cache


class RedditAPI(APIWrapper):
    """A simple class to interact with the reddit public api;"""

    def get_subreddit_top_posts(self, subreddit, limit=75):
        """Fetch subreddits/posts from reddit.com;

        Args:
            subreddit (str): reddit community and posts associated with it;
            limit (int): max number of posts to return in the listing;
        Returns:
            A dictionary containing JSON data;
        """
        url = "https://www.reddit.com/r/{subreddit}/top.json".format(
            subreddit=subreddit
        )
        return self.make_request(url, limit=limit)
