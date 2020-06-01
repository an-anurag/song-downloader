from redis import Redis


class DownloadHistory:

    def __init__(self):
        self.db = Redis('localhost', db=0)

    def add(self, key, value):
        self.db.set(key, value)

    def remove(self, key):
        self.db.delete(key)


class DownloadQueue:

    def __init__(self):
        self.db = Redis('localhost', db=1)

    def add(self, key, value):
        self.db.set(key, value)

    def remove(self, key):
        self.db.delete(key)