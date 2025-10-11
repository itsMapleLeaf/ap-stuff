from .world import WorldSpec


def __define_world_spec() -> WorldSpec:
    spec = WorldSpec()

    spec.define_item("Test Item")
    spec.define_location("Test Location")

    return spec


spec = __define_world_spec()
