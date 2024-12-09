# -*- coding: utf-8 -*-
"""

@file: sniffer listener sequence demo script

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
    log_i("Start of sniffer listener sequence demo script...")
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
    sniffer_param.set_sfd_id(0)
    sniffer_param.set_preamble_id(9)
    sniffer_param.set_tx_num(5)
    sniffer_param.set_tx_interval(10000)

    sniffer_app.sniffer_cfg_ranging_app(sniffer_param.channel_id, sniffer_param.tx_power)

    # cfg sniffer listener sequence
    cmd = []
    cmd += sniffer_app.sniffer_generate_ranging_cmd(preamble_id=sniffer_param.preamble_id, 
                                                    sfd_id=sniffer_param.sfd_id, 
                                                    delay=500, timeout=0xFFFFFF, psdu_index=0)  # first frame's timeout is about 16.7s
    cmd += sniffer_app.sniffer_generate_ranging_cmd(preamble_id=sniffer_param.preamble_id, 
                                                    sfd_id=sniffer_param.sfd_id, 
                                                    delay=0.5 * sniffer_param.tx_interval + 500, 
                                                    timeout=sniffer_param.tx_interval - 200, psdu_index=1)
    cmd += sniffer_app.sniffer_generate_ranging_cmd(preamble_id=sniffer_param.preamble_id, 
                                                    sfd_id=sniffer_param.sfd_id, 
                                                    delay=1.5 * sniffer_param.tx_interval + 500, 
                                                    timeout=sniffer_param.tx_interval - 200, psdu_index=2)
    cmd += sniffer_app.sniffer_generate_ranging_cmd(preamble_id=sniffer_param.preamble_id, 
                                                    sfd_id=sniffer_param.sfd_id, 
                                                    delay=2.5 * sniffer_param.tx_interval + 500, 
                                                    timeout=sniffer_param.tx_interval - 200, psdu_index=3)
    cmd += sniffer_app.sniffer_generate_ranging_cmd(preamble_id=sniffer_param.preamble_id, 
                                                    sfd_id=sniffer_param.sfd_id, 
                                                    delay=3.5 * sniffer_param.tx_interval + 500, 
                                                    timeout=sniffer_param.tx_interval - 200, psdu_index=4)

    sniffer_app.sniffer_cfg_ranging_seq(cmd)

    # start sniffer listener sequence
    try:
        result = sniffer_app.sniffer_start_ranging()    # by default, first frame's timeout is about 16.7s
        if result.status == EnumUciStatus.UCI_STATUS_OK.value:
            log_i("sniffer listener sequence successfully")
            result = sniffer_app.sniffer_get_ranging_status()
            log_i(str(result.uci_result))
            result = sniffer_app.sniffer_get_ranging_result() # get all timestamp difference from first frame's timestamp
            log_i(str(result.uci_result))
            for i in range(sniffer_param.tx_num):
                result = sniffer_app.sniffer_get_payload(i)
                if result.uci_result.status == EnumUciStatus.UCI_STATUS_OK.value:
                    log_i(f"get payload {i}:")
                    log_i(str(result.uci_result))
        else:
            log_i("sniffer listener sequence failed")
    except KeyboardInterrupt:
        sniffer_app.device.hard_reset()

    log_i("**************************************************************")
    log_i("End of sniffer listener sequence demo script...")
    log_i("**************************************************************")

if __name__ == '__main__':
    main()





