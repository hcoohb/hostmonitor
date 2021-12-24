import os

from probes._probe import Probe
from plugins import register_class


@register_class
class CPU(Probe):
    def run(self) -> str:
        ret = os.cpu_count()
        return str(ret)
