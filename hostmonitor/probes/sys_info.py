import platform
import socket
import uuid
from typing import Dict

from hostmonitor.plugins import register_class
from hostmonitor.probes._probe import Probe


@register_class
class SysInfo(Probe):
    def run(self) -> Dict:
        """Collect system info, typically static values"""

        hostname = socket.gethostname()
        sys_uuid = uuid.getnode()

        ret_dict = {
            "hostname": hostname,
            "uuid": sys_uuid,
            "OS_name": platform.system(),
            "OS_version": platform.release(),
        }
        return ret_dict
