class INetworking:
    def connect(self):
        raise NotImplementedError("Subclasses should implement this!")

    def listen(self, device):
        raise NotImplementedError("Subclasses should implement this!")