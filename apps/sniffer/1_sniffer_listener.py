# -*- coding: utf-8 -*-
"""

@file: sniffer listener demo script

@author: duanqiyi

@copyright  Copyright (c) 2019 - 2024, chengdu forthink tech. Co., Ltd.
                       All rights reserved
"""

import sys
from nxp_ft4222h import *
from console_helper import *
from forthink_uwb_dongle import *

from uci_port import *
from uci_defs import *
from uci_layer import *
from SnifferDevice import *
from SnifferRegionParams import *

def main():
    print_forthink_logo()
    log_i("**************************************************************")
    log_i("Start of sniffer listener demo script...")
    log_i("**************************************************************")

    dongle_list = scan_uwb_dongle_devices()
    if len(dongle_list) == 0:
        sys.exit("No UWB dongle devices found. Aborting program...")

    # get the first device in the list
    dongle = forthink_uwb_dongle(dongle_list[0])
    dongle.ft4222_device.open(spi_frequency_hz=1e07,
                              mode=EnumFtdiSpiMode.FTDI_SPI_MODE_SINGLE)
    
    # register and initialize sniffer Device (include UCI layer)
    sniffer_app = SnifferDevice(dongle.ft4222_device)

    # hard reset UWB Device, activate the device
    sniffer_app.device.hard_reset()
    result = sniffer_app.wait_response(timeout_ms=200)

    if result.status is not EnumUciStatus.UCI_STATUS_REBOOT:
        log_e(": " + str(result.status))

    # python-uwbzero uwbmac_fira_ranging app parameter
    sniffer_param = SnifferParam(channel=9)
    sniffer_param.set_sfd_id(2)
    sniffer_param.set_preamble_id(10)
    
    # python-uwbzero 2_uwbmac_ccc_ranging_initiator app parameter
    # sniffer_param = SnifferParam(channel=9)
    # sniffer_param.set_sfd_id(0)
    # sniffer_param.set_preamble_id(9)

    sniffer_app.sniffer_cfg_ranging_app(sniffer_param.channel_id, sniffer_param.tx_power)
    sniffer_app.sniffer_cfg_rx_mode(sniffer_param.preamble_id, sniffer_param.sfd_id)

    # start sniffer listener
    # may print UCI_PORT_STATUS_ERR_TIMEOUT, just ignore it
    while True:
        try:
            result = sniffer_app.sniffer_start_rx_mode()
            if result.status == EnumUciStatus.UCI_STATUS_OK.value:
                log_i(str(result.uci_result))
        except KeyboardInterrupt:
            break

    log_i("**************************************************************")
    log_i("End of sniffer listener demo script...")
    log_i("**************************************************************")

if __name__ == '__main__':
    main()





