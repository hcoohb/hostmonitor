from configparser import ConfigParser
from pathlib import Path
from typing import Union, Dict, List


class Config:
    def __init__(self, config_file: Union[str, Path]) -> None:
        if isinstance(config_file, str):
            self.config_file = Path(config_file)
        elif isinstance(config_file, Path):
            self.config_file = config_file
        self.parser = ConfigParser()
        self.read()

    def read(self):
        # define default global section:
        self.parser.read_dict({"global": {"key1": 233}})
        if Path(self.config_file).exists():
            self.parser.read(self.config_file)

    def dump(self):
        print(self.parser.sections())
        print(self.parser.items(section="full"))
        print(self.parser["full"])
        print(self.get_section_dict("full"))

    def get_sections(self) -> List[str]:
        return self.parser.sections()

    def get_section_dict(self, section: str) -> Dict:
        options = self.parser.items(section)
        ret = {}
        for (key, value) in options:
            ret[key] = value
        return ret
