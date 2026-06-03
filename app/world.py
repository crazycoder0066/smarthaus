# one mutable in-memory world; reset between eval runs
WORLD = {
    "bedroom_thermostat":  {"type": "thermostat", "room": "bedroom",    "target_c": 19, "current_c": 17},
    "living_room_lights":  {"type": "light",      "room": "living_room","on": False, "brightness": 0},
    "living_room_blinds":  {"type": "blinds",     "room": "living_room","open": True},
    "kitchen_lights":      {"type": "light",      "room": "kitchen",    "on": True,  "brightness": 80},
}
SENSORS = {
    "bedroom": {"temperature": 17},
    "living_room": {"temperature": 21},
    "kitchen": {"temperature": 22}
}

# Safe ranges for numeric attributes. set_device clamps incoming values into
# these bounds so the agent can never drive a device out of a safe range.
GUARDRAILS = {
    "target_c":   (5, 30),    # thermostat setpoint, °C
    "brightness": (0, 100),   # light brightness, %
}
