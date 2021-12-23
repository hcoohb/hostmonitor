import os

from probes.probes import Probes


class CPU(Probes):
    name = "CPU"

    def __init__(self, scheduler, queue, param: str = "test") -> None:
        super().__init__()
        self.scheduler = scheduler
        self.q = queue

    def run(self) -> str:
        self.scheduler.enter(5, 1, self.run)
        ret = os.cpu_count()
        self.q.put({self.name: ret})
        # print(f"::{self.name} -> {ret}")
        return str(ret)
