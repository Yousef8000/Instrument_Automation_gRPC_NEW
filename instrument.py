import pyvisa
from datetime import datetime
import time
from collections import deque
import threading

# No more global 'rm'. We only need a global for the connected instrument.
instrument = None

# Data storage and status dictionary remain the same
voltage_data = {1: deque(maxlen=100), 2: deque(maxlen=100), 3: deque(maxlen=100)}
time_data = {1: deque(maxlen=100), 2: deque(maxlen=100), 3: deque(maxlen=100)}
device_status = {
    "connected": False, "device_info": None, "last_settings": {},
    "output_state": False, "timestamp": datetime.now().isoformat(), "current_channel": 1
}
monitoring_active = False
monitoring_thread = None

def list_devices():
    """
    Creates a new VISA resource manager and lists available devices.
    This is the most reliable way to get a fresh, accurate list.
    """
    print("[VISA] Creating new ResourceManager to list devices...")
    # This will raise an exception if NI-VISA is not found, which is what we want.
    rm = pyvisa.ResourceManager()
    devices = rm.list_resources()
    print(f"[VISA] Found devices: {devices}")
    return devices

def connect_device(address):
    """Establishes a connection to a specific VISA instrument."""
    global instrument, device_status
    print(f"[VISA] Attempting to connect to: {address}")
    try:
        if instrument:
            instrument.close() # Close any previous connection
        rm = pyvisa.ResourceManager()
        instrument = rm.open_resource(address)
        instrument.timeout = 5000  # 5 second timeout
        idn = instrument.query("*IDN?").strip()
        print(f"[VISA] Successfully connected to: {idn}")

        device_status.update({
            "connected": True,
            "device_info": idn.split(',')[0] if ',' in idn else idn,
            "current_channel": 1
        })
        check_initial_output_state()
        start_monitoring()
        return idn
    except Exception as e:
        print(f"[VISA CRITICAL ERROR] on connect: {e}")
        instrument = None
        device_status["connected"] = False
        raise e # Re-raise the exception to be caught by the gRPC layer

def disconnect_device():
    """Disconnects from the instrument and resets status."""
    global instrument, device_status
    stop_monitoring()
    if instrument:
        try:
            for ch in [1, 2, 3]:
                instrument.write(f"INST:NSEL {ch}")
                instrument.write("OUTP OFF")
        except pyvisa.errors.VisaIOError:
            pass # Ignore errors if device is already gone
        instrument.close()
    instrument = None
    print("[VISA] Device disconnected.")
    device_status.update({"connected": False, "device_info": None, "output_state": False})
    clear_data()
    return True

# --- All functions below are simple wrappers with guards ---

def get_status():
    if device_status["connected"]: check_initial_output_state()
    device_status["timestamp"] = datetime.now().isoformat()
    return device_status

def set_channel_settings(channel, limit, voltage, current):
    if not instrument: return False, "Instrument not connected"
    try:
        instrument.write(f"INST:NSEL {channel}")
        instrument.write(f"SOUR:VOLT:LIM {limit}")
        instrument.write(f"SOUR:VOLT:LIM:STAT ON")
        instrument.write(f"SOUR:VOLT {voltage}")
        instrument.write(f"SOUR:CURR {current}")
        return True, f"Channel {channel} set to {voltage}V, {current}A"
    except Exception as e:
        return False, str(e)

def set_output(channel, state):
    if not instrument: return False, "Instrument not connected"
    try:
        channels_to_set = [1, 2, 3] if channel == 0 else [channel]
        for ch in channels_to_set:
            instrument.write(f"INST:NSEL {ch}")
            instrument.write(f"OUTP {'ON' if state else 'OFF'}")
        check_initial_output_state()
        msg = f"All channels set to {'ON' if state else 'OFF'}" if channel == 0 else f"Channel {channel} set to {'ON' if state else 'OFF'}"
        return True, msg
    except Exception as e:
        return False, str(e)

def check_initial_output_state():
    if not instrument: return
    try:
        states = [int(instrument.query(f"OUTP? {ch}").strip()) for ch in [1,2,3]]
        device_status["output_state"] = any(states)
    except Exception:
        device_status["output_state"] = False

def monitor_voltage():
    global monitoring_active
    while monitoring_active:
        if instrument and device_status["connected"]:
            try:
                ch = device_status["current_channel"]
                instrument.write(f"INST:NSEL {ch}")
                voltage = float(instrument.query("MEAS:VOLT?").strip())
                time_data[ch].append(datetime.now())
                voltage_data[ch].append(voltage)
            except Exception: pass
        time.sleep(1)

def start_monitoring():
    global monitoring_active, monitoring_thread
    if not monitoring_active:
        monitoring_active = True
        monitoring_thread = threading.Thread(target=monitor_voltage, daemon=True)
        monitoring_thread.start()
        print("[MONITOR] Started.")

def stop_monitoring():
    global monitoring_active
    if monitoring_active:
        monitoring_active = False
        print("[MONITOR] Stopped.")

def clear_data():
    for ch in [1, 2, 3]:
        voltage_data[ch].clear()
        time_data[ch].clear()

def get_plot_data(channel):
    return {"time": [t.isoformat() for t in time_data[channel]], "voltage": list(voltage_data[channel])}

def set_current_channel(channel):
    if channel in [1, 2, 3]:
        device_status["current_channel"] = channel
        return True, f"Monitoring channel set to {channel}"
    return False, "Invalid channel"