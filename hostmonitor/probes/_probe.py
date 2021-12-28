from abc import ABC, abstractmethod
from typing import Union, Dict


class Probe(ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def run(self) -> Union[str, Dict]:
        pass
