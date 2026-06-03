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

def _coerce(value: str, current):
    """Coerce the string ``value`` to match the type of the attribute's
    current value (bool / int / float / str)."""
    # bool must be checked before int — bool is a subclass of int.
    if isinstance(current, bool):
        v = value.strip().lower()
        if v in ("true", "on", "yes", "1"):
            return True
        if v in ("false", "off", "no", "0"):
            return False
        raise ValueError(f"can't read '{value}' as a true/false value")
    if isinstance(current, int):
        return int(float(value))  # tolerate '21' and '21.0'
    if isinstance(current, float):
        return float(value)
    return value


@tool
def set_device(device_id: str, attribute: str, value: str) -> dict:
    """Set one attribute on one device (e.g. attribute='on' value='true',
    or attribute='target_c' value='21'). Returns the device's new state."""
    device = world.WORLD.get(device_id)
    if device is None:
        raise ValueError(
            f"unknown device '{device_id}'. Call list_devices to see valid ids."
        )
    if attribute not in device:
        raise ValueError(
            f"device '{device_id}' has no attribute '{attribute}'. "
            f"Valid attributes: {sorted(k for k in device if k not in ('type', 'room'))}"
        )

    coerced = _coerce(value, device[attribute])

    # Clamp numeric values into their safe range (booleans are not clamped).
    if attribute in world.GUARDRAILS and not isinstance(coerced, bool):
        lo, hi = world.GUARDRAILS[attribute]
        coerced = max(lo, min(hi, coerced))

    device[attribute] = coerced
    return {"device_id": device_id, **device}

