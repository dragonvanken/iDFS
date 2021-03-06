# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MasterForClient.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='MasterForClient.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x15MasterForClient.proto\"\n\n\x08\x45mptyArg\"%\n\x03Str\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08isFolder\x18\x02 \x01(\x08\"G\n)getChunkInfoAndAllocatedDataServerRequest\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12\x0c\n\x04path\x18\x02 \x01(\t\"~\n\rChunkStructor\x12\x11\n\tChunkSize\x18\x01 \x01(\x05\x12\x0f\n\x07\x43hunkId\x18\x02 \x01(\x05\x12\r\n\x05inFID\x18\x03 \x01(\x05\x12\x0e\n\x06offset\x18\x04 \x01(\x05\x12\x10\n\x08StoreDID\x18\x05 \x01(\x05\x12\n\n\x02ip\x18\x06 \x01(\t\x12\x0c\n\x04port\x18\x07 \x01(\x05\"*\n\x08\x46ilePath\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x10\n\x08isFolder\x18\x02 \x01(\x08\"$\n\x03\x41\x43K\x12\x10\n\x08\x66\x65\x65\x64\x42\x61\x63k\x18\x01 \x01(\x08\x12\x0b\n\x03msg\x18\x02 \x01(\t\"#\n\x13\x64ownloadRequestInfo\x12\x0c\n\x04path\x18\x01 \x01(\t\"Z\n\ntargetInfo\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x12\x11\n\tChunkSize\x18\x03 \x01(\x05\x12\x0f\n\x07\x43hunkId\x18\x04 \x01(\x05\x12\x0e\n\x06status\x18\x05 \x01(\x08\"*\n\x13\x63reateFolderRequest\x12\x13\n\x0b\x64\x65stination\x18\x01 \x01(\t2\xa2\x02\n\x03MFC\x12\"\n\x0bgetFiletree\x12\t.EmptyArg\x1a\x04.Str\"\x00\x30\x01\x12\x64\n\"getChunkInfoAndAllocatedDataServer\x12*.getChunkInfoAndAllocatedDataServerRequest\x1a\x0e.ChunkStructor\"\x00\x30\x01\x12,\n\x0c\x63reateFolder\x12\x14.createFolderRequest\x1a\x04.ACK\"\x00\x12\x42\n\x19requestDownloadFromMaster\x12\x14.downloadRequestInfo\x1a\x0b.targetInfo\"\x00\x30\x01\x12\x1f\n\ndeleteFile\x12\t.FilePath\x1a\x04.ACK\"\x00\x62\x06proto3')
)




_EMPTYARG = _descriptor.Descriptor(
  name='EmptyArg',
  full_name='EmptyArg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=35,
)


_STR = _descriptor.Descriptor(
  name='Str',
  full_name='Str',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Str.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isFolder', full_name='Str.isFolder', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=74,
)


_GETCHUNKINFOANDALLOCATEDDATASERVERREQUEST = _descriptor.Descriptor(
  name='getChunkInfoAndAllocatedDataServerRequest',
  full_name='getChunkInfoAndAllocatedDataServerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='getChunkInfoAndAllocatedDataServerRequest.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='getChunkInfoAndAllocatedDataServerRequest.path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=147,
)


_CHUNKSTRUCTOR = _descriptor.Descriptor(
  name='ChunkStructor',
  full_name='ChunkStructor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ChunkSize', full_name='ChunkStructor.ChunkSize', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ChunkId', full_name='ChunkStructor.ChunkId', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inFID', full_name='ChunkStructor.inFID', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='offset', full_name='ChunkStructor.offset', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='StoreDID', full_name='ChunkStructor.StoreDID', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ip', full_name='ChunkStructor.ip', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='ChunkStructor.port', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=275,
)


_FILEPATH = _descriptor.Descriptor(
  name='FilePath',
  full_name='FilePath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='FilePath.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isFolder', full_name='FilePath.isFolder', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=277,
  serialized_end=319,
)


_ACK = _descriptor.Descriptor(
  name='ACK',
  full_name='ACK',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feedBack', full_name='ACK.feedBack', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='msg', full_name='ACK.msg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=321,
  serialized_end=357,
)


_DOWNLOADREQUESTINFO = _descriptor.Descriptor(
  name='downloadRequestInfo',
  full_name='downloadRequestInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='downloadRequestInfo.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=359,
  serialized_end=394,
)


_TARGETINFO = _descriptor.Descriptor(
  name='targetInfo',
  full_name='targetInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='targetInfo.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='targetInfo.port', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ChunkSize', full_name='targetInfo.ChunkSize', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ChunkId', full_name='targetInfo.ChunkId', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='targetInfo.status', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=396,
  serialized_end=486,
)


_CREATEFOLDERREQUEST = _descriptor.Descriptor(
  name='createFolderRequest',
  full_name='createFolderRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='destination', full_name='createFolderRequest.destination', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=488,
  serialized_end=530,
)

DESCRIPTOR.message_types_by_name['EmptyArg'] = _EMPTYARG
DESCRIPTOR.message_types_by_name['Str'] = _STR
DESCRIPTOR.message_types_by_name['getChunkInfoAndAllocatedDataServerRequest'] = _GETCHUNKINFOANDALLOCATEDDATASERVERREQUEST
DESCRIPTOR.message_types_by_name['ChunkStructor'] = _CHUNKSTRUCTOR
DESCRIPTOR.message_types_by_name['FilePath'] = _FILEPATH
DESCRIPTOR.message_types_by_name['ACK'] = _ACK
DESCRIPTOR.message_types_by_name['downloadRequestInfo'] = _DOWNLOADREQUESTINFO
DESCRIPTOR.message_types_by_name['targetInfo'] = _TARGETINFO
DESCRIPTOR.message_types_by_name['createFolderRequest'] = _CREATEFOLDERREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EmptyArg = _reflection.GeneratedProtocolMessageType('EmptyArg', (_message.Message,), {
  'DESCRIPTOR' : _EMPTYARG,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:EmptyArg)
  })
_sym_db.RegisterMessage(EmptyArg)

Str = _reflection.GeneratedProtocolMessageType('Str', (_message.Message,), {
  'DESCRIPTOR' : _STR,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:Str)
  })
_sym_db.RegisterMessage(Str)

getChunkInfoAndAllocatedDataServerRequest = _reflection.GeneratedProtocolMessageType('getChunkInfoAndAllocatedDataServerRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCHUNKINFOANDALLOCATEDDATASERVERREQUEST,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:getChunkInfoAndAllocatedDataServerRequest)
  })
_sym_db.RegisterMessage(getChunkInfoAndAllocatedDataServerRequest)

ChunkStructor = _reflection.GeneratedProtocolMessageType('ChunkStructor', (_message.Message,), {
  'DESCRIPTOR' : _CHUNKSTRUCTOR,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:ChunkStructor)
  })
_sym_db.RegisterMessage(ChunkStructor)

FilePath = _reflection.GeneratedProtocolMessageType('FilePath', (_message.Message,), {
  'DESCRIPTOR' : _FILEPATH,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:FilePath)
  })
_sym_db.RegisterMessage(FilePath)

ACK = _reflection.GeneratedProtocolMessageType('ACK', (_message.Message,), {
  'DESCRIPTOR' : _ACK,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:ACK)
  })
_sym_db.RegisterMessage(ACK)

downloadRequestInfo = _reflection.GeneratedProtocolMessageType('downloadRequestInfo', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOADREQUESTINFO,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:downloadRequestInfo)
  })
_sym_db.RegisterMessage(downloadRequestInfo)

targetInfo = _reflection.GeneratedProtocolMessageType('targetInfo', (_message.Message,), {
  'DESCRIPTOR' : _TARGETINFO,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:targetInfo)
  })
_sym_db.RegisterMessage(targetInfo)

createFolderRequest = _reflection.GeneratedProtocolMessageType('createFolderRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEFOLDERREQUEST,
  '__module__' : 'MasterForClient_pb2'
  # @@protoc_insertion_point(class_scope:createFolderRequest)
  })
_sym_db.RegisterMessage(createFolderRequest)



_MFC = _descriptor.ServiceDescriptor(
  name='MFC',
  full_name='MFC',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=533,
  serialized_end=823,
  methods=[
  _descriptor.MethodDescriptor(
    name='getFiletree',
    full_name='MFC.getFiletree',
    index=0,
    containing_service=None,
    input_type=_EMPTYARG,
    output_type=_STR,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getChunkInfoAndAllocatedDataServer',
    full_name='MFC.getChunkInfoAndAllocatedDataServer',
    index=1,
    containing_service=None,
    input_type=_GETCHUNKINFOANDALLOCATEDDATASERVERREQUEST,
    output_type=_CHUNKSTRUCTOR,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='createFolder',
    full_name='MFC.createFolder',
    index=2,
    containing_service=None,
    input_type=_CREATEFOLDERREQUEST,
    output_type=_ACK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='requestDownloadFromMaster',
    full_name='MFC.requestDownloadFromMaster',
    index=3,
    containing_service=None,
    input_type=_DOWNLOADREQUESTINFO,
    output_type=_TARGETINFO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='deleteFile',
    full_name='MFC.deleteFile',
    index=4,
    containing_service=None,
    input_type=_FILEPATH,
    output_type=_ACK,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MFC)

DESCRIPTOR.services_by_name['MFC'] = _MFC

# @@protoc_insertion_point(module_scope)
