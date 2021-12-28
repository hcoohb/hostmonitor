import psutil
from typing import Dict

from plugins import register_class

from probes._probe import Probe


@register_class
class Memory(Probe):
    def run(self) -> Dict:
        """Collect memory info"""
        memory_stats = psutil.virtual_memory()
        memory_total = memory_stats.total
        memory_used = memory_stats.used
        memory_used_percent = memory_stats.percent
        ret_dict = {
            "total": memory_total,
            "used": memory_used,
            "used_pct": memory_used_percent,
        }
        return ret_dict
