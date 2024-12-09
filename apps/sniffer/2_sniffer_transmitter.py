# -*- coding: utf-8 -*-
"""

@file: sniffer transmitter demo script

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
    log_i("Start of sniffer transmitter demo script...")
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

    sniffer_param = SnifferParam(channel=9)
    sniffer_param.set_tx_power(14)
    sniffer_param.set_sfd_id(0)
    sniffer_param.set_preamble_id(9)
    sniffer_param.set_tx_num(100)
    sniffer_param.set_tx_interval(50000)  # 50ms, max interval : 65535, ~65 ms

    sniffer_app.sniffer_cfg_ranging_app(sniffer_param.channel_id, sniffer_param.tx_power)
    sniffer_app.sniffer_cfg_tx_mode(sniffer_param.preamble_id, sniffer_param.sfd_id, sniffer_param.tx_num, sniffer_param.tx_interval)

    payload = [0x11, 0x22, 0x33, 0x44]

    # start sniffer transmitter
    result = sniffer_app.sniffer_start_tx_mode(payload)
    if result.status == EnumUciStatus.UCI_STATUS_OK.value:
        log_i(str(result.uci_result))
    if sniffer_param.tx_num == 0:
        log_i("TX number is set to 0, it will repeat indefinitelyly until reset device, and it will not return any response")
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        sniffer_app.device.hard_reset()

    log_i("**************************************************************")
    log_i("End of sniffer transmitter demo script...")
    log_i("**************************************************************")

if __name__ == '__main__':
    main()





