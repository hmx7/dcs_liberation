import typing
import random

import dcs

from shop import db
from theater.controlpoint import *
from theater.base import *
from theater.conflicttheater import *

UNIT_VARIETY = 2
UNIT_AMOUNT_FACTOR = 1


def generate_initial(theater: ConflictTheater, enemy: str):
    for cp in theater.enemy_bases():
        if cp.captured:
            continue

        for task in [CAP, FighterSweep, CAS, AirDefence]:
            suitable_unittypes = db.find_unittype(task, enemy)
            suitable_unittypes.sort(key=lambda x: db.PRICES[x], reverse=True)

            importance = IMPORTANCE_HIGH * 10 - cp.importance * 10
            units_idx_start = int(importance)
            units_idx_end = units_idx_start + UNIT_VARIETY
            print("{} - {}-{}".format(cp.name, units_idx_start, units_idx_end))

            range_start = min(len(suitable_unittypes)-1, units_idx_start)
            range_end = min(len(suitable_unittypes), units_idx_end)
            unittypes = suitable_unittypes[range_start:range_end]

            typecount = max(math.floor(importance * UNIT_AMOUNT_FACTOR), 1)
            units = {unittype: typecount for unittype in unittypes}
            cp.base.commision_units(units)