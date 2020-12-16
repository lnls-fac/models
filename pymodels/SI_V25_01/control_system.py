
from siriuspy.namesys import SiriusPVName as _PVName, join_name as _join_name

from . import families as _fams


def get_control_system_data(lattice, fam_data=None):
    fam_data = fam_data or _fams.get_family_data(lattice)
    names = dict()

    # Individual elements
    quads = _fams.families_quadrupoles()
    mags = quads[:]
    mags.extend(['CH', 'CV', 'QS'])
    for mag in mags:
        dta = fam_data[mag]
        idxs = dta['index']
        subs = dta['subsection']
        insts = dta['instance']
        for idx, sub, inst in zip(idxs, subs, insts):
            name = _join_name(sec='SI', dis='MA', sub=sub, idx=inst, dev=mag)
            names[name] = idx

    # Families
    mags = quads[:]
    mags.extend(_fams.families_sextupoles())
    mags.extend(['B1B2-1', 'B1B2-2'])
    for mag in mags:
        name = _join_name(sec='SI', dis='MA', sub='Fam', dev=mag)
        names[name] = fam_data[mag]['index']

    return names
