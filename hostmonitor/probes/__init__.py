import plugins
from typing import Type
from probes._probe import Probe as ProbsCls

registered = plugins.names_factory(__package__)
required_args = plugins.required_args_factory(__package__)


def get(plugin: str):
    cls: Type[ProbsCls] = plugins.get(__package__, plugin)

    class Probe(cls):  # type: ignore
        def __init__(self, scheduler, queue, name, interval, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.sched = scheduler
            self.q = queue
            self.interval = int(interval)
            self.name = name

        def run(self):
            self.sched.enter(self.interval, 1, self.run)
            ret = super().run()
            self.q.put({self.name: ret})

    return Probe
