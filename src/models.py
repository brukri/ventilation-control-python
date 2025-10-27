from enum import Enum

class VentilationLevel(str, Enum):
    """Enum representing the available ventilation levels"""
    OFF = "off"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"