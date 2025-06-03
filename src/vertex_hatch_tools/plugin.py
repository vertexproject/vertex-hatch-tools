from hatchling.plugin import hookimpl

import vertex_hatch_tools.hooks as v_hooks

@hookimpl
def hatch_register_build_hook():
    return v_hooks.VertexBuildHook
