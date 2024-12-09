# -*- coding: utf-8 -*-
"""

@file: Forthink UWB Dongle Sniffer session use UCI (UWB Command Interface)

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import math
import struct
from uci_defs import *

def get_trx_bitmap_str(bitmap):
    bitmap_str = ''
    if bitmap == 0:
        bitmap_str = 'SUCCESS'
    else:
        if bitmap & 0x01:
            bitmap_str += 'RX_TOA_DETECT_FAILED'
        if bitmap & 0x02:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_SIGNAL_LOST'
        if bitmap & 0x04:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_PRMBL_TIMEOUT'
        if bitmap & 0x08:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_SFD_TIMEOUT'
        if bitmap & 0x10:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_SECDED_DECODE_FAILURE'
        if bitmap & 0x20:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_RS_DECODE_FAILURE'
        if bitmap & 0x40:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_DECODE_CHAIN_FAILURE'
        if bitmap & 0x80:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_DATA_BUFFER_OVERFLOW'
        if bitmap & 0x100:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'RX_STS_MISMATCH'
        if bitmap & 0x800:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'TX_ERROR'
        if bitmap & 0xA000:
            if bitmap_str:
                bitmap_str += '| '
            bitmap_str += 'TX_PAYLOAD_LENGTH_ERROR'
    return bitmap_str

class SnifferRxResult():

    def __init__(self, status, rx_status, rx_frame_num, rx_err_num, min_overall_rssi, max_overall_rssi, min_noise_rssi, max_noise_rssi, payload_len, payload):
        self.status = status
        self.rx_status = rx_status
        self.rx_frame_num = rx_frame_num
        self.rx_err_num = rx_err_num
        self.min_overall_rssi = min_overall_rssi
        self.max_overall_rssi = max_overall_rssi
        self.min_noise_rssi = min_noise_rssi
        self.max_noise_rssi = max_noise_rssi
        self.payload_len = payload_len
        self.payload = payload

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        status = struct.unpack("<B", byte_stream[0:1])[0]
        rx_status = struct.unpack("<H", byte_stream[4:6])[0]
        if status == EnumUciStatus.UCI_STATUS_OK.value:
            rx_frame_num = struct.unpack("<B", byte_stream[6:7])[0]
            rx_err_num = struct.unpack("<B", byte_stream[7:8])[0]
            min_overall_rssi = struct.unpack("<i", byte_stream[8:12])[0]
            min_overall_rssi *= 10 * math.log10(2) / (2 ** 25)
            max_overall_rssi = struct.unpack("<i", byte_stream[16:20])[0]
            max_overall_rssi *= 10 * math.log10(2) / (2 ** 25)
            min_noise_rssi = struct.unpack("<i", byte_stream[20:24])[0]
            min_noise_rssi *= 10 * math.log10(2) / (2 ** 25)
            max_noise_rssi = struct.unpack("<i", byte_stream[28:32])[0]
            max_noise_rssi *= 10 * math.log10(2) / (2 ** 25)
            payload_len = struct.unpack("<B", byte_stream[32:33])[0]
            if payload_len > 0:
                payload = byte_stream[33:33 + payload_len]
            else:
                payload = None
        else:
            rx_frame_num = None
            rx_err_num = None
            min_overall_rssi = None
            max_overall_rssi = None
            min_noise_rssi = None
            max_noise_rssi = None
            payload_len = None
            payload = None
        return SnifferRxResult(status, rx_status, rx_frame_num, rx_err_num, min_overall_rssi, max_overall_rssi, min_noise_rssi, max_noise_rssi, payload_len, payload)

    def __str__(self) -> str:
        # rx status is a bit field
        rx_status_str = get_trx_bitmap_str(self.rx_status)
        payload_str = ', '.join([f'0x{byte:02x}' for byte in self.payload]) if self.payload else None
        if self.status!= EnumUciStatus.UCI_STATUS_OK.value:
            return f" RX_RESULT:\n" \
                + f"          status: {EnumUciStatus(self.status).name}\n" \
                + f"       rx_status: {rx_status_str}\n"
        return f" RX_RESULT:\n" \
            + f"          status: {EnumUciStatus(self.status).name}\n" \
            + f"       rx_status: {rx_status_str}\n" \
            + f"    rx_frame_num: {self.rx_frame_num}\n" \
            + f"      rx_err_num: {self.rx_err_num}\n" \
            + f"min_overall_rssi: {self.min_overall_rssi:{'.2f'}} dBm\n" \
            + f"max_overall_rssi: {self.max_overall_rssi:{'.2f'}} dBm\n" \
            + f"  min_noise_rssi: {self.min_noise_rssi:{'.2f'}} dBm\n" \
            + f"  max_noise_rssi: {self.max_noise_rssi:{'.2f'}} dBm\n" \
            + f"     payload_len: {self.payload_len}\n" \
            + f"         payload: {payload_str}\n"
    
class SnifferTxResult():
    def __init__(self, status, tx_status):
        self.status = status
        self.tx_status = tx_status

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        status = struct.unpack("<B", byte_stream[0:1])[0]
        if len(byte_stream) > 4:
            tx_status = struct.unpack("<H", byte_stream[4:6])[0]
        else:
            tx_status = None
        return SnifferTxResult(status, tx_status)
    
    def __str__(self) -> str:
        if self.tx_status == 0x0000:
            tx_status_str = 'TX_SUCCESS'
        elif self.tx_status == 0x8000:
            tx_status_str = 'TX_ERROR'
        else:
            tx_status_str = 'None'
        return f" TX_RESULT:\n" \
            + f"          status: {EnumUciStatus(self.status).name}\n" \
            + f"       tx_status: {tx_status_str}\n"

class SnifferRangingStatusResult():
    def __init__(self, status, rx_status_list):
        self.status = status
        self.rx_status_list = rx_status_list

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        status = struct.unpack("<B", byte_stream[0:1])[0]
        rx_status_list = []
        for i in range(round((len(byte_stream)-4)/2)):
            rx_status_list.append(struct.unpack("<H", byte_stream[4+2*i:6+2*i])[0])
        return SnifferRangingStatusResult(status, rx_status_list)
        
    
    def __str__(self) -> str:
        if self.status != EnumUciStatus.UCI_STATUS_OK.value:
            return f" RANGING_STATUS_RESULT:\n" \
                 + f"          status: {EnumUciStatus(self.status).name}\n"
        rx_status_str = ''
        for rx_status in self.rx_status_list:
            rx_status_str += get_trx_bitmap_str(rx_status) + '\t\t'
        return f" RANGING_STATUS_RESULT:\n" \
            + f"          status: {EnumUciStatus(self.status).name}\n" \
            + f"  rx_status_list: {rx_status_str}"

class SnifferRangingResult():
    def __init__(self, status, rx_result_list):
        self.status = status
        self.rx_result_list = rx_result_list

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        status = struct.unpack("<B", byte_stream[0:1])[0]
        rx_result_list = []
        for i in range(round((len(byte_stream)-4)/4) - 1):
            rx_result_list.append(struct.unpack("<I", byte_stream[4+4*i:8+4*i])[0])
        return SnifferRangingResult(status, rx_result_list)
    
    def __str__(self) -> str:
        if self.status!= EnumUciStatus.UCI_STATUS_OK.value:
            return f" RANGING_RESULT:\n" \
                 + f"          status: {EnumUciStatus(self.status).name}\n"
        rx_result_str = ''
        for rx_result in self.rx_result_list:
            rx_result_str += str(rx_result) + '\t\t'
        return f" RANGING_RESULT:\n" \
            + f"          status: {EnumUciStatus(self.status).name}\n" \
            + f"rx_timestamp_dif: {rx_result_str}"

class SnifferPayload():
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload

    @staticmethod
    def from_bytes(byte_stream):
        if not isinstance(byte_stream, bytes):
            byte_stream = bytes(byte_stream)
        status = struct.unpack("<B", byte_stream[0:1])[0]
        payload = byte_stream[4:]
        return SnifferPayload(status, payload)
    
    def __str__(self) -> str:
        if self.status!= EnumUciStatus.UCI_STATUS_OK.value:
            return f" PAYLOAD_RESULT:\n" \
                + f"          status: {EnumUciStatus(self.status).name}\n"
        payload_str = ', '.join([f'0x{byte:02x}' for byte in self.payload])
        return f" PAYLOAD_RESULT:\n" \
            + f"          status: {EnumUciStatus(self.status).name}\n" \
            + f"          payload: {payload_str}\n"