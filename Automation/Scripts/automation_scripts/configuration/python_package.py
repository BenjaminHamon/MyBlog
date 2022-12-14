import dataclasses


@dataclasses.dataclass(frozen = True)
class PythonPackage:
    name: str
    path_to_sources: str

    @property
    def name_for_file_system(self):
        return self.name.replace("-", "_")
