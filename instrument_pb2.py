# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: instrument.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'instrument.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10instrument.proto\"\x07\n\x05\x45mpty\" \n\x0eStatusResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"Z\n\x0e\x43hannelRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x12\x15\n\rvoltage_limit\x18\x02 \x01(\x02\x12\x0f\n\x07voltage\x18\x03 \x01(\x02\x12\x0f\n\x07\x63urrent\x18\x04 \x01(\x02\"3\n\x0f\x43hannelResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"%\n\x12\x44\x65viceListResponse\x12\x0f\n\x07\x64\x65vices\x18\x01 \x03(\t\" \n\rDeviceRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\"6\n\x12\x43onnectionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"/\n\rOutputRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x12\r\n\x05state\x18\x02 \x01(\x08\"2\n\x0eOutputResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\"\n\x0fPlotDataRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\"B\n\x10PlotDataResponse\x12\x0c\n\x04time\x18\x01 \x03(\t\x12\x0f\n\x07voltage\x18\x02 \x03(\x02\x12\x0f\n\x07\x63hannel\x18\x03 \x01(\x05\"$\n\x11SetChannelRequest\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x32\xf6\x03\n\x11InstrumentService\x12-\n\x0eInitializeVISA\x12\x06.Empty\x1a\x13.ConnectionResponse\x12*\n\x0bListDevices\x12\x06.Empty\x1a\x13.DeviceListResponse\x12\x34\n\rConnectDevice\x12\x0e.DeviceRequest\x1a\x13.ConnectionResponse\x12/\n\x10\x44isconnectDevice\x12\x06.Empty\x1a\x13.ConnectionResponse\x12$\n\tGetStatus\x12\x06.Empty\x1a\x0f.StatusResponse\x12/\n\nSetChannel\x12\x0f.ChannelRequest\x1a\x10.ChannelResponse\x12,\n\tSetOutput\x12\x0e.OutputRequest\x1a\x0f.OutputResponse\x12<\n\x11SetCurrentChannel\x12\x12.SetChannelRequest\x1a\x13.ConnectionResponse\x12\x32\n\x0bGetPlotData\x12\x10.PlotDataRequest\x1a\x11.PlotDataResponse\x12(\n\tClearData\x12\x06.Empty\x1a\x13.ConnectionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'instrument_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=20
  _globals['_EMPTY']._serialized_end=27
  _globals['_STATUSRESPONSE']._serialized_start=29
  _globals['_STATUSRESPONSE']._serialized_end=61
  _globals['_CHANNELREQUEST']._serialized_start=63
  _globals['_CHANNELREQUEST']._serialized_end=153
  _globals['_CHANNELRESPONSE']._serialized_start=155
  _globals['_CHANNELRESPONSE']._serialized_end=206
  _globals['_DEVICELISTRESPONSE']._serialized_start=208
  _globals['_DEVICELISTRESPONSE']._serialized_end=245
  _globals['_DEVICEREQUEST']._serialized_start=247
  _globals['_DEVICEREQUEST']._serialized_end=279
  _globals['_CONNECTIONRESPONSE']._serialized_start=281
  _globals['_CONNECTIONRESPONSE']._serialized_end=335
  _globals['_OUTPUTREQUEST']._serialized_start=337
  _globals['_OUTPUTREQUEST']._serialized_end=384
  _globals['_OUTPUTRESPONSE']._serialized_start=386
  _globals['_OUTPUTRESPONSE']._serialized_end=436
  _globals['_PLOTDATAREQUEST']._serialized_start=438
  _globals['_PLOTDATAREQUEST']._serialized_end=472
  _globals['_PLOTDATARESPONSE']._serialized_start=474
  _globals['_PLOTDATARESPONSE']._serialized_end=540
  _globals['_SETCHANNELREQUEST']._serialized_start=542
  _globals['_SETCHANNELREQUEST']._serialized_end=578
  _globals['_INSTRUMENTSERVICE']._serialized_start=581
  _globals['_INSTRUMENTSERVICE']._serialized_end=1083
# @@protoc_insertion_point(module_scope)
