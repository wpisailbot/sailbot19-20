# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MessagesServices.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import TrimTabMessages_pb2 as TrimTabMessages__pb2
import ArduinoMessages_pb2 as ArduinoMessages__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='MessagesServices.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x16MessagesServices.proto\x1a\x15TrimTabMessages.proto\x1a\x15\x41rduinoMessages.proto\"\xdb\x06\n\nAirmarData\x12\x35\n\x0c\x61pparentWind\x18\x01 \x01(\x0b\x32\x1f.AirmarData.ApparentWind_Airmar\x12\x34\n\x0ftheoreticalWind\x18\x02 \x01(\x0b\x32\x1b.AirmarData.TheoreticalWind\x12\x12\n\nbaro_press\x18\x03 \x01(\x02\x12,\n\x0btemperature\x18\x04 \x01(\x0b\x32\x17.AirmarData.Temperature\x12\x1c\n\x03gps\x18\x05 \x01(\x0b\x32\x0f.AirmarData.GPS\x12$\n\x07\x63ompass\x18\x06 \x01(\x0b\x32\x13.AirmarData.Compass\x12.\n\x0c\x61\x63\x63\x65leration\x18\x07 \x01(\x0b\x32\x18.AirmarData.Acceleration\x12(\n\trateGyros\x18\t \x01(\x0b\x32\x15.AirmarData.RateGyros\x12(\n\tpitchRoll\x18\n \x01(\x0b\x32\x15.AirmarData.PitchRoll\x12\x0f\n\x07rel_hum\x18\x0b \x01(\x02\x1a\x37\n\x13\x41pparentWind_Airmar\x12\r\n\x05speed\x18\x01 \x01(\x02\x12\x11\n\tdirection\x18\x02 \x01(\x02\x1a\x33\n\x0fTheoreticalWind\x12\r\n\x05speed\x18\x01 \x01(\x02\x12\x11\n\tdirection\x18\x02 \x01(\x02\x1a\x33\n\x0bTemperature\x12\x10\n\x08\x61ir_temp\x18\x01 \x01(\x02\x12\x12\n\nwind_chill\x18\x02 \x01(\x02\x1aY\n\x03GPS\x12\x0b\n\x03lat\x18\x01 \x01(\x02\x12\x0b\n\x03lon\x18\x02 \x01(\x02\x12\x0b\n\x03\x61lt\x18\x03 \x01(\x02\x12\x14\n\x0cground_speed\x18\x04 \x01(\x02\x12\x15\n\rground_course\x18\x05 \x01(\x02\x1a*\n\x07\x43ompass\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x1a/\n\x0c\x41\x63\x63\x65leration\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x1a@\n\tRateGyros\x12\x0f\n\x07phi_dot\x18\x01 \x01(\x02\x12\x11\n\ttheta_dot\x18\x02 \x01(\x02\x12\x0f\n\x07psi_dot\x18\x03 \x01(\x02\x1a(\n\tPitchRoll\x12\r\n\x05pitch\x18\x01 \x01(\x02\x12\x0c\n\x04roll\x18\x02 \x01(\x02\"M\n\rControlValues\x12\x13\n\x0brudderAngle\x18\x01 \x01(\x02\x12\x11\n\ttrimAngle\x18\x02 \x01(\x02\x12\x14\n\x0c\x62\x61llastAngle\x18\x03 \x01(\x02\" \n\x08Readings\x12\x14\n\x0c\x61pparentWind\x18\x01 \x01(\x02\"\x1d\n\x0eServer_request\x12\x0b\n\x03req\x18\x01 \x01(\x08\x32?\n\x0c\x41irmarReader\x12/\n\rGetAirmarData\x12\x0f.Server_request\x1a\x0b.AirmarData\"\x00\x32K\n\x15\x41utonomousValueReader\x12\x32\n\x13GetAutonomousValues\x12\t.Readings\x1a\x0e.ControlValues\"\x00\x32\x9f\x01\n\tPWMReader\x12,\n\x0cGetPWMInputs\x12\x0e.ControlAngles\x1a\n.PWMValues\"\x00\x12-\n\x0cGetPWMValues\x12\x0f.Server_request\x1a\n.PWMValues\"\x00\x12\x35\n\x10GetControlAngles\x12\x0f.Server_request\x1a\x0e.ControlAngles\"\x00\x32\xaf\x01\n\rTrimTabGetter\x12\x35\n\x11SetTrimTabSetting\x12\n.TrimState\x1a\x12.ApparentWind_Trim\"\x00\x12-\n\x0cGetTrimState\x12\x0f.Server_request\x1a\n.TrimState\"\x00\x12\x38\n\x0fGetApparentWind\x12\x0f.Server_request\x1a\x12.ApparentWind_Trim\"\x00\x62\x06proto3')
  ,
  dependencies=[TrimTabMessages__pb2.DESCRIPTOR,ArduinoMessages__pb2.DESCRIPTOR,])




_AIRMARDATA_APPARENTWIND_AIRMAR = _descriptor.Descriptor(
  name='ApparentWind_Airmar',
  full_name='AirmarData.ApparentWind_Airmar',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='speed', full_name='AirmarData.ApparentWind_Airmar.speed', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='direction', full_name='AirmarData.ApparentWind_Airmar.direction', index=1,
      number=2, type=2, cpp_type=6, label=1,
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
  serialized_start=479,
  serialized_end=534,
)

_AIRMARDATA_THEORETICALWIND = _descriptor.Descriptor(
  name='TheoreticalWind',
  full_name='AirmarData.TheoreticalWind',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='speed', full_name='AirmarData.TheoreticalWind.speed', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='direction', full_name='AirmarData.TheoreticalWind.direction', index=1,
      number=2, type=2, cpp_type=6, label=1,
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
  serialized_start=536,
  serialized_end=587,
)

_AIRMARDATA_TEMPERATURE = _descriptor.Descriptor(
  name='Temperature',
  full_name='AirmarData.Temperature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='air_temp', full_name='AirmarData.Temperature.air_temp', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wind_chill', full_name='AirmarData.Temperature.wind_chill', index=1,
      number=2, type=2, cpp_type=6, label=1,
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
  serialized_start=589,
  serialized_end=640,
)

_AIRMARDATA_GPS = _descriptor.Descriptor(
  name='GPS',
  full_name='AirmarData.GPS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lat', full_name='AirmarData.GPS.lat', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lon', full_name='AirmarData.GPS.lon', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alt', full_name='AirmarData.GPS.alt', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ground_speed', full_name='AirmarData.GPS.ground_speed', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ground_course', full_name='AirmarData.GPS.ground_course', index=4,
      number=5, type=2, cpp_type=6, label=1,
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
  serialized_start=642,
  serialized_end=731,
)

_AIRMARDATA_COMPASS = _descriptor.Descriptor(
  name='Compass',
  full_name='AirmarData.Compass',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='AirmarData.Compass.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='AirmarData.Compass.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z', full_name='AirmarData.Compass.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=733,
  serialized_end=775,
)

_AIRMARDATA_ACCELERATION = _descriptor.Descriptor(
  name='Acceleration',
  full_name='AirmarData.Acceleration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='AirmarData.Acceleration.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='AirmarData.Acceleration.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z', full_name='AirmarData.Acceleration.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=777,
  serialized_end=824,
)

_AIRMARDATA_RATEGYROS = _descriptor.Descriptor(
  name='RateGyros',
  full_name='AirmarData.RateGyros',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='phi_dot', full_name='AirmarData.RateGyros.phi_dot', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='theta_dot', full_name='AirmarData.RateGyros.theta_dot', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='psi_dot', full_name='AirmarData.RateGyros.psi_dot', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=826,
  serialized_end=890,
)

_AIRMARDATA_PITCHROLL = _descriptor.Descriptor(
  name='PitchRoll',
  full_name='AirmarData.PitchRoll',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pitch', full_name='AirmarData.PitchRoll.pitch', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='roll', full_name='AirmarData.PitchRoll.roll', index=1,
      number=2, type=2, cpp_type=6, label=1,
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
  serialized_start=892,
  serialized_end=932,
)

_AIRMARDATA = _descriptor.Descriptor(
  name='AirmarData',
  full_name='AirmarData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='apparentWind', full_name='AirmarData.apparentWind', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='theoreticalWind', full_name='AirmarData.theoreticalWind', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='baro_press', full_name='AirmarData.baro_press', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature', full_name='AirmarData.temperature', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gps', full_name='AirmarData.gps', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='compass', full_name='AirmarData.compass', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acceleration', full_name='AirmarData.acceleration', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rateGyros', full_name='AirmarData.rateGyros', index=7,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pitchRoll', full_name='AirmarData.pitchRoll', index=8,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rel_hum', full_name='AirmarData.rel_hum', index=9,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_AIRMARDATA_APPARENTWIND_AIRMAR, _AIRMARDATA_THEORETICALWIND, _AIRMARDATA_TEMPERATURE, _AIRMARDATA_GPS, _AIRMARDATA_COMPASS, _AIRMARDATA_ACCELERATION, _AIRMARDATA_RATEGYROS, _AIRMARDATA_PITCHROLL, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=932,
)


_CONTROLVALUES = _descriptor.Descriptor(
  name='ControlValues',
  full_name='ControlValues',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rudderAngle', full_name='ControlValues.rudderAngle', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trimAngle', full_name='ControlValues.trimAngle', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ballastAngle', full_name='ControlValues.ballastAngle', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=934,
  serialized_end=1011,
)


_READINGS = _descriptor.Descriptor(
  name='Readings',
  full_name='Readings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='apparentWind', full_name='Readings.apparentWind', index=0,
      number=1, type=2, cpp_type=6, label=1,
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
  serialized_start=1013,
  serialized_end=1045,
)


_SERVER_REQUEST = _descriptor.Descriptor(
  name='Server_request',
  full_name='Server_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='req', full_name='Server_request.req', index=0,
      number=1, type=8, cpp_type=7, label=1,
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
  serialized_start=1047,
  serialized_end=1076,
)

_AIRMARDATA_APPARENTWIND_AIRMAR.containing_type = _AIRMARDATA
_AIRMARDATA_THEORETICALWIND.containing_type = _AIRMARDATA
_AIRMARDATA_TEMPERATURE.containing_type = _AIRMARDATA
_AIRMARDATA_GPS.containing_type = _AIRMARDATA
_AIRMARDATA_COMPASS.containing_type = _AIRMARDATA
_AIRMARDATA_ACCELERATION.containing_type = _AIRMARDATA
_AIRMARDATA_RATEGYROS.containing_type = _AIRMARDATA
_AIRMARDATA_PITCHROLL.containing_type = _AIRMARDATA
_AIRMARDATA.fields_by_name['apparentWind'].message_type = _AIRMARDATA_APPARENTWIND_AIRMAR
_AIRMARDATA.fields_by_name['theoreticalWind'].message_type = _AIRMARDATA_THEORETICALWIND
_AIRMARDATA.fields_by_name['temperature'].message_type = _AIRMARDATA_TEMPERATURE
_AIRMARDATA.fields_by_name['gps'].message_type = _AIRMARDATA_GPS
_AIRMARDATA.fields_by_name['compass'].message_type = _AIRMARDATA_COMPASS
_AIRMARDATA.fields_by_name['acceleration'].message_type = _AIRMARDATA_ACCELERATION
_AIRMARDATA.fields_by_name['rateGyros'].message_type = _AIRMARDATA_RATEGYROS
_AIRMARDATA.fields_by_name['pitchRoll'].message_type = _AIRMARDATA_PITCHROLL
DESCRIPTOR.message_types_by_name['AirmarData'] = _AIRMARDATA
DESCRIPTOR.message_types_by_name['ControlValues'] = _CONTROLVALUES
DESCRIPTOR.message_types_by_name['Readings'] = _READINGS
DESCRIPTOR.message_types_by_name['Server_request'] = _SERVER_REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AirmarData = _reflection.GeneratedProtocolMessageType('AirmarData', (_message.Message,), {

  'ApparentWind_Airmar' : _reflection.GeneratedProtocolMessageType('ApparentWind_Airmar', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_APPARENTWIND_AIRMAR,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.ApparentWind_Airmar)
    })
  ,

  'TheoreticalWind' : _reflection.GeneratedProtocolMessageType('TheoreticalWind', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_THEORETICALWIND,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.TheoreticalWind)
    })
  ,

  'Temperature' : _reflection.GeneratedProtocolMessageType('Temperature', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_TEMPERATURE,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.Temperature)
    })
  ,

  'GPS' : _reflection.GeneratedProtocolMessageType('GPS', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_GPS,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.GPS)
    })
  ,

  'Compass' : _reflection.GeneratedProtocolMessageType('Compass', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_COMPASS,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.Compass)
    })
  ,

  'Acceleration' : _reflection.GeneratedProtocolMessageType('Acceleration', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_ACCELERATION,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.Acceleration)
    })
  ,

  'RateGyros' : _reflection.GeneratedProtocolMessageType('RateGyros', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_RATEGYROS,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.RateGyros)
    })
  ,

  'PitchRoll' : _reflection.GeneratedProtocolMessageType('PitchRoll', (_message.Message,), {
    'DESCRIPTOR' : _AIRMARDATA_PITCHROLL,
    '__module__' : 'MessagesServices_pb2'
    # @@protoc_insertion_point(class_scope:AirmarData.PitchRoll)
    })
  ,
  'DESCRIPTOR' : _AIRMARDATA,
  '__module__' : 'MessagesServices_pb2'
  # @@protoc_insertion_point(class_scope:AirmarData)
  })
_sym_db.RegisterMessage(AirmarData)
_sym_db.RegisterMessage(AirmarData.ApparentWind_Airmar)
_sym_db.RegisterMessage(AirmarData.TheoreticalWind)
_sym_db.RegisterMessage(AirmarData.Temperature)
_sym_db.RegisterMessage(AirmarData.GPS)
_sym_db.RegisterMessage(AirmarData.Compass)
_sym_db.RegisterMessage(AirmarData.Acceleration)
_sym_db.RegisterMessage(AirmarData.RateGyros)
_sym_db.RegisterMessage(AirmarData.PitchRoll)

ControlValues = _reflection.GeneratedProtocolMessageType('ControlValues', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLVALUES,
  '__module__' : 'MessagesServices_pb2'
  # @@protoc_insertion_point(class_scope:ControlValues)
  })
_sym_db.RegisterMessage(ControlValues)

Readings = _reflection.GeneratedProtocolMessageType('Readings', (_message.Message,), {
  'DESCRIPTOR' : _READINGS,
  '__module__' : 'MessagesServices_pb2'
  # @@protoc_insertion_point(class_scope:Readings)
  })
_sym_db.RegisterMessage(Readings)

Server_request = _reflection.GeneratedProtocolMessageType('Server_request', (_message.Message,), {
  'DESCRIPTOR' : _SERVER_REQUEST,
  '__module__' : 'MessagesServices_pb2'
  # @@protoc_insertion_point(class_scope:Server_request)
  })
_sym_db.RegisterMessage(Server_request)



_AIRMARREADER = _descriptor.ServiceDescriptor(
  name='AirmarReader',
  full_name='AirmarReader',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1078,
  serialized_end=1141,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAirmarData',
    full_name='AirmarReader.GetAirmarData',
    index=0,
    containing_service=None,
    input_type=_SERVER_REQUEST,
    output_type=_AIRMARDATA,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AIRMARREADER)

DESCRIPTOR.services_by_name['AirmarReader'] = _AIRMARREADER


_AUTONOMOUSVALUEREADER = _descriptor.ServiceDescriptor(
  name='AutonomousValueReader',
  full_name='AutonomousValueReader',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=1143,
  serialized_end=1218,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAutonomousValues',
    full_name='AutonomousValueReader.GetAutonomousValues',
    index=0,
    containing_service=None,
    input_type=_READINGS,
    output_type=_CONTROLVALUES,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUTONOMOUSVALUEREADER)

DESCRIPTOR.services_by_name['AutonomousValueReader'] = _AUTONOMOUSVALUEREADER


_PWMREADER = _descriptor.ServiceDescriptor(
  name='PWMReader',
  full_name='PWMReader',
  file=DESCRIPTOR,
  index=2,
  serialized_options=None,
  serialized_start=1221,
  serialized_end=1380,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetPWMInputs',
    full_name='PWMReader.GetPWMInputs',
    index=0,
    containing_service=None,
    input_type=ArduinoMessages__pb2._CONTROLANGLES,
    output_type=ArduinoMessages__pb2._PWMVALUES,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetPWMValues',
    full_name='PWMReader.GetPWMValues',
    index=1,
    containing_service=None,
    input_type=_SERVER_REQUEST,
    output_type=ArduinoMessages__pb2._PWMVALUES,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetControlAngles',
    full_name='PWMReader.GetControlAngles',
    index=2,
    containing_service=None,
    input_type=_SERVER_REQUEST,
    output_type=ArduinoMessages__pb2._CONTROLANGLES,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PWMREADER)

DESCRIPTOR.services_by_name['PWMReader'] = _PWMREADER


_TRIMTABGETTER = _descriptor.ServiceDescriptor(
  name='TrimTabGetter',
  full_name='TrimTabGetter',
  file=DESCRIPTOR,
  index=3,
  serialized_options=None,
  serialized_start=1383,
  serialized_end=1558,
  methods=[
  _descriptor.MethodDescriptor(
    name='SetTrimTabSetting',
    full_name='TrimTabGetter.SetTrimTabSetting',
    index=0,
    containing_service=None,
    input_type=TrimTabMessages__pb2._TRIMSTATE,
    output_type=TrimTabMessages__pb2._APPARENTWIND_TRIM,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetTrimState',
    full_name='TrimTabGetter.GetTrimState',
    index=1,
    containing_service=None,
    input_type=_SERVER_REQUEST,
    output_type=TrimTabMessages__pb2._TRIMSTATE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetApparentWind',
    full_name='TrimTabGetter.GetApparentWind',
    index=2,
    containing_service=None,
    input_type=_SERVER_REQUEST,
    output_type=TrimTabMessages__pb2._APPARENTWIND_TRIM,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRIMTABGETTER)

DESCRIPTOR.services_by_name['TrimTabGetter'] = _TRIMTABGETTER

# @@protoc_insertion_point(module_scope)
