from pymemcache.client import base

HOST = "localhost"
POST = 11212

OLD_CACHE = base.Client((HOST, POST), ignore_exc=True)
NEW_CACHE = base.Client((HOST, POST))


class Cache:
    """Simple cache backend wrapper using pymemcache;

    Attributes:
        client (Client): The client object for a single memcached server;
    """

    def __init__(self):
        self.client = base.Client((HOST, POST))

    def __repr__(self):
        return "<Cache {}>".format(self.client.server)

    def set_to_cache(self, key, value):
        """Cache setter;

        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        """
        self.client.set(key, value)

    def get_from_cache(self, key):
        """Cache getter;

        Args:
            key (str): unique identifier of pair;

        Returns:
            The value for the key if was found;

        Raises:
            Exception if the key wasn’t found;
        """
        result = self.client.get(key)

        if result is None:
            raise Exception("{} has no value in cache".format(key))

        return result
