from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import grpc_client

router = APIRouter()

# --- Pydantic Models for Request Validation ---
class ConnectRequest(BaseModel):
    device_address: str

class ChannelSettings(BaseModel):
    channel: int = Field(..., ge=1, le=3)
    voltage_limit: float = Field(..., ge=0, le=30)
    voltage_set: float = Field(..., ge=0, le=30) # Renamed for clarity
    current: float = Field(..., ge=0, le=5)

class OutputRequest(BaseModel):
    state: bool

class ChannelSelectRequest(BaseModel):
    channel: int = Field(..., ge=1, le=3)

# --- API Routes ---
@router.get("/devices")
async def get_devices():
    return await grpc_client.list_devices()

@router.post("/connect")
async def connect_to_device(request: ConnectRequest):
    success, message = await grpc_client.connect_remote_device(request.device_address)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "device_info": message}

@router.post("/disconnect")
async def disconnect_from_device():
    success, message = await grpc_client.disconnect_remote_device()
    return {"success": success, "message": message}

@router.get("/status")
async def get_device_status():
    status_dict = await grpc_client.get_status()
    return status_dict

@router.post("/settings")
async def apply_settings(settings: ChannelSettings):
    success, message = await grpc_client.set_channel_settings(
        settings.channel, settings.voltage_limit, settings.voltage_set, settings.current
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}

@router.post("/output")
async def control_output(request: OutputRequest):
    # Channel 0 is our command for "all channels"
    success, message = await grpc_client.set_output(0, request.state)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}

@router.post("/set-channel")
async def set_monitoring_channel(request: ChannelSelectRequest):
    success, message = await grpc_client.set_current_channel(request.channel)
    return {"success": success, "message": message}

@router.get("/plot-data")
async def get_plot_data_endpoint():
    status = await grpc_client.get_status()
    if not status.get("connected"):
        return {"time": [], "voltage": []}
    current_channel = status.get("current_channel", 1)
    return await grpc_client.get_plot_data(current_channel)

@router.post("/clear-data")
async def clear_plot():
    success, message = await grpc_client.clear_data()
    return {"success": success, "message": message}