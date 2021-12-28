import psutil

from probes._probe import Probe
from plugins import register_class
from typing import Dict


@register_class
class CPU(Probe):
    def run(self) -> Dict:

        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(interval=1)

        ret_dict = {
            "cores": cpu_count,
            "used_pct": cpu_usage,
        }
        if psutil.version_info >= (5, 6, 2):
            # get load:
            cpu_load = [round(x / cpu_count * 100, 1) for x in psutil.getloadavg()]
            load = {
                "load_1m": cpu_load[0],
                "load_5m": cpu_load[1],
                "load_15m": cpu_load[2],
            }
            ret_dict.update(load)
            # list the core temps:
            try:
                cpu_temps = psutil.sensors_temperatures().get("coretemp", [])
                temps = {"temp_" + core.label: core.current for core in cpu_temps}
                ret_dict.update(temps)
            except AttributeError:
                pass
        return ret_dict
