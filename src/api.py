from fastapi import FastAPI, HTTPException
from src.controller import VentilationController
from src.models import VentilationLevel
import atexit

app = FastAPI(
    title="Ventilation Control API",
    description="REST API for controlling Stiebel Eltron LWZ 170E plus ventilation system",
    version="1.0.0"
)

# Create a single instance of the controller
controller = VentilationController()

# Register cleanup on application shutdown
atexit.register(controller.cleanup)

@app.get("/ventilation-control/level")
async def get_level():
    """Get the current ventilation level"""
    return {"level": controller.get_level()}

@app.post("/ventilation-control/level/{level}")
async def set_level(level: str):
    """Set the ventilation level"""
    try:
        ventilation_level = VentilationLevel(level.lower())
        controller.set_level(ventilation_level)
        return {"level": ventilation_level, "status": "success"}
    except ValueError:
        valid_levels = [level.value for level in VentilationLevel]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid ventilation level. Valid levels are: {', '.join(valid_levels)}"
        )