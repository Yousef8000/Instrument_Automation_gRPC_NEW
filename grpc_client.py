import asyncio
import grpc
import json

import instrument_pb2
import instrument_pb2_grpc

GRPC_ADDRESS = "localhost:50051"

# Reuse a single gRPC channel and stub to avoid connection overhead.
_channel: grpc.aio.Channel | None = None
_stub: instrument_pb2_grpc.InstrumentServiceStub | None = None


async def _get_stub() -> instrument_pb2_grpc.InstrumentServiceStub:
    """Lazily create and return a gRPC stub."""
    global _channel, _stub
    if _stub is None:
        _channel = grpc.aio.insecure_channel(GRPC_ADDRESS)
        _stub = instrument_pb2_grpc.InstrumentServiceStub(_channel)
    return _stub


async def close_channel() -> None:
    """Close the global gRPC channel if it exists."""
    global _channel, _stub
    if _channel is not None:
        await _channel.close()
        _channel = None
        _stub = None

async def list_devices():
    stub = await _get_stub()
    try:
        response = await stub.ListDevices(instrument_pb2.Empty())
        return list(response.devices)
    except grpc.aio.AioRpcError as e:
        return [f"gRPC Error: {e.details()}"]

async def connect_remote_device(address: str):
    stub = await _get_stub()
    try:
        request = instrument_pb2.DeviceRequest(address=address)
        response = await stub.ConnectDevice(request)
        return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def disconnect_remote_device():
    stub = await _get_stub()
    try:
        response = await stub.DisconnectDevice(instrument_pb2.Empty())
        return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def get_status():
    stub = await _get_stub()
    try:
        response = await stub.GetStatus(instrument_pb2.Empty())
        return json.loads(response.status)
    except (grpc.aio.AioRpcError, json.JSONDecodeError):
        return {"connected": False}

# --- All other functions follow the same async pattern ---

async def set_channel_settings(channel: int, limit: float, voltage: float, current: float):
    stub = await _get_stub()
    try:
        request = instrument_pb2.ChannelRequest(
            channel=channel,
            voltage_limit=limit,
            voltage=voltage,
            current=current,
        )
        response = await stub.SetChannel(request)
        return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def set_output(channel: int, state: bool):
    stub = await _get_stub()
    try:
        request = instrument_pb2.OutputRequest(channel=channel, state=state)
        response = await stub.SetOutput(request)
        return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def set_current_channel(channel: int):
    stub = await _get_stub()
    try:
        request = instrument_pb2.SetChannelRequest(channel=channel)
        response = await stub.SetCurrentChannel(request)
        return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def get_plot_data(channel: int):
    stub = await _get_stub()
    try:
        request = instrument_pb2.PlotDataRequest(channel=channel)
        response = await stub.GetPlotData(request)
        return {"time": list(response.time), "voltage": list(response.voltage)}
    except grpc.aio.AioRpcError:
        return {"time": [], "voltage": []}

async def clear_data():
    stub = await _get_stub()
    try:
        response = await stub.ClearData(instrument_pb2.Empty())
        return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"