import subprocess
from typing import Dict

from plugins import register_class

from probes._probe import Probe


@register_class
class CMD(Probe):
    def __init__(self, cmd: str, *args, **kwargs) -> None:
        self.cmd = cmd
        super().__init__(*args, **kwargs)

    def run(self) -> str:
        """Run a subprocess command"""
        res = "-1"
        try:
            res = (
                subprocess.check_output(
                    [self.cmd], stderr=subprocess.STDOUT, shell=True
                )
                .decode("utf-8")
                .rstrip()
            )
        except:
            pass
        return res
