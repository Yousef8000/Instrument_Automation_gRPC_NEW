import grpc
from concurrent import futures
import json
import instrument_pb2
import instrument_pb2_grpc
import services.instrument as instr_module

class InstrumentServiceServicer(instrument_pb2_grpc.InstrumentServiceServicer):

    def ListDevices(self, request, context):
        """Handles the device scan request."""
        try:
            # This call is now much more reliable.
            devices = instr_module.list_devices()
            return instrument_pb2.DeviceListResponse(devices=devices)
        except Exception as e:
            # If PyVISA fails, send the error message to the UI.
            error_message = f"VISA Error: {e}"
            print(f"[gRPC Server] ERROR during ListDevices: {error_message}")
            return instrument_pb2.DeviceListResponse(devices=[error_message])

    def ConnectDevice(self, request, context):
        """Handles the connection request."""
        try:
            idn = instr_module.connect_device(request.address)
            return instrument_pb2.ConnectionResponse(success=True, message=idn)
        except Exception as e:
            # The instrument service now raises exceptions on failure.
            print(f"[gRPC Server] ERROR during ConnectDevice: {e}")
            return instrument_pb2.ConnectionResponse(success=False, message=str(e))

    def DisconnectDevice(self, request, context):
        instr_module.disconnect_device()
        return instrument_pb2.ConnectionResponse(success=True, message="Disconnected successfully.")

    def GetStatus(self, request, context):
        status_dict = instr_module.get_status()
        return instrument_pb2.StatusResponse(status=json.dumps(status_dict))

    # --- All other methods simply pass through ---
    def SetChannel(self, request, context):
        success, message = instr_module.set_channel_settings(
            request.channel, request.voltage_limit, request.voltage, request.current)
        return instrument_pb2.ChannelResponse(success=success, message=message)

    def SetOutput(self, request, context):
        success, message = instr_module.set_output(request.channel, request.state)
        return instrument_pb2.OutputResponse(success=success, message=message)

    def SetCurrentChannel(self, request, context):
        success, message = instr_module.set_current_channel(request.channel)
        return instrument_pb2.ConnectionResponse(success=success, message=message)

    def GetPlotData(self, request, context):
        plot_data = instr_module.get_plot_data(request.channel)
        return instrument_pb2.PlotDataResponse(
            time=plot_data["time"], voltage=plot_data["voltage"], channel=request.channel)

    def ClearData(self, request, context):
        instr_module.clear_data()
        return instrument_pb2.ConnectionResponse(success=True, message="Plot data cleared.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    instrument_pb2_grpc.add_InstrumentServiceServicer_to_server(InstrumentServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051. Press Ctrl+C to stop.")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()