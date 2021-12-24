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
        self.parser.read_dict({"global": {"interval": 10}})
        if Path(self.config_file).exists():
            self.parser.read(self.config_file)
        # for each section, add default values:
        glob_inter = self.parser.get("global", "interval")
        for section in self.get_sections():
            if not section.startswith("export"):
                if not self.parser.has_option(section, "interval"):
                    self.parser.set(section, "interval", glob_inter)

    def dump(self):
        print("Config DUMP:")
        for section in self.get_sections():
            options = self.get_section_dict(section)
            print(f"[{section}]")
            for k, v in options.items():
                print(f"  {k}={v}")

    def get_sections(self) -> List[str]:
        return self.parser.sections()

    def get_sections_with_option(self, option) -> List[str]:
        return [s for s in self.get_sections() if option in self.parser[s]]

    def get_section_dict(self, section: str) -> Dict:
        options = self.parser.items(section)
        ret = {}
        for (key, value) in options:
            ret[key] = value
        return ret

    def has_section(self, section) -> bool:
        return section in self.get_sections()

    def get_option(self, section: str, option: str) -> str:
        return self.parser[section].get(option)
