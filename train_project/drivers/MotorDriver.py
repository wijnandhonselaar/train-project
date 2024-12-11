class MotorDriver:
    async def actuate(self, direction, speed):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    async def gradualy_actuate(self, direction, speed, delay=100):
        raise NotImplementedError("This method should be implemented by subclasses")

    def stop(self):
        raise NotImplementedError("This method should be implemented by subclasses")
