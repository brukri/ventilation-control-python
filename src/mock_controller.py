from src.models import VentilationLevel

class MockVentilationController:
    """Mock implementation of the ventilation controller for testing purposes"""
    def __init__(self):
        self.current_level = VentilationLevel.OFF
        print("Running in mock mode - no GPIO control active")
    
    def set_level(self, level: VentilationLevel):
        """Set the ventilation level in mock mode"""
        self.current_level = level
        print(f"Mock: Setting ventilation level to {level}")
        
        # Print mock GPIO states based on level
        if level == VentilationLevel.OFF:
            self._print_gpio_state(True, False, False)  # PIN 17 high, others low
        elif level == VentilationLevel.LOW:
            self._print_gpio_state(False, False, False)  # All pins low
        elif level == VentilationLevel.MEDIUM:
            self._print_gpio_state(False, False, True)  # PIN 27 high, others low
        elif level == VentilationLevel.HIGH:
            self._print_gpio_state(False, True, False)  # PIN 22 high, others low
    
    def get_level(self) -> VentilationLevel:
        """Get the current ventilation level"""
        return self.current_level
    
    def cleanup(self):
        """Mock cleanup method"""
        print("Mock: Cleaning up resources")
    
    @staticmethod
    def _print_gpio_state(pin_17_state: bool, pin_22_state: bool, pin_27_state: bool):
        """Print mock GPIO states"""
        print(f"Mock GPIO state - PIN 17: {pin_17_state}, PIN 22: {pin_22_state}, PIN 27: {pin_27_state}")