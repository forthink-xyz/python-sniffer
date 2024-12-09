# -*- coding: utf-8 -*-
"""

@file: Sniffer Region Params

@author: duanqiyi

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

from enum import IntEnum

class EnumSnifferPllMode(IntEnum):
    SNIFFER_PLL_MODE_ON = 0
    SNIFFER_PLL_MODE_OFF = 1
    SNIFFER_PLL_MODE_DPD = 2
    SNIFFER_PLL_MODE_SLEEP = 3

class EnumSnifferNBICMode(IntEnum):
    SNIFFER_NBIC_DISABLE = 0
    SNIFFER_NBIC_ENABLE = 1
    SNIFFER_NBIC_ENABLE_WITH_LOW_POWER = 2

class EnumSnifferPayloadCipherMode(IntEnum):
    SNIFFER_PAYLOAD_CIPHER_DISABLE = 0xFF

class EnumSnifferTXTempCompMode(IntEnum):
    SNIFFER_TX_TEMP_COMP_DISABLE = 0
    SNIFFER_TX_TEMP_COMP_ENABLE = 1

class EnumSnifferXTALTempCompMode(IntEnum):
    SNIFFER_XTAL_TEMP_COMP_DISABLE = 0
    SNIFFER_XTAL_TEMP_COMP_ENABLE = 1

class EnumSnifferToaAlgorithmMode(IntEnum):
    SNIFFER_TOA_ALGORITHM_DISABLE = 0
    SNIFFER_TOA_ALGORITHM_ENABLE = 1

class EnumSnifferRangingActionMode(IntEnum):
    SNIFFER_RANGING_ACTION_EMPTY = 0
    SNIFFER_RANGING_ACTION_RX_WITH_TOA = 1
    SNIFFER_RANGING_ACTION_TX_WITH_TOA = 2
    SNIFFER_RANGING_ACTION_RX_WITHOUT_TOA = 3
    SNIFFER_RANGING_ACTION_TX_WITHOUT_TOA = 4

class EnumSnifferDataInPSDUMode(IntEnum):
    SNIFFER_DATA_IN_PSDU_NO_PSDU = 0
    SNIFFER_DATA_IN_PSDU_PRE_PSDU = 1
    SNIFFER_DATA_IN_PSDU_TIMESTAMPS = 2
    SNIFFER_DATA_IN_PSDU_PRE_PSDU_AND_TIMESTAMPS = 3