# PrettyTable is a Python library to display tabular data
from prettytable import PrettyTable

TOP_LISTING_FIELDS = ["", "id", "ups", "headline"]

NO_LONGER_TOP_FIELDS = ["id", "ups", "headline"]

VOTE_MUTATIONS_FIELDS = [
    "id",
    "headline",
    "vote_type",
    "when",
    "current",
    "before",
    "diff",
]


# Instantiate tables
top_table = PrettyTable(TOP_LISTING_FIELDS)
no_longer_top_table = PrettyTable(NO_LONGER_TOP_FIELDS)
vote_mutations_table = PrettyTable(VOTE_MUTATIONS_FIELDS)


# Data alignment settings
top_table.align["headline"] = "l"
no_longer_top_table.align["headline"] = "l"
vote_mutations_table.align["headline"] = "l"
