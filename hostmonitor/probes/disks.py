import psutil
from typing import Dict

from plugins import register_class

from probes._probe import Probe


@register_class
class SysInfo(Probe):
    def run(self) -> Dict:
        """Collect disks info"""
        # Disk Info
        disk_info = psutil.disk_partitions()
        disks = {}
        for x in disk_info:
            # Try fixes issues with connected 'disk' such as CD-ROMS, Phones, etc.
            try:
                disk = {
                    "name": x.device,
                    "mount_point": x.mountpoint,
                    "type": x.fstype,
                    "total_size": psutil.disk_usage(x.mountpoint).total,
                    "used_size": psutil.disk_usage(x.mountpoint).used,
                    "used_pct": psutil.disk_usage(x.mountpoint).percent,
                }

                disks[x.mountpoint] = disk
            except:
                pass
        return disks
