# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PWMMessages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='PWMMessages.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x11PWMMessages.proto\"Y\n\tPWMValues\x12\x0b\n\x03\x63h1\x18\x01 \x01(\x02\x12\x0b\n\x03\x63h2\x18\x02 \x01(\x02\x12\x0b\n\x03\x63h3\x18\x03 \x01(\x02\x12\x0b\n\x03\x63h4\x18\x04 \x01(\x02\x12\x0b\n\x03\x63h5\x18\x05 \x01(\x02\x12\x0b\n\x03\x63h6\x18\x06 \x01(\x02\x62\x06proto3')
)




_PWMVALUES = _descriptor.Descriptor(
  name='PWMValues',
  full_name='PWMValues',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ch1', full_name='PWMValues.ch1', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ch2', full_name='PWMValues.ch2', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ch3', full_name='PWMValues.ch3', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ch4', full_name='PWMValues.ch4', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ch5', full_name='PWMValues.ch5', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ch6', full_name='PWMValues.ch6', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=21,
  serialized_end=110,
)

DESCRIPTOR.message_types_by_name['PWMValues'] = _PWMVALUES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PWMValues = _reflection.GeneratedProtocolMessageType('PWMValues', (_message.Message,), {
  'DESCRIPTOR' : _PWMVALUES,
  '__module__' : 'PWMMessages_pb2'
  # @@protoc_insertion_point(class_scope:PWMValues)
  })
_sym_db.RegisterMessage(PWMValues)


# @@protoc_insertion_point(module_scope)