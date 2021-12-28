import queue
import sched
import socket
import threading
import time
from typing import List, Type

import exports as export_plugins
import probes as probes_plugins
from config import Config
from probes._probe import Probe


class HostMonitor:
    """Monitoring host and exporting results"""

    def __init__(self, config_file: str = "hostmonitor.conf") -> None:
        config = Config(config_file)
        self.config = config
        config.dump()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.q: queue.Queue = queue.Queue(maxsize=50)
        self.probes: List[Probe] = []
        exports = []

        # load exports:
        for ex in config.get_sections_with_option("export"):
            ex_module = config.get_option(ex, "export")
            if ex_module not in export_plugins.registered():
                continue
            param = config.get_section_dict(ex)
            param.pop("export")  # remove key export
            if export_plugins.validate_args(ex_module, param):
                cls = export_plugins.get(ex_module)
                exports.append(cls(**param))

        # load probes:
        for probe_title in config.get_sections_with_option("probe"):
            self.setup_probe(probe_title)

        # end of setup, run tasks:
        for probe in self.probes:
            # self.scheduler.enter(5, 1, p.run)
            probe.run()
        t = threading.Thread(target=self.scheduler.run, args=(), kwargs={}, daemon=True)
        t.start()
        # self.scheduler.run()
        print("I am after")
        while True:
            while not self.q.empty():
                data = self.q.get()
                # print(f"fake{data}")
                for export in exports:
                    export.export(data)
                # print(data)
            time.sleep(1)

    def setup_probe(self, section: str):
        p_module = self.config.get_option(section, "probe")
        if p_module not in probes_plugins.registered():
            return
        param = self.config.get_section_dict(section)
        param.pop("probe")
        if "runon" in param:
            if socket.gethostname() != param["runon"]:
                return
            param.pop("runon")
        if not probes_plugins.validate_args(p_module, param):
            return
        cls: Type[Probe] = probes_plugins.get(p_module)
        self.probes.append(cls(self.scheduler, self.q, section, **param))


if __name__ == "__main__":
    t = HostMonitor()
