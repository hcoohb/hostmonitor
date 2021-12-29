import subprocess
from typing import Dict

from hostmonitor.plugins import register_class
from hostmonitor.probes._probe import Probe


@register_class
class User(Probe):
    def run(self) -> Dict:
        """Collect user data"""
        num_users = "-1"
        num_sessions = "-1"
        try:
            comm = "users |tr ' ' '\n' | sort -u | wc -l"
            num_users = (
                subprocess.check_output([comm], stderr=subprocess.STDOUT, shell=True)
                .decode("utf-8")
                .rstrip()
            )
            comm = "who | wc -l"
            num_sessions = (
                subprocess.check_output([comm], stderr=subprocess.STDOUT, shell=True)
                .decode("utf-8")
                .rstrip()
            )
        except:
            pass
        ret_dict = {"num_users": num_users, "num_sessions": num_sessions}
        return ret_dict
