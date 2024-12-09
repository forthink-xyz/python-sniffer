# -*- coding: utf-8 -*-
"""

@file:   UCI Message Class and callbacks

@author: luochao

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from uci_defs import *
from console_helper import *
from uci_sniffer_rx_rsp import *
import struct


# @defgroup Forthink_UCI
# This is forthink UWB Communication Interface message Class and callbacks ( RESPONSE/NOTIFICATION ).
# @{

# UCI Sniffer-Group RSP/NTF callbacks
def uci_sniffer_reset_status_ntf_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x6E 0x00
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"SNIFFER_RESET_STATUS_NTF: Status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_NOTIFICATION, gid, oid, status)


def uci_sniffer_cfg_tx_mode_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x18
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"SNIFFER_CFG_TX_MODE_RSP: Status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status)

def uci_sniffer_start_tx_mode_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x19
    '''
    tx_result = SnifferTxResult.from_bytes(payload)
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, tx_result.status, tx_result)

def uci_sniffer_cfg_rx_mode_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x1A
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"SNIFFER_CFG_RX_MODE_RSP: Status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status)

def uci_sniffer_start_rx_mode_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x1B
    '''
    rx_result = SnifferRxResult.from_bytes(payload)
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, rx_result.status, rx_result)


def uci_sniffer_cfg_ranging_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x28
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"SNIFFER_CFG_RANGING_RSP: Status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status)

def uci_sniffer_cfg_ranging_seq_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x2D
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"SNIFFER_CFG_RANGING_SEQ_RSP: Status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status)

def uci_sniffer_start_ranging_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x2E
    '''
    status = EnumUciStatus(payload[0])
    log_i(f"SNIFFER_START_RANGING_RSP: Status: {status.name}")
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, status)

def uci_sniffer_get_ranging_status_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x35
    '''
    rx_status = SnifferRangingStatusResult.from_bytes(payload)
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, rx_status.status, rx_status)

def uci_sniffer_get_ranging_result_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x36
    '''
    rx_results = SnifferRangingResult.from_bytes(payload)
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, rx_results.status, rx_results)

def uci_sniffer_get_payload_rsp_callback(gid: int, oid: int, payload: list[int]):
    '''
        GID OID: 0x4E 0x27
    '''
    rx_payload = SnifferPayload.from_bytes(payload)
    return UciRspNtfResult(EnumUciMessageType.UCI_MT_RESPONSE, gid, oid, rx_payload.status, rx_payload)


# @}
