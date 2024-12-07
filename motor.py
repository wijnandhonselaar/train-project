import uasyncio as asyncio

class Motor:
    def __init__(self, driver):
        """
        Initialize the motor with a specific driver.
        :param driver: An instance of a motor driver.
        """
        self.driver = driver
        self.task = None  # Async task for motor actuation

    def start(self, direction=1, speed=512, duration=None):
        """
        Start the motor.
        :param direction: 1 for forward, 0 for reverse.
        :param speed: Speed of the motor (0-1023).
        :param duration: Duration to run the motor in seconds (None for indefinite).
        """
        if self.task and not self.task.done():
            self.task.cancel()  # Cancel any ongoing motor task

        self.task = asyncio.create_task(self._run_motor(direction, speed, duration))

    async def _run_motor(self, direction, speed, duration):
        """
        Internal coroutine to run the motor.
        """
        await self.driver.actuate(direction, speed)
        if duration is not None:
            await asyncio.sleep(duration)
            self.stop()

    def stop(self):
        """
        Stop the motor.
        """
        if self.task and not self.task.done():
            self.task.cancel()
        self.driver.stop()
