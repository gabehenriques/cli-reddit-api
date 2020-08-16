from reddit.wrapper import APIWrapper
from utils.cache.backend.base import Cache


class RedditAPI(APIWrapper):
    """A simple class to interact with the reddit public api;

    Attributes:
        subreddit (str): reddit community and posts associated with it;
    """

    def get_subreddit_top_posts(self, subreddit, limit=75):
        """
        """
        url = "https://www.reddit.com/r/{subreddit}/top.json".format(
            subreddit=subreddit
        )
        return self.make_request(url, limit=limit)

    """
    id (str): i['data']['id']
    title (str): i['data']['title']
    created (timestamp): i['data']['created_utc']

    for i in resp.parsed["data"]["children"]:
        print(i['data']['title'])
    """
