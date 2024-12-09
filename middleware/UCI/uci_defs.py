# -*- coding: utf-8 -*-
"""

@file: uci definitions

@brief: This file contains the definition from UCI specification

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum
import nxp_crc

## @defgroup Forthink_UCI
# This is forthink UWB Communication Interface Common Class and Functions.
# @{

class EnumUciStatus(IntEnum):
    '''
        UCI Rangging Status Enum, <UCI generic specification 8.5 Table 32>
        usage example:
        status = UciRangingStatus(rcv_data[i])
        if status == UciRangingStatus.UCI_STATUS_OK:
            pass
    '''
    # CORE Generic status codes
    UCI_STATUS_OK = 0x00
    UCI_STATUS_REJECTED = 0x01
    UCI_STATUS_FAILED = 0x02
    UCI_STATUS_SYNTAX_ERROR = 0x03
    UCI_STATUS_INVALID_PARAM = 0x04
    UCI_STATUS_INVALID_RANGE = 0x05
    UCI_STATUS_INVALID_MESSAGE_SIZE = 0x06
    UCI_STATUS_UNKNOWN_GID = 0x07
    UCI_STATUS_UNKNOWN_OID = 0x08
    UCI_STATUS_READ_ONLY = 0x09
    UCI_STATUS_COMMAND_RETRY = 0x0A
    UCI_STATUS_UNKNOWN = 0x0B
    UCI_STATUS_NOT_APPLICABLE = 0x0C

    # UWB session specific status codes
    UCI_STATUS_ERROR_SESSION_NOT_EXIST = 0x11
    UCI_STATUS_ERROR_SESSION_DUPLICATE = 0x12   # session already exist/created
    UCI_STATUS_ERROR_SESSION_ACTIVE = 0x13
    UCI_STATUS_ERROR_MAX_SESSIONS_EXCEEDED = 0x14
    UCI_STATUS_ERROR_SESSION_NOT_CONFIGURED = 0x15
    UCI_STATUS_ERROR_ACTIVE_SESSIONS_ONGOING = 0x16
    UCI_STATUS_ERROR_MULTICAST_LIST_FULL = 0x17
    UCI_STATUS_ERROR_ADDRESS_NOT_FOUND = 0x18
    UCI_STATUS_ERROR_ADDRESS_ALREADY_PRESENT = 0x19
    UCI_STATUS_ERROR_UWB_INITIATION_TIME_TOO_OLD = 0x1A
    UCI_STATUS_OK_NEGATIVE_DISTANCE_REPORT = 0x1B
    UCI_STATUS_INVALID_STS_IDX = 0x1C # <NXP CCC UCI>

    # UWB ranging session specific status codes
    UCI_STATUS_RANGING_TX_FAILED = 0x20
    UCI_STATUS_RANGING_RX_TIMEOUT = 0x21
    UCI_STATUS_RANGING_RX_PHY_DEC_FAILED = 0x22
    UCI_STATUS_RANGING_RX_PHY_TOA_FAILED = 0x23
    UCI_STATUS_RANGING_RX_PHY_STS_FAILED = 0x24
    UCI_STATUS_RANGING_RX_MAC_DEC_FAILED = 0x25
    UCI_STATUS_RANGING_RX_MAC_IE_DEC_FAILED = 0x26
    UCI_STATUS_RANGING_RX_MAC_IE_MISSING = 0x27

    # Vendor specific status codes
    UCI_STATUS_INVALID_RESPONDER_SLOT_INDEX = 0xA0
    ## Forthink Vendor specific status codes
    UCI_STATUS_LICENSE_NEED = 0xA1
    UCI_STATUS_LICENSE_VERIFIED_FAILED = 0xA2
    UCI_STATUS_INVALID_PUBLIC_KEY = 0xA3
    UCI_STATUS_SN_TOO_LONG = 0xA4
    # UCI_STATUS_SLOT_LEN_NOT_SUPPORTED = 0xA1
    # UCI_STATUS_INVALID_SLOT_PER_RR = 0xA2
    # UCI_STATUS_INVALID_STS_IDX = 0xA3
    # UCI_STATUS_RESPONDER_LISTEN_ONLY_MODE = 0xA4

    # Proprietary status codes
    UCI_STATUS_RANGING_CONSISTENCY_CHECK_FAILED = 0xE1

    # NXP Testware status codes
    UCI_STATUS_VERIFICATION_FAILED = 0x7D
    UCI_STATUS_REBOOT = 0x80
    UCI_STATUS_REBOOT_WDT = 0x81
    UCI_STATUS_CRC_ERROR = 0xF8
    UCI_STATUS_NOT_IMPLEMENTED = 0xFE
    UCI_STATUS_UNDEF = 0xFF


class EnumDeviceState(IntEnum):
    '''
        Device State Values, FiRa Consortium UCI Generic Specification Table 10
    '''
    DEVICE_STATE_RFU = 0x00
    DEVICE_STATE_READY = 0x01
    DEVICE_STATE_ACTIVE = 0x02
    DEVICE_STATE_ERROR = 0xFF


class EnumUciMessageType(IntEnum):
    '''
        UCI Message Type
    '''
    UCI_MT_COMMAND = 0x01
    UCI_MT_RESPONSE = 0x02
    UCI_MT_NOTIFICATION = 0x03
    UCI_MT_UNDEF = 0xFF


class EnumUciGid(IntEnum):
    '''
        UCI GID
    '''
    CORE_GENERIC_GID = 0x00
    UWB_SESSION_GID = 0x01
    UWB_RANGE_GID = 0x02
    FORTHINK_VENDOR_GID = 0x0A
    VENDOR_B_GID = 0x0B
    VENDOR_C_GID = 0x0C
    RF_TEST_GID = 0x0D
    UWB_SNIFFER_GID = 0x0E
    VENDOR_F_GID = 0x0F


class EnumSnifferOid(IntEnum):
    '''
        UCI UWB Sniffer Group-0x0E: opcodes
    '''
    SNIFFER_RESET_STATUS_NTF_OID = 0x00
    SNIFFER_REBOOT_OID = 0x01
    SNIFFER_GET_REBOOT_REASON_OID = 0x02
    SNIFFER_GET_VERSION_OID = 0x03
    SNIFFER_GET_RADIO_CFG_VERSION_OID = 0x04
    SNIFFER_CFG_GPIO_OID = 0x05
    SNIFFER_READ_GPIO_OID = 0x06
    SNIFFER_SET_GPIO_OID = 0x07
    SNIFFER_ENTER_POWER_MODE_OID = 0x0A
    SNIFFER_XO_CONTROL_CMD_OID = 0x0B
    SNIFFER_SET_CURRENT_LIMIT_OID = 0x0C
    SNIFFER_VERIFY_IMAGE_CHECKSUM_OID = 0x0D
    SNIFFER_SET_CRC_CFG_OID = 0x0E
    SNIFFER_SET_TX_SLOTS_OUTPUT_POWER_OID = 0x0F
    SNIFFER_STORE_RADIO_SETTINGS_OID = 0x10
    SNIFFER_SET_BUFFER_OID = 0x12
    SNIFFER_GET_BUFFER_OID = 0x13
    SNIFFER_CLEAR_BUFFER_OID = 0x14
    SNIFFER_CFG_TX_MODE_OID = 0x18
    SNIFFER_START_TX_MODE_OID = 0x19
    SNIFFER_CFG_RX_MODE_OID = 0x1A
    SNIFFER_START_RX_MODE_OID = 0x1B
    SNIFFER_STORE_PROTECTION_KEY_OID = 0x1C
    SNIFFER_SET_EPOCH_ID_OID = 0x1D
    SNIFFER_STORE_KEY_OID = 0x1E
    SNIFFER_DELETE_KEY_OID = 0x1F
    SNIFFER_IMPORT_KEY_OID = 0x20
    SNIFFER_EVICT_KEY_OID = 0x21
    SNIFFER_EVICT_ALL_KEYS_OID = 0x22
    SNIFFER_CFG_STS_OID = 0x23
    SNIFFER_SET_PAYLOAD_OID = 0x26
    SNIFFER_GET_PAYLOAD_OID = 0x27
    SNIFFER_CFG_RANGING_APP_OID = 0x28
    SNIFFER_RESET_RANGING_APP_CFG_OID = 0x29
    SNIFFER_CFG_RANGING_SEQ_OID = 0x2D
    SNIFFER_START_RANGING_OID = 0x2E
    SNIFFER_LOOPBACK_OID = 0x30
    SNIFFER_START_LOOPBACK_OID = 0x31
    SNIFFER_GET_RANGING_STATUS_OID = 0x35
    SNIFFER_GET_RANGING_RESULT_OID = 0x36
    SNIFFER_GET_CIR_OID = 0x37
    SNIFFER_GET_CFO_OID = 0x38
    SNIFFER_GET_FIRST_PATH_INFO_OID = 0x39
    SNIFFER_STORE_RANGING_APP_SETTINGS_OID = 0x3A
    SNIFFER_CLEAR_RANGING_APP_SETTINGS_OID = 0x3B
    
    
class InvalidFormatError(Exception):
    def __init__(self, input: str = ""):
        message = "Error, invalid format! " + input
        super().__init__(message)

class UciMessage:
    def __init__(self, message_type: EnumUciMessageType, packet_boundary_flag: int, gid: int, payload_extension: int, oid: int, payload_length: int, payload: list[int], uci_packets: list = None, response_status: EnumUciStatus = None):
        self.message_type = message_type
        self.packet_boundary_flag = packet_boundary_flag
        self.gid = gid
        self.payload_extension = payload_extension
        self.oid = oid
        self.payload_length = payload_length
        self.response_status = response_status
        self.payload = payload
        self.uci_packets = uci_packets
        self.to_byte_stream()

    @classmethod
    def from_bytes(cls, bytes: list[int], remove_crc: bool = False, prior_pbf: bool = False):
        uci_packets = [bytes]
        bytes = bytes[:-2] if remove_crc == True else bytes
        if len(bytes) >= 4:
            message_type = EnumUciMessageType.UCI_MT_UNDEF
            try:
                message_type = EnumUciMessageType(((bytes[0] & 0xe0) >> 5))
            except ValueError as e:
                print("unsupported message type, ValueError: ", e)
            packet_boundary_flag = (bytes[0] & 0x10) >> 4
            gid = bytes[0] & 0x0f
            payload_extension = ((bytes[1] & 0x80) >> 7)
            oid = bytes[1] & 0x3f
            payload_length = bytes[3] + (bytes[2] << 8)
            response_status = None
            # check if a status field is required in case it is a response
            if message_type == EnumUciMessageType.UCI_MT_RESPONSE and prior_pbf == False:
                response_status = EnumUciStatus(bytes[4] & 0xFF)
                payload = bytes[4:]
                # if len(bytes) >= 5:
                #     response_status = EnumUciStatus(bytes[4] & 0xFF)
                #     payload = bytes[5:]
                # else:
                #     raise InvalidFormatError("UCI response status missing!")
            else:
                payload = bytes[4:]
        else:
            raise InvalidFormatError("UCI Input message too short!")
        
        return UciMessage(message_type=message_type,
                          packet_boundary_flag=packet_boundary_flag,
                          gid=gid,
                          payload_extension=payload_extension,
                          oid=oid,
                          payload_length=payload_length,
                          payload=payload,
                          uci_packets=uci_packets,
                          response_status=response_status)

    def __str__(self):
        return "message type: " + str(self.message_type.name) + " (" + str("0x{:02x}".format(self.message_type.value)) + ")\n" \
            + "packet boundary flag: " + str(self.packet_boundary_flag) + "\n" \
            + "gid: " + str("0x{:02x}".format(self.gid)) + "\n" \
            + "payload extension: " + str(self.payload_extension) + "\n" \
            + "oid: " + str("0x{:02x}".format(self.oid)) + "\n" \
            + "payload length: " + str(self.payload_length) + " bytes (" + str("0x{:02x}".format(self.payload_length)) + ")\n" \
            + "payload: " + str(["0x{:02x}".format(x) for x in self.payload])

    def to_byte_stream(self, append_crc=False):
        self.byte_stream: list[int] = []
        # assemble the byte stream
        self.byte_stream.append(self.message_type.value <<
                                5 | self.packet_boundary_flag << 4 | self.gid)
        self.byte_stream.append(self.payload_extension << 7 | self.oid)
        # check for extended payload size
        if (self.payload_extension > 0):
            self.byte_stream.append((self.payload_length & 0xFF00) >> 8)
        else:
            self.byte_stream.append(0)
        self.byte_stream.append(self.payload_length & 0x00FF)
        if self.response_status is not None:
            self.byte_stream.append(self.response_status.value & 0xFF)
        self.byte_stream += self.payload
        if append_crc:
            crc: int = nxp_crc.calculate_crc(frame=self.byte_stream)
            self.byte_stream += crc.to_bytes(2, 'little')
        return self.byte_stream

class UciRspNtfResult:
    
    def __init__(self, message_type: EnumUciMessageType, gid: int, oid: int, response_status: EnumUciStatus, result = None):
        self.message_type = message_type
        self.gid = gid
        self.oid = oid
        self.status = response_status
        self.uci_result = result
        
    def __str__(self) -> str:
        return "message type: " + str(self.message_type.name) + " (" + str("0x{:02x}".format(self.message_type.value)) + ")\n" \
            + "gid: " + str("0x{:02x}".format(self.gid)) + "\n" \
            + "oid: " + str("0x{:02x}".format(self.oid)) + "\n" \
            + "status: " + str(self.status.name) + " (" + str("0x{:02x}".format(self.status.value)) + ")\n" \
            + "payload: " + str(self.uci_result)

# @}

