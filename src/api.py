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
async def set_level(level: VentilationLevel):
    """Set the ventilation level"""
    controller.set_level(level)
    return {"level": level, "status": "success"}