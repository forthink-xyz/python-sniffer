# -*- coding: utf-8 -*-
"""

@file: sniffer device Class

@author: duanqiyi

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from console_helper import *

from SnifferRegionParams import *
from uci_message import *
from uci_defs import *
from uci_layer import UCILayer

class SnifferParam():

    def __init__(self, channel):
        self.channel_id = channel
        self.sfd_id = 0
        self.preamble_id = 9
        self.tx_power = 14
        self.tx_num = 5
        self.tx_interval = 10000

    def set_tx_power(self, dbm: int):
        '''
            TX power (-12 ~ 14 dBm)
        '''
        if dbm < -12 or dbm > 14:
            raise ValueError('Invalid value for TX power. Must be between -12 ~ 14 dBm')
        self.tx_power = dbm

    def set_sfd_id(self, sfd_id: int):
        '''
            sfd_id: 0, 2
        '''
        if sfd_id not in [0, 2]:
            raise ValueError('Invalid value for SFD ID. Must be 0 or 2')
        self.sfd_id = sfd_id

    def set_preamble_id(self, preamble_id: int):
        '''
            preamble_id: 9 ~ 24
        '''
        if preamble_id < 9 or preamble_id > 24:
            raise ValueError('Invalid value for preamble ID. Must be between 9 ~ 24')
        self.preamble_id = preamble_id

    def set_tx_num(self, tx_num: int):
        '''
            tx_num: 0 ~ 0xFF; if set to 0, it weill repeat indefinitely until reset device, and it will not return any response
        '''
        if tx_num < 0 or tx_num > 0xFF:
            raise ValueError('Invalid value for TX number. Must be between 0 ~ 0xFF')
        self.tx_num = tx_num

    def set_tx_interval(self, tx_interval: int):
        '''
            tx_interval: 0 ~ 0xFFFFFF us
        '''
        if tx_interval < 0 or tx_interval > 0xFFFFFF:
            raise ValueError('Invalid value for TX interval. Must be between 0 ~ 0xFFFFFF')
        self.tx_interval = tx_interval

class SnifferDevice(UCILayer):
    def __init__(self, device):
        super().__init__(device)
        self.dev = device

    def sniffer_cfg_ranging_app(self, channel_id: int, tx_power: int):
        '''
            config sniffer ranging parameters
        '''
        match channel_id:
            case 5:
                frequency = 6489600
            case 6:
                frequency = 6988800
            case 8:
                frequency = 7488000
            case 9:
                frequency = 7987200
            case default:
                log_e('Error: Invalid channel id.')
                return
        tx_ramp_up = 80     # tx ramp-up time: 80us
        rx_ramp_up = 100    # rx ramp-up time: 100us
        tx_power_value = tx_power * 4 # tx power value: 0.25dBm/step
        cfg = []
        cfg += struct.pack('<IBHHbBBBB', frequency, 
                           EnumSnifferPllMode.SNIFFER_PLL_MODE_ON.value, 
                           tx_ramp_up, rx_ramp_up, tx_power_value, 
                           EnumSnifferNBICMode.SNIFFER_NBIC_DISABLE.value,
                           EnumSnifferPayloadCipherMode.SNIFFER_PAYLOAD_CIPHER_DISABLE.value,
                           EnumSnifferTXTempCompMode.SNIFFER_TX_TEMP_COMP_DISABLE.value,
                           EnumSnifferXTALTempCompMode.SNIFFER_XTAL_TEMP_COMP_ENABLE.value)
        self.uci_sniffer_cfg_ranging_app(cfg)

        result = self.wait_response(timeout_ms=200)
        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))


    def sniffer_cfg_rx_mode(self, preamble_id: int, sfd_id: int):
        '''
            config sniffer rx mode
        '''
        radio = sfd_id + 4                  # Radio select depends on default radio setting, in this case, sfd 0 is radio 0x04 and sfd 2 is radio 0x06
        preamble_index = preamble_id - 8    # Preamble index depends on default preamble setting, in this case, preamble 9 is index 1 and preamble 24 is index 16
        sts_offset = 0
        rx_delay = 0                        # Execute rx immediately
        timeout = 0xFFFFFF                  # Rx timeout: 16777215us, ~ 16.7ms
        rx_cycles = 1                       # Rx cycles: 1
        cfg = []
        cfg += struct.pack('<BBBBHIBBB', radio, preamble_index, sts_offset,
                           EnumSnifferToaAlgorithmMode.SNIFFER_TOA_ALGORITHM_ENABLE.value,
                           rx_delay, timeout, rx_cycles,
                           EnumSnifferPayloadCipherMode.SNIFFER_PAYLOAD_CIPHER_DISABLE.value,
                           EnumSnifferXTALTempCompMode.SNIFFER_XTAL_TEMP_COMP_ENABLE.value)
        self.uci_sniffer_cfg_rx_mode(cfg)

        result = self.wait_response(timeout_ms=200)
        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))

    def sniffer_start_rx_mode(self):
        '''
            start sniffer rx mode
        '''
        self.uci_sniffer_start_rx_mode()

        result = self.wait_response(timeout_ms=17000)

        return result

    def sniffer_cfg_tx_mode(self, preamble_id: int, sfd_id: int, tx_num: int, tx_interval: int):
        '''
            config sniffer tx mode
        '''
        radio = sfd_id + 4 + 0x10           # Radio select depends on default radio setting, in this case, sfd 0 is radio 0x14 and sfd 2 is radio 0x16
        preamble_index = preamble_id - 8    # Preamble index depends on default preamble setting, in this case, preamble 9 is index 1 and preamble 24 is index 16
        sts_offset = 0
        tx_delay = tx_interval              # tx delay between each frame
        timeout = 0xFFFFFF                  # Tx timeout: 16777215us
        tx_cycles = tx_num                  
        cfg = []
        cfg += struct.pack('<BBBBHIBBBBB', radio, preamble_index, sts_offset,
                           EnumSnifferToaAlgorithmMode.SNIFFER_TOA_ALGORITHM_ENABLE.value,
                           tx_delay, timeout, tx_cycles,
                           EnumSnifferTXTempCompMode.SNIFFER_TX_TEMP_COMP_DISABLE.value,
                           EnumSnifferPayloadCipherMode.SNIFFER_PAYLOAD_CIPHER_DISABLE.value,
                           EnumSnifferTXTempCompMode.SNIFFER_TX_TEMP_COMP_DISABLE.value,
                           EnumSnifferXTALTempCompMode.SNIFFER_XTAL_TEMP_COMP_ENABLE.value)
        self.uci_sniffer_cfg_tx_mode(cfg)

        result = self.wait_response(timeout_ms=200)
        if result.status is not EnumUciStatus.UCI_STATUS_OK:
            log_e("Error: " + str(result.status))

    def sniffer_start_tx_mode(self, payload):
        '''
            start sniffer tx mode
        '''
        payload_len = len(payload)
        if payload_len > 127 or payload_len < 2:
            raise ValueError("Payload length must be between 2 ~ 127 bytes")
        data = []
        data += struct.pack('<B', payload_len)
        data += payload
        self.uci_sniffer_start_tx_mode(data)

        result = self.wait_response(timeout_ms=200)
        return result
    
    def sniffer_generate_ranging_cmd(self, preamble_id: int, sfd_id: int, delay: int, timeout: int, psdu_index: int):
        '''
            generate ranging command
        '''
        radio = sfd_id + 4           # Radio select depends on default radio setting, in this case, sfd 0 is radio 0x04 and sfd 2 is radio 0x06
        preamble_index = preamble_id - 8    # Preamble index depends on default preamble setting, in this case, preamble 9 is index 1 and preamble 24 is index 16
        sts_offset = 0
        cfg = []
        cfg += struct.pack('<BBBBHIBB', 
                           EnumSnifferRangingActionMode.SNIFFER_RANGING_ACTION_RX_WITHOUT_TOA.value,
                           radio, preamble_index, sts_offset, round(delay), round(timeout),
                           EnumSnifferDataInPSDUMode.SNIFFER_DATA_IN_PSDU_PRE_PSDU_AND_TIMESTAMPS.value,
                           psdu_index)
        return cfg
    
    def sniffer_cfg_ranging_seq(self, cfg):
        '''
            config ranging sequence
        '''
        self.uci_sniffer_cfg_ranging_seq(cfg)

        result = self.wait_response(timeout_ms=200)
        return result
    
    def sniffer_start_ranging(self):
        '''
            start ranging
        '''
        self.uci_sniffer_start_ranging()

        result = self.wait_response(timeout_ms=17000)
        return result

    def sniffer_get_ranging_status(self):
        '''
            get ranging status
        '''
        self.uci_sniffer_get_ranging_status()

        result = self.wait_response(timeout_ms=200)
        return result
    
    def sniffer_get_ranging_result(self):
        '''
            get ranging timestamp result
        '''
        self.uci_sniffer_get_ranging_result()

        result = self.wait_response(timeout_ms=200)
        return result
    
    def sniffer_get_payload(self, index: int):
        '''
            get payload
        '''
        self.uci_sniffer_get_payload(index)

        result = self.wait_response(timeout_ms=200)
        return result
