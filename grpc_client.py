import grpc
import json
import instrument_pb2
import instrument_pb2_grpc

GRPC_ADDRESS = 'localhost:50051'

async def list_devices():
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel)
            response = await stub.ListDevices(instrument_pb2.Empty())
            return list(response.devices)
    except grpc.aio.AioRpcError as e:
        return [f"gRPC Error: {e.details()}"]

async def connect_remote_device(address: str):
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel)
            request = instrument_pb2.DeviceRequest(address=address)
            response = await stub.ConnectDevice(request)
            return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def disconnect_remote_device():
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel)
            response = await stub.DisconnectDevice(instrument_pb2.Empty())
            return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def get_status():
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel)
            response = await stub.GetStatus(instrument_pb2.Empty())
            return json.loads(response.status)
    except (grpc.aio.AioRpcError, json.JSONDecodeError):
        return {"connected": False} # Return a safe default

# --- All other functions follow the same async pattern ---

async def set_channel_settings(channel: int, limit: float, voltage: float, current: float):
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel_conn:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel_conn)
            request = instrument_pb2.ChannelRequest(
                channel=channel, voltage_limit=limit, voltage=voltage, current=current)
            response = await stub.SetChannel(request)
            return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def set_output(channel: int, state: bool):
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel_conn:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel_conn)
            request = instrument_pb2.OutputRequest(channel=channel, state=state)
            response = await stub.SetOutput(request)
            return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def set_current_channel(channel: int):
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel_conn:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel_conn)
            request = instrument_pb2.SetChannelRequest(channel=channel)
            response = await stub.SetCurrentChannel(request)
            return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"

async def get_plot_data(channel: int):
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel_conn:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel_conn)
            request = instrument_pb2.PlotDataRequest(channel=channel)
            response = await stub.GetPlotData(request)
            return {"time": list(response.time), "voltage": list(response.voltage)}
    except grpc.aio.AioRpcError:
        return {"time": [], "voltage": []}

async def clear_data():
    try:
        async with grpc.aio.insecure_channel(GRPC_ADDRESS) as channel_conn:
            stub = instrument_pb2_grpc.InstrumentServiceStub(channel_conn)
            response = await stub.ClearData(instrument_pb2.Empty())
            return response.success, response.message
    except grpc.aio.AioRpcError as e:
        return False, f"gRPC Error: {e.details()}"