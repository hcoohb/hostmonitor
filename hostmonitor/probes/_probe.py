from abc import ABC, abstractmethod
class Probe(ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def run(self):
        pass
