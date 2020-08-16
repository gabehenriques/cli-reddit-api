MESSAGE_ONE = ""

MUTATIONS_HEADING = "Mutations since last program execution"


def top_list_msg(limit):
    return "Top {} subreddits listing:".format(limit)


def no_longer_top_list_msg(limit):
    return "The following posts are no longer in the top {} list".format(limit)
