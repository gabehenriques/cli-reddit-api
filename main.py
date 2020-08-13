import click
from reddit.reddit import RedditAPI


@click.command()
@click.option("--subreddit", help="Reddit subreddit, e.g. popular")
@click.option("--limit", default=75, help="Top posts list.")
def main(subreddit, limit):
    """Entry point of execution for cli;

    Args:
        subreddit (str): reddit community and posts associated with it;
        limit (int): max number of posts to return in the listing;

    Returns:
        Should return a 'list' of top :parm:`limit` posts in the listing;
    """

    reddit = RedditAPI()

    resp = reddit.get_subreddit_top_posts(subreddit, limit)

    for i in resp.parsed["data"]["children"]:
        print(i["data"]["title"])


if __name__ == "__main__":
    main()
