from typing import NotRequired, TypedDict

type AreaNumber = int
type SpotName = str
type SpotData = dict[int, "StageNode"]


class SpotNode(TypedDict):
    stages: dict[int, "StageNode"]
    required_clears: int
    """The number of required stage clears to unlock the Great Reigen Kaisei Prayer for this spot"""


class StageNode(TypedDict):
    requires: NotRequired[int]
    """Unlocked by this stage"""
    dlc: NotRequired[int]
    """Available after purchasing this "Extra Songs Pack" DLC by number (e.g. `3` means "Extra Songs Pack 3")"""


map_graph: dict[AreaNumber, dict[SpotName, SpotNode]] = {
    0: {
        "Hakurei Shrine": {
            "required_clears": 3,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {"requires": 2},
                5: {"requires": 2},
                6: {"requires": 5},
                7: {"requires": 5},
                12: {"dlc": 2},
                13: {"dlc": 3},
                14: {"dlc": 4},
            },
        },
    },
    1: {
        "Scarlet Devil Mansion": {
            "required_clears": 6,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {},
                7: {},
                8: {"requires": 1},
                9: {"requires": 1},
                10: {"requires": 2},
                11: {"requires": 14},
                12: {"requires": 6},
                14: {"requires": 6},
                15: {"requires": 6},
                16: {"dlc": 3},
                17: {"dlc": 4},
                18: {"dlc": 4},
            },
        },
        "Misty Lake": {
            "required_clears": 5,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {"requires": 5},
                7: {"requires": 5},
                8: {"dlc": 2},
                9: {"dlc": 3},
            },
        },
        "Forest of Magic": {
            "required_clears": 5,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {"requires": 1},
                7: {"requires": 5},
                8: {"requires": 5},
                9: {"dlc": 2},
                10: {"dlc": 4},
                11: {"dlc": 4},
            },
        },
    },
    2: {
        "Human Village": {
            "required_clears": 3,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {"requires": 3},
                6: {"requires": 2},
                7: {"requires": 2},
                8: {"requires": 3},
                9: {"dlc": 2},
                10: {"dlc": 3},
                11: {"dlc": 3},
            },
        },
        "Bamboo Forest of the Lost": {
            "required_clears": 4,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {"requires": 1},
                6: {"requires": 4},
                7: {"requires": 4},
                8: {"dlc": 2},
                9: {"dlc": 3},
                10: {"dlc": 3},
            },
        },
        "Eientei": {
            "required_clears": 5,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {"requires": 2},
                7: {"requires": 5},
                8: {"requires": 5},
                9: {"dlc": 2},
                10: {"dlc": 4},
            },
        },
        "Underworld": {
            "required_clears": 4,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {"requires": 2},
                6: {"requires": 2},
                7: {"requires": 2},
                8: {"requires": 1},
                9: {"requires": 1},
                10: {"requires": 1},
                11: {"requires": 4},
                12: {"requires": 2},
                13: {"requires": 4},
                14: {"dlc": 2},
                15: {"dlc": 2},
                16: {"dlc": 2},
            },
        },
        "Myouren Temple": {
            "required_clears": 6,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {},
                7: {"requires": 2},
                8: {"requires": 6},
                9: {"requires": 11},
                10: {"requires": 5},
                11: {"requires": 5},
                12: {"requires": 11},
                13: {"requires": 4},
                14: {"requires": 4},
                15: {"dlc": 2},
                16: {"dlc": 3},
                17: {"dlc": 4},
            },
        },
    },
    3: {
        "Youkai Mountain": {
            "required_clears": 6,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {},
                7: {},
                8: {"requires": 2},
                9: {"requires": 8},
                10: {"requires": 8},
                11: {"requires": 6},
                12: {"requires": 6},
                13: {"requires": 6},
                14: {"requires": 12},
                15: {"requires": 12},
                16: {"dlc": 2},
                17: {"dlc": 4},
                18: {"dlc": 4},
            },
        },
        "Moriya Shrine": {
            "required_clears": 4,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {"requires": 2},
                6: {"requires": 2},
                7: {"requires": 6},
                8: {"requires": 6},
                9: {"requires": 3},
                10: {"dlc": 2},
                11: {"dlc": 4},
            },
        },
        "Heaven": {
            "required_clears": 3,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {"requires": 1},
                5: {"requires": 1},
                6: {"requires": 3},
                7: {"requires": 3},
                8: {"dlc": 2},
                9: {"dlc": 3},
            },
        },
        "Hades": {
            "required_clears": 5,
            "stages": {
                1: {},
                2: {},
                3: {},
                4: {},
                5: {},
                6: {},
                7: {"requires": 2},
                8: {"requires": 5},
                9: {"requires": 5},
                10: {"requires": 5},
                11: {"requires": 7},
                12: {"requires": 7},
                13: {"dlc": 3},
                14: {"dlc": 4},
                15: {"dlc": 4},
            },
        },
    },
    4: {
        "Hakurei Shrine - Reconstructed": {
            "required_clears": 4,
            "stages": {
                8: {},
                9: {},
                10: {},
                11: {},
            },
        },
        "Scarlet Devil Mansion - Seeking Memories": {
            "required_clears": 0,
            "stages": {
                13: {},
            },
        },
    },
}
