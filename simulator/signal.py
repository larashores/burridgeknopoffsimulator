class Signal:
    def __init__(self):
        self.connections = []
        self.debug = False

    def __call__(self, *args, **kwargs):
        for func in self.connections:
            func(*args, **kwargs)

    def connect(self, func):
        if func not in self.connections:
            self.connections.append(func)

    def disconnect(self, func):
        if func in self.connections:
            self.connections.remove(func)

    def clear(self):
        self.connections.clear()
