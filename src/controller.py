import os
import platform
from src.mock_controller import MockVentilationController
from src.models import VentilationLevel

try:
    import RPi.GPIO as GPIO
    is_raspberry_pi = True
except (ImportError, RuntimeError):
    is_raspberry_pi = False

# Environment variable to force mock mode
FORCE_MOCK_ENV = "VENTILATION_FORCE_MOCK"

class VentilationController:
    # GPIO pin mapping
    PIN_17 = 17
    PIN_22 = 22
    PIN_27 = 27
    
    def __init__(self):
        use_mock = not is_raspberry_pi or os.getenv(FORCE_MOCK_ENV, "false").lower() == "true"
        
        if use_mock:
            self._controller = MockVentilationController()
        else:
            self._controller = self._setup_gpio_controller()
    
    def _setup_gpio_controller(self):
        """Set up the real GPIO controller"""
        class GPIOController:
            def __init__(self, pin_17, pin_22, pin_27):
                self.PIN_17 = pin_17
                self.PIN_22 = pin_22
                self.PIN_27 = pin_27
                self.current_level = VentilationLevel.OFF
                
                # Set up GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.PIN_17, GPIO.OUT)
                GPIO.setup(self.PIN_22, GPIO.OUT)
                GPIO.setup(self.PIN_27, GPIO.OUT)
            
            def set_level(self, level: VentilationLevel):
                """Set the ventilation level using real GPIO"""
                self.current_level = level
                
                if level == VentilationLevel.OFF:
                    self._set_gpio_state(True, False, False)  # PIN 17 high, others low
                elif level == VentilationLevel.LOW:
                    self._set_gpio_state(False, False, False)  # All pins low
                elif level == VentilationLevel.MEDIUM:
                    self._set_gpio_state(False, False, True)  # PIN 27 high, others low
                elif level == VentilationLevel.HIGH:
                    self._set_gpio_state(False, True, False)  # PIN 22 high, others low
            
            def get_level(self) -> VentilationLevel:
                """Get the current ventilation level"""
                return self.current_level
            
            def cleanup(self):
                """Cleanup GPIO resources"""
                GPIO.cleanup()
            
            def _set_gpio_state(self, pin_17_state: bool, pin_22_state: bool, pin_27_state: bool):
                """Set the GPIO pins to the specified states"""
                GPIO.output(self.PIN_17, GPIO.HIGH if pin_17_state else GPIO.LOW)
                GPIO.output(self.PIN_22, GPIO.HIGH if pin_22_state else GPIO.LOW)
                GPIO.output(self.PIN_27, GPIO.HIGH if pin_27_state else GPIO.LOW)
        
        return GPIOController(self.PIN_17, self.PIN_22, self.PIN_27)
    
    def set_level(self, level: VentilationLevel):
        """Set the ventilation level"""
        self._controller.set_level(level)
    
    def get_level(self) -> VentilationLevel:
        """Get the current ventilation level"""
        return self._controller.get_level()
    
    def cleanup(self):
        """Cleanup resources"""
        self._controller.cleanup()