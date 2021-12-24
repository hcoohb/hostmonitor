from datetime import datetime
from probes._probe import Probe
from plugins import register_class


@register_class
class TimeNow(Probe):
    def run(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time
