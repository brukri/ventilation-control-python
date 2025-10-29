import os
import platform
from gpiozero import OutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero.exc import BadPinFactory
from src.models import VentilationLevel

# Environment variable to force mock mode
FORCE_MOCK_ENV = "VENTILATION_FORCE_MOCK"

class VentilationController:
    # GPIO pin mapping
    PIN_17 = 17
    PIN_22 = 22
    PIN_27 = 27
    
    def __init__(self):
        """Initialize the ventilation controller with real or mock GPIO"""
        use_mock = os.getenv(FORCE_MOCK_ENV, "false").lower() == "true"
        
        try:
            if use_mock:
                from gpiozero.pins.mock import MockFactory
                from gpiozero import Device
                Device.pin_factory = MockFactory()
                print("Running in mock mode - no GPIO control active")
            
            # Initialize GPIO outputs
            self._pin_17 = OutputDevice(self.PIN_17, active_high=True, initial_value=False)
            self._pin_22 = OutputDevice(self.PIN_22, active_high=True, initial_value=False)
            self._pin_27 = OutputDevice(self.PIN_27, active_high=True, initial_value=False)
            self._current_level = VentilationLevel.OFF
            
        except BadPinFactory:
            # If we can't initialize real GPIO and mock wasn't requested, force mock mode
            from gpiozero.pins.mock import MockFactory
            from gpiozero import Device
            Device.pin_factory = MockFactory()
            print("No GPIO hardware detected, falling back to mock mode")
            self._pin_17 = OutputDevice(self.PIN_17, active_high=True, initial_value=False)
            self._pin_22 = OutputDevice(self.PIN_22, active_high=True, initial_value=False)
            self._pin_27 = OutputDevice(self.PIN_27, active_high=True, initial_value=False)
            self._current_level = VentilationLevel.OFF
    
    def set_level(self, level: VentilationLevel):
        """Set the ventilation level"""
        self._current_level = level
        
        # Reset all pins to low first
        self._pin_17.off()
        self._pin_22.off()
        self._pin_27.off()
        
        # Set the appropriate pin high based on the level
        if level == VentilationLevel.OFF:
            self._pin_17.on()  # PIN 17 high, others low
        elif level == VentilationLevel.MEDIUM:
            self._pin_27.on()  # PIN 27 high, others low
        elif level == VentilationLevel.HIGH:
            self._pin_22.on()  # PIN 22 high, others low
        # For LOW level, all pins remain low
    
    def get_level(self) -> VentilationLevel:
        """Get the current ventilation level"""
        return self._current_level
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        self._pin_17.close()
        self._pin_22.close()
        self._pin_27.close()
        
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