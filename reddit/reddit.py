from reddit.wrapper import APIWrapper


class RedditAPI(APIWrapper):
    """A simple class to interact with reddit public json api;

    Attributes:
        subreddit (str): reddit community and posts associated with it;
    """

    #
    # def __init__(self, subreddit):
    #     self.subreddit = subreddit

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
