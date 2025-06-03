from hatchling.plugin import hookimpl

import vertex_hatch_tools.plugin as v_plugin

@hookimpl
def hatch_register_build_hook():
    return v_plugin.VertexBuildHook
