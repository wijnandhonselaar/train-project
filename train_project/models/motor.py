import uasyncio as asyncio

class Motor:
    def __init__(self, driver):
        """
        Initialize the motor with a specific driver.
        :param driver: An instance of a motor driver.
        """
        self.driver = driver
        self.task = None  # Async task for motor actuation

    def start(self, direction=1, speed=512):
        """
        Start the motor.
        :param direction: 1 for forward, 0 for reverse.
        :param speed: Speed of the motor (0-1023).
        :param delay: Delay between increasing the speed to reach the specified speed.
        """
        if self.task and not self.task.done():
            self.task.cancel()  # Cancel any ongoing motor task

        self.task = asyncio.create_task(self._run_motor(direction, speed))

    def start_gradually(self, direction=1, speed=512, delay=100):
        """
        Start the motor.
        :param direction: 1 for forward, 0 for reverse.
        :param speed: Speed of the motor (0-1023).
        :param delay: Delay between increasing the speed to reach the specified speed.
        """
        if self.task and not self.task.done():
            self.task.cancel()  # Cancel any ongoing motor task

        self.task = asyncio.create_task(self._run_motor(direction, speed, delay))

    async def _run_motor(self, direction, speed, delay=None):
        """
        Internal coroutine to run the motor.
        """

        if delay is None:
            await self.driver.actuate(direction, speed)
        else:
            await self.driver.gradualy_actuate(direction, speed, delay)

    def stop(self):
        """
        Stop the motor.
        """
        if self.task and not self.task.done():
            self.task.cancel()
        self.driver.stop()
