import json
from pymemcache.client.base import Client

HOST = "memcached"
# HOST = "localhost"
POST = 11211


class JsonSerde:
    """Serializer/Deserializer class;"""

    def serialize(self, key, value):
        if isinstance(value, str):
            return value, 1
        return json.dumps(value), 2

    def deserialize(self, key, value, flags):
        if flags == 1:
            return value
        if flags == 2:
            return json.loads(value)
        raise Exception("Unknown serialization format")


class Cache:
    """Simple cache backend wrapper using Pinterest's pymemcache;

    Attributes:
        client (Client): The client object for a single memcached server;
    """

    def __init__(self):
        self.client = Client((HOST, POST), serde=JsonSerde())

    def __repr__(self):
        return "<Cache {}>".format(self.client.server)

    def get_stats(self, *args):
        """Runs the memcached `stats` command;

        Args:
            *arg (list): extra string arguments to the “stats” command;
        Returns:
            A dictionary of the returned stats;
        """
        return self.client.stats(args)

    def set(self, key, value):
        """Cache setter;

        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        """
        self.client.set(key, value)

    def set_multiple(self, value):
        """A convenience function for setting multiple values;

        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        """
        self.client.set_multi(value)

    def get(self, key):
        """Cache getter;

        Args:
            key (str): unique identifier of pair;

        Returns:
            The value for the key if was found;

        Raises:
            Exception if the key wasn’t found;
        """
        return self.client.get(key)

    def add(self, key, value):
        """Runs memcached “add” command;

        Store data, only if it does not already exist;

        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        Returns:
             return True if value was stored, False if it was not;
        """

        return self.client.add(key, value)

    def replace(self, key, value):
        """Runs memcached “replace” command;

        Store data, but only if the data already exists;

        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        Returns:
             return True if value was stored, False if it was not;
        """

        return self.client.replace(key, value)

    def append(self, key, value):
        """Runs memcached append command;


        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        Returns:
             return True;
        """

        return self.client.append(key, value)

    def prepend(self, key, value):
        """Runs memcached “prepend” command;

        Same as append, but adding new data before existing data;

        Args:
            key (str): unique identifier of pair;
            value (str): value for the key;
        Returns:
             return True;
        """

        return self.client.prepend(key, value)

    def delete(self, key):
        """Runs memcached delete command;"""
        return self.client.delete(key)

    def delete_many(self, keys):
        """A convenience function to delete multiple keys;"""
        return self.client.delete_many(keys)

        # if result is None:
        #     raise Exception("{} has no value in cache".format(key))
        #
        # return result
