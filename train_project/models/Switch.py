import uasyncio as asyncio

class Switch():
    def __init__(self, driver):
        self.driver = driver

    async def switch(self, action):
        """
        Control the motor with the specified direction and speed.
        """
        if action == "open":
            self.driver.direction.value(1)
        elif action == "close":
            self.driver.direction.value(0)
        else:
            raise ValueError("Invalid action. Use 'open' or 'close'.")
        
        self.driver.pwm.duty(self.driver.speed)  # Set PWM speed
        await asyncio.sleep(0.3)
        self.stop()

    def stop(self):
        """
        Stop the motor.
        """
        self.driver.pwm.duty(0)
        self.driver.direction.value(0)
