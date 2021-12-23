import importlib
import sched
import time
import threading
import queue

from config import Config


class HostMonitor:
    """Monitoring host and exporting results"""

    def __init__(self, config_file: str = "hostmonitor.conf") -> None:
        config = Config(config_file)
        config.dump()
        scheduler = sched.scheduler(time.time, time.sleep)
        q: queue.Queue = queue.Queue(maxsize=50)
        probes = []
        exports = []

        # load exports:
        for export in [p for p in config.get_sections() if p.startswith("export")]:
            try:
                module = importlib.import_module(
                    f"exports.{export.lower()[len('export_'):]}"
                )
                cls = getattr(module, export)
            except ModuleNotFoundError:
                print(f"Failed importing module: exports.{export.lower()}")
                continue
            if cls is not None:
                exports.append(cls())

        # load probes:
        for probe in config.get_sections():
            try:
                module = importlib.import_module(f"probes.{probe.lower()}")
                cls = getattr(module, probe)
            except ModuleNotFoundError:
                print(f"Failed importing module: probes.{probe.lower()}")
                continue
            if cls is not None:
                probes.append(cls(scheduler, q))

        # end of setup, run tasks:
        for p in probes:
            # self.scheduler.enter(5, 1, p.run)
            p.run()
        t = threading.Thread(target=scheduler.run, args=(), kwargs={}, daemon=True)
        t.start()
        # self.scheduler.run()
        print("I am after")
        while True:
            while not q.empty():
                data = q.get()
                for export in exports:
                    export.export(data)
                # print(data)
            time.sleep(1)


if __name__ == "__main__":
    t = HostMonitor()
