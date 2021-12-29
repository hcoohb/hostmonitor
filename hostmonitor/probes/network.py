import time
from typing import Dict

import psutil
from hostmonitor.plugins import register_class
from hostmonitor.probes._probe import Probe


@register_class
class Network(Probe):
    def run(self) -> Dict:
        """Collect network info"""
        # bandwidth:
        # Get net in/out
        net1_out = psutil.net_io_counters().bytes_sent
        net1_in = psutil.net_io_counters().bytes_recv
        time.sleep(1)
        # Get new net in/out
        net2_out = psutil.net_io_counters().bytes_sent
        net2_in = psutil.net_io_counters().bytes_recv
        current_in = round(max(0, net2_in - net1_in) / 1e3, 1)
        current_out = round(max(0, net2_out - net1_out) / 1e3, 1)

        nics = {}
        for name, snic_array in psutil.net_if_addrs().items():
            # Create NIC object
            nic = {"mac": "", "address": "", "address6": "", "netmask": ""}
            # Get NiC values
            for snic in snic_array:
                if snic.family == -1:
                    nic["mac"] = snic.address
                elif snic.family == 2:
                    nic["address"] = snic.address
                    nic["netmask"] = snic.netmask
                elif snic.family == 23:
                    nic["address6"] = snic.address
            nics[name] = nic

        ret_dict = {"up": current_out, "down": current_in}
        ret_dict.update(nics)
        return ret_dict
