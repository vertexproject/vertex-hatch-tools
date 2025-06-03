import os
import glob
import subprocess

from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def get_git_commit() -> str | None:
    commit = None
    try:
        ret = subprocess.run(['git', 'rev-parse', 'HEAD'],
                             capture_output=True,
                             timeout=15,
                             check=True,
                             text=True, )
    except Exception as e:
        print(f'Error grabbing commit: {e}')
    else:
        commit = ret.stdout.strip()
    return commit


def _replace_commit(filepath: str, oldv, newv):
    if not os.path.exists(filepath):
        raise ValueError(f'{filepath=} does not exist!')
    with open(filepath, 'r') as fd:
        content = fd.read()
    new_content = content.replace(f"commit = {oldv}", f"commit = {newv}")
    if content == new_content:
        raise ValueError(f'Unable to replace [{oldv}] -> [{newv}] into {filepath}')
    with open(filepath, 'wb') as fd:
        _ = fd.write(new_content.encode())


class VertexBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'vertex'

    def __init__(self, *args, **kwargs):
        print(f'{args=} {kwargs=}')
        super().__init__(*args, **kwargs)

        print(self.config)  # Access key-value configs from the pyproject.toml file.

        self.vtx_git_current_commit = None  # type: None | str
        self.vtx_git_set_commit = self.config.get('set_git_commit', ())

    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        print('vertex initialize')
        print(f'{self.root=}')
        print(f'{self.app=}')
        print(f'{self.directory}')
        print(f'{build_data=}')
        print(f'{self.target_name=}')

        if self.vtx_git_set_commit:
            self.replace_commit(build_data)

    def replace_commit(self, build_data: Dict[str, Any]) -> None:
        self.vtx_git_current_commit = get_git_commit()
        if self.vtx_git_current_commit:
            for filepath in self.vtx_git_set_commit:
                _replace_commit(filepath, oldv="''", newv=f"'{self.vtx_git_current_commit}'")
        else:
            raise ValueError('No git commit detected!')

    def undo_replace_commit(self, build_data: Dict[str, Any]) -> None:
        for filepath in self.vtx_git_set_commit:
            _replace_commit(filepath, oldv=f"'{self.vtx_git_current_commit}'", newv="''")

    def clean(self, build_data: Dict[str, Any]) -> None:
        print(f'vertex clean!')
        print(f'{build_data=}')

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:
        print('vertex finalize')
        print(build_data)
        print(artifact_path)

        if self.vtx_git_set_commit:
            self.undo_replace_commit(build_data)
