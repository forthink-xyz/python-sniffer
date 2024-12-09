import struct

from console_helper import *

from uci_defs import *
from uci_port import *
from uci_message import *

class UCILayer():

    def __init__(self, device: UCIDevice):
        self.device = device
        self.device_serial_num = ""
        self.device_license = ""
        self.rsp_callback_table = {}
        self.ntf_callback_table = {}
        # register default notification callbacks
        ## 0xE - sniffer group
        self.register_notification_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_RESET_STATUS_NTF_OID.value, uci_sniffer_reset_status_ntf_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_CFG_RANGING_APP_OID.value, uci_sniffer_cfg_ranging_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_CFG_RX_MODE_OID.value, uci_sniffer_cfg_rx_mode_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_START_RX_MODE_OID.value, uci_sniffer_start_rx_mode_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_CFG_TX_MODE_OID.value, uci_sniffer_cfg_tx_mode_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_START_TX_MODE_OID.value, uci_sniffer_start_tx_mode_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_CFG_RANGING_SEQ_OID.value, uci_sniffer_cfg_ranging_seq_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_START_RANGING_OID.value, uci_sniffer_start_ranging_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_GET_RANGING_STATUS_OID.value, uci_sniffer_get_ranging_status_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_GET_RANGING_RESULT_OID.value, uci_sniffer_get_ranging_result_rsp_callback)
        self.register_response_callback(EnumUciGid.UWB_SNIFFER_GID.value, EnumSnifferOid.SNIFFER_GET_PAYLOAD_OID.value, uci_sniffer_get_payload_rsp_callback)
        

    def register_response_callback(self, gid: int, oid: int, callback):
        '''
            @brief callback  func(gid, oid, payload: list[int])
        '''
        index = gid * 256 + oid
        # if callback already exists, overwrite it
        self.rsp_callback_table[index] = callback

    def register_notification_callback(self, gid: int, oid: int, callback):
        '''
            @brief callback func(gid, oid, payload: list[int])
        '''
        index = gid * 256 + oid
        self.ntf_callback_table[index] = callback

    def wait_response(self, timeout_ms=200, crc_enabled=False):
        result = self.device.receive_uci_message(timeout_ms, crc_enabled)
        rsp_ntf_result = UciRspNtfResult(EnumUciMessageType.UCI_MT_UNDEF, 0, 0, EnumUciStatus.UCI_STATUS_FAILED, [])
        if result.status == EnumUCIPortStatus.UCI_PORT_STATUS_OK:
            msg = UciMessage.from_bytes(result.msg_buffer)
            if msg is not None:
                if msg.message_type == EnumUciMessageType.UCI_MT_RESPONSE:
                    index = msg.gid * 256 + msg.oid
                    if index in self.rsp_callback_table:
                        rsp_ntf_result = self.rsp_callback_table[index](msg.gid, msg.oid, msg.payload)
                    else:
                        log_i("UCI Layer: recv a response, no callback, GID: " + hex(msg.gid) + " OID: " + hex(msg.oid) + " payload len: " + str(msg.payload_length))
                        rsp_ntf_result = UciRspNtfResult(msg.message_type, msg.gid, msg.oid, EnumUciStatus.UCI_STATUS_NOT_IMPLEMENTED, msg.payload)
                elif msg.message_type == EnumUciMessageType.UCI_MT_NOTIFICATION:
                    index = msg.gid * 256 + msg.oid
                    if index in self.ntf_callback_table:
                        rsp_ntf_result = self.ntf_callback_table[index](msg.gid, msg.oid, msg.payload)
                    else:
                        log_i("UCI Layer: recv a notification, no callback, GID: " + hex(msg.gid) + " OID:" + hex(msg.oid) + " payload len: " + str(msg.payload_length))
                        rsp_ntf_result = UciRspNtfResult(msg.message_type, msg.gid, msg.oid, EnumUciStatus.UCI_STATUS_NOT_IMPLEMENTED, msg.payload)
                else:
                    log_e(f"UCI Layer: unknown message type: {msg.message_type}")
                    return UciRspNtfResult(msg.message_type, msg.gid, msg.oid, EnumUciStatus.UCI_STATUS_UNKNOWN)
            else:
                log_e("UCI Layer: invalid message received!")
        else:
            log_e(f"UCI Layer: wait response failed, status: {result.status.name}")
        return rsp_ntf_result


    def uci_layer_user_defined_cmd(self, gid: int, oid: int, payload: list[int]):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, gid, 0, oid, len(payload), payload)
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    # UCI Sniffer Commands
    def uci_sniffer_cfg_ranging_app(self, cfg: list[int]):
        buf = []
        buf += cfg
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_CFG_RANGING_APP_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
        
    def uci_sniffer_cfg_rx_mode(self, cfg: list[int]):
        buf = []
        buf += cfg
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_CFG_RX_MODE_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_sniffer_start_rx_mode(self):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_START_RX_MODE_OID.value, 0, [])
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    def uci_sniffer_cfg_tx_mode(self, cfg: list[int]):
        buf = []
        buf += cfg
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_CFG_TX_MODE_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_sniffer_start_tx_mode(self, cfg: list[int]):
        buf = []
        buf += cfg
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_START_TX_MODE_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    def uci_sniffer_cfg_ranging_seq(self, cfg: list[int]):
        buf = []
        buf += cfg
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_CFG_RANGING_SEQ_OID.value, len(buf), buf)
        return self.device.transmit_uci_command(msg.to_byte_stream())
    
    def uci_sniffer_start_ranging(self):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_START_RANGING_OID.value, 0, [])
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_sniffer_get_ranging_status(self):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_GET_RANGING_STATUS_OID.value, 0, [])
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_sniffer_get_ranging_result(self):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_GET_RANGING_RESULT_OID.value, 0, [])
        return self.device.transmit_uci_command(msg.to_byte_stream())

    def uci_sniffer_get_payload(self, index):
        msg = UciMessage(EnumUciMessageType.UCI_MT_COMMAND, 0, EnumUciGid.UWB_SNIFFER_GID.value, 0,
                            EnumSnifferOid.SNIFFER_GET_PAYLOAD_OID.value, 1, [index])
        return self.device.transmit_uci_command(msg.to_byte_stream())


