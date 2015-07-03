"""Magnet to power supply mapping definitions"""

import re as _re
from . import record_names as _record_names


_name_split_char = '-'


def get_magnet_mapping():
    """Get mapping from power supply to magnet names and inverse mapping

    Returns mapping, inverse_mapping.
    """
    mapping = dict()

    # Add individual power supplies
    magnets = _record_names.get_record_names('tsma')
    magnet_names = magnets.keys()
    pss = _record_names.get_record_names('tsps')
    for ps_name in pss.keys():
        ps_magnet_name = ps_name.replace('TSPS', 'TSMA')
        if ps_magnet_name in magnet_names:
            if ps_magnet_name in mapping:
                mapping[ps_magnet_name].add(ps_name)
            else:
                s = set()
                s.add(ps_name)
                mapping[ps_magnet_name] = s

    inverse_mapping = dict()
    for item in mapping.items():
        key, value = item
        for v in value:
            if v in inverse_mapping:
                inverse_mapping[v].add(key)
            else:
                s = set()
                s.add(key)
                inverse_mapping[v] = s

    return mapping, inverse_mapping
