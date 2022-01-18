import uuid


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class AppState(Singleton):

    def __init__(self):
        self.number_of_connected_clients = 0
        self.server_uuid = uuid.uuid4()


AppState()
