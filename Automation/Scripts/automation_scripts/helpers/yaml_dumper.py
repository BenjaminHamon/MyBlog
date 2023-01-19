import datetime
import yaml


class YamlDumper(yaml.SafeDumper):


    def ignore_aliases(self, data) -> bool:
        if isinstance(data, datetime.datetime):
            return True

        return super().ignore_aliases(data)
