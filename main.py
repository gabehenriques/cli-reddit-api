import time
from datetime import datetime
import click

from reddit.reddit import RedditAPI
from utils.cache.backend.base import Cache
from utils.helpers import *
from utils.console.tables import *
from utils.console.messages import *

reddit = RedditAPI()
cache = Cache()


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

    # Vars
    TOP_LIST_HEADING = top_list_msg(limit)
    NO_LONGER_IN_TOP_LIST_HEADING = no_longer_top_list_msg(limit)

    # Fetch reddit.com
    resp = reddit.get_subreddit_top_posts(subreddit, limit)

    # Get payload
    subreddits = resp.parsed["data"]["children"]

    # Set init state
    STATE = {}

    # Check if there is cached data
    if cache.get("ids"):
        cached_post_ids = cache.get("ids")
    else:
        cached_post_ids = []

    # Set array to store post ids from payload
    payload_post_ids = []

    index = 1
    for i in subreddits:
        post = i["data"]

        # Get post metadata
        id = post["id"]
        headline = post["title"]
        ups = post["ups"]
        curr_timestamp = int(time.time())

        # Add state
        STATE[id] = {
            "headline": headline,
            "ups": ups,
            "received": curr_timestamp,
        }

        # Cache post
        cached_post = cache.get(id)

        # Check if post exists in memory
        if cached_post:
            # Check if there are mutations with new data
            if cached_post != STATE[id]:

                # Get upvote mutation
                mutation = get_mutations(id, cached_post, STATE[id], "ups")

                # Set rows for `vote_mutations_table`
                if mutation:

                    # Shorten headline for smooth rendering
                    title = truncate_text(STATE[id]["headline"])

                    # Get date and time when mutation was received
                    when = datetime.fromtimestamp(mutation["timestamp"])

                    # Add single row
                    vote_mutations_table.add_row(
                        [
                            mutation["id"],
                            title,
                            mutation["type"],
                            when,
                            mutation["current"],
                            mutation["before"],
                            mutation["diff"],
                        ]
                    )

                # Replace the value of the existing post in cache
                cache.replace(id, STATE[id])

        else:
            # Cache the new post
            cache.add(id, STATE[id])

        # Append id
        payload_post_ids.append(id)

        # Set rows for `top_table
        title = truncate_text(headline)
        top_table.add_row([index, id, ups, title])

        # Increment count
        index += 1

    # Get diff from cached data and payload
    no_loner_in_top_list = list(set(cached_post_ids) - set(payload_post_ids))

    if no_loner_in_top_list:
        # [TABLE] No Longer in the top list
        print(NO_LONGER_IN_TOP_LIST_HEADING)
        for i in no_loner_in_top_list:
            title = truncate_text(cache.get(i)["headline"])
            ups = cache.get(i)["ups"]

            no_longer_top_table.add_row([id, ups, title])

        print(top_table, "\n")

        # Remove legacy posts and update cache
        cache.delete_many(no_loner_in_top_list)
        cache.replace("ids", payload_post_ids)
    else:
        # Reset cache for post ids to have a fresh copy in memory
        cache.set("ids", payload_post_ids)

    # [TABLE] Top list
    print(TOP_LIST_HEADING)
    print(top_table, "\n")

    # [TABLE] Mutations
    print(MUTATIONS_HEAD)
    print(vote_mutations_table, "\n")


if __name__ == "__main__":
    main()
