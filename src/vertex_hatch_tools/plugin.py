from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

print('vertex-hatch-tools.plugin have been imported')

class VertexBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'vertex'

    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        print('vertex initialize')
        print(self.root)
        print(self.app)
        print(self.PLUGIN_NAME)
        print(version)
        print(build_data)

    def finalize(version: str, build_data: dict[str, Any], artifact_path: str) -> None:
        print('vertex finalize')
        print(build_data)
        print(artifact_path)
