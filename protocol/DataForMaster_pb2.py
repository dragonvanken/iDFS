# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: DataForMaster.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='DataForMaster.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x13\x44\x61taForMaster.proto\"\n\n\x08\x45mptyArg\"\x13\n\x03Str\x12\x0c\n\x04name\x18\x01 \x01(\t2\x05\n\x03\x44\x46Mb\x06proto3')
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
  serialized_start=23,
  serialized_end=33,
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
  serialized_start=35,
  serialized_end=54,
)

DESCRIPTOR.message_types_by_name['EmptyArg'] = _EMPTYARG
DESCRIPTOR.message_types_by_name['Str'] = _STR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EmptyArg = _reflection.GeneratedProtocolMessageType('EmptyArg', (_message.Message,), {
  'DESCRIPTOR' : _EMPTYARG,
  '__module__' : 'DataForMaster_pb2'
  # @@protoc_insertion_point(class_scope:EmptyArg)
  })
_sym_db.RegisterMessage(EmptyArg)

Str = _reflection.GeneratedProtocolMessageType('Str', (_message.Message,), {
  'DESCRIPTOR' : _STR,
  '__module__' : 'DataForMaster_pb2'
  # @@protoc_insertion_point(class_scope:Str)
  })
_sym_db.RegisterMessage(Str)



_DFM = _descriptor.ServiceDescriptor(
  name='DFM',
  full_name='DFM',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=56,
  serialized_end=61,
  methods=[
])
_sym_db.RegisterServiceDescriptor(_DFM)

DESCRIPTOR.services_by_name['DFM'] = _DFM

# @@protoc_insertion_point(module_scope)
