import html


def get_mutations(id, a, b, vote):
    """
    Args:
        a (dict): cached data;
        b (dict): payload;
        vote (str): reddit upvote;

    Returns:

    """

    votes_a = a.get(vote)
    votes_b = b.get(vote)

    received = b.get("received")

    if votes_a > votes_b:
        return {
            "id": id,
            "type": vote,
            "before": votes_a,
            "current": votes_b,
            "diff": votes_b - votes_a,
            "timestamp": received,
        }
    elif votes_a < votes_b:
        return {
            "id": id,
            "type": vote,
            "before": votes_a,
            "current": votes_b,
            "diff": votes_b - votes_a,
            "timestamp": received,
        }
    return {}


def _display_message(a, b, c, d, e):
    return 'Post {} has had it\'s "{}" vote counts {} from {} to {} since your last program execution.'.format(
        a, b, c, d, e
    )


import telnetlib


def get_all_memcached_keys(host, port):
    t = telnetlib.Telnet(host, port)
    t.write("stats items STAT items:0:number 0 END\n")
    items = t.read_until("END").split("\r\n")
    keys = set()
    for item in items:
        parts = item.split(":")
        if not len(parts) >= 3:
            continue
        slab = parts[1]
        t.write(
            "stats cachedump {} 200000 ITEM views.decorators.cache.cache_header..cc7d9 [6 b; 1256056128 s] END\n".format(
                slab
            )
        )
        cachelines = t.read_until("END").split("\r\n")
        for line in cachelines:
            parts = line.split(" ")
            if not len(parts) >= 3:
                continue
            keys.add(parts[1])
    t.close()
    return keys


def truncate_text(string):
    string = str(string).strip()
    return (string[:55] + "...") if len(string) > 55 else string


def escape(data):
    html.escape(data)
