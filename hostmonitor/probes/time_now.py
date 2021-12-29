import time
from datetime import datetime

import psutil
from hostmonitor.plugins import register_class
from hostmonitor.probes._probe import Probe


@register_class
class TimeNow(Probe):
    def run(self):
        """Collect time info"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
        uptime = int(time.time() - psutil.boot_time())
        lastboot = datetime.fromtimestamp(psutil.boot_time()).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        ret_dict = {"uptime": uptime, "timestamp": timestamp, "lastboot": lastboot}
        return ret_dict
