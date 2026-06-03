from langchain_core.tools import tool
from app import world

@tool
def list_devices() -> dict:
    """List every device and its current state. Call this first to discover device ids."""
    return world.WORLD

@tool
def get_sensor(room: str, sensor: str) -> dict:
    """Read a sensor in a room, e.g. room='bedroom', sensor='temperature'."""
    return world.SENSORS[room][sensor]

@tool
def set_device(device_id: str, attribute: str, value: str) -> dict:
    """Set one attribute on one device (e.g. attribute='on' value='true',
    or attribute='target_c' value='21'). Returns the device's new state."""
    ...  # TODO: validate device exists; coerce value; CLAMP (see guardrail); return new state
    pass
