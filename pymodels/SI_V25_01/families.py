"""Element family definitions."""

import pyaccel as _pyaccel


_family_segmentation = {
    'B1': 30, 'B2': 36, 'BC': 34,
    'QFA': 1, 'QDA': 1,
    'QFB': 1, 'QDB1': 1, 'QDB2': 1,
    'QFP': 1, 'QDP1': 1, 'QDP2': 1,
    'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1,
    'SDA0': 1, 'SDB0': 1, 'SDP0': 1,
    'SDA1': 1, 'SDB1': 1, 'SDP1': 1,
    'SDA2': 1, 'SDB2': 1, 'SDP2': 1,
    'SDA3': 1, 'SDB3': 1, 'SDP3': 1,
    'SFA0': 1, 'SFB0': 1, 'SFP0': 1,
    'SFA1': 1, 'SFB1': 1, 'SFP1': 1,
    'SFA2': 1, 'SFB2': 1, 'SFP2': 1,
    'BPM': 1, 'DCCT': 1, 'ScrapH': 1, 'ScrapV': 1, 'GSL15': 1,
    'GSL07': 1, 'GBPM': 1, 'BbBPkup': 1, 'BbBKckrH': 1, 'BbBKckrV': 1,
    'BbBKckrL': 1, 'TuneShkrH': 1, 'TuneShkrV': 1, 'TunePkup': 1,
    'FC1': 1, 'FC2': 1,
    'QS': 1, 'CH': 1, 'CV': 1,
    'SRFCav': 1, 'start': 1,
    'InjDpKckr': 1, 'InjNLKckr': 1, 'PingH': 1, 'PingV': 1,
    'APU22': 2, 'APU58': 2,
    }


family_mapping = {

    'B1': 'dipole',
    'B2': 'dipole',
    'BC': 'dipole',
    'B1B2-1': 'dipole',
    'B1B2-2': 'dipole',

    'QFA': 'quadrupole',
    'QDA': 'quadrupole',
    'QDB2': 'quadrupole',
    'QFB': 'quadrupole',
    'QDB1': 'quadrupole',
    'QDP2': 'quadrupole',
    'QFP': 'quadrupole',
    'QDP1': 'quadrupole',
    'Q1': 'quadrupole',
    'Q2': 'quadrupole',
    'Q3': 'quadrupole',
    'Q4': 'quadrupole',

    'SDA0': 'sextupole',
    'SDB0': 'sextupole',
    'SDP0': 'sextupole',
    'SDA1': 'sextupole',
    'SDB1': 'sextupole',
    'SDP1': 'sextupole',
    'SDA2': 'sextupole',
    'SDB2': 'sextupole',
    'SDP2': 'sextupole',
    'SDA3': 'sextupole',
    'SDB3': 'sextupole',
    'SDP3': 'sextupole',
    'SFA0': 'sextupole',
    'SFB0': 'sextupole',
    'SFP0': 'sextupole',
    'SFA1': 'sextupole',
    'SFB1': 'sextupole',
    'SFP1': 'sextupole',
    'SFA2': 'sextupole',
    'SFB2': 'sextupole',
    'SFP2': 'sextupole',

    'InjNLKckr': 'pulsed_magnet',
    'InjDpKckr': 'pulsed_magnet',
    'PingH': 'pulsed_magnet',
    'PingV': 'pulsed_magnet',

    'BPM': 'bpm',
    'DCCT': 'dcct_to_measure_beam_current',
    'ScrapH': 'horizontal_scraper',
    'ScrapV': 'vertical_scraper',
    'GSL15': 'generic_stripline_(lambda/4)',
    'GSL07': 'generic_stripline_(lambda/8)',
    'GBPM': 'general_bpm',
    'BbBPkup': 'bunch-by-bunch_pickup',
    'BbBKckrH': 'horizontal_bunch-by-bunch_shaker',
    'BbBKckrV': 'vertical_bunch-by-bunch_shaker',
    'BbBKckrL': 'longitudinal_bunch-by-bunch_shaker',
    'TuneShkrH': 'horizontal_tune_shaker',
    'TuneShkrV': 'vertical_tune_shaker',
    'TunePkup': 'tune_pickup',

    'FC1': 'fast_corrector',
    'FC2': 'fast_corrector',
    'FCH': 'fast_horizontal_corrector',
    'FCV': 'fast_vertical_corrector',

    'CH': 'slow_horizontal_corrector',
    'CV': 'slow_vertical_corrector',

    'QS': 'skew_quadrupole',

    'SRFCav': 'superconducting_rf_cavity',
    'APU22': 'insertion_device',
    'APU58': 'insertion_device',
    }


def families_dipoles():
    """Return dipole families."""
    return ['B1', 'B2', 'BC', ]


def families_quadrupoles():
    """Return quadrupole families."""
    return ['QFA', 'QDA', 'QFB', 'QDB1', 'QDB2', 'QFP',
            'QDP1', 'QDP2', 'Q1', 'Q2', 'Q3', 'Q4', ]


def families_sextupoles():
    """Return sextupole families."""
    return ['SDA0', 'SDB0', 'SDP0',
            'SDA1', 'SDB1', 'SDP1',
            'SDA2', 'SDB2', 'SDP2',
            'SDA3', 'SDB3', 'SDP3',
            'SFA0', 'SFB0', 'SFP0',
            'SFA1', 'SFB1', 'SFP1',
            'SFA2', 'SFB2', 'SFP2', ]


def families_horizontal_correctors():
    """Return horizontal corrector families."""
    return ['FCH', 'CH', ]


def families_vertical_correctors():
    """Return vertical corrector families."""
    return ['FCV', 'CV', ]


def families_skew_correctors():
    """Return skew corrector families."""
    return ['QS', ]


def families_rf():
    """Return RF families."""
    return ['SRFCav', ]


def families_pulsed_magnets():
    """Return pulsed magnet families."""
    return ['InjDpKckr', 'InjNLKckr', 'PingH', 'PingV', ]


def families_di():
    """Return diagnostics families."""
    return ['BPM', 'DCCT', 'ScrapH', 'ScrapV', 'GSL15', 'GSL07',
            'GBPM', 'BbBPkup', 'BbBKckrH', 'BbBKckrV', 'BbBKckL'
            'TuneShkrH', 'TuneShkrV', 'TunePkup']


def families_ids():
    """Return insertion devices families."""
    return ['APU22', 'APU58', ]


def get_section_name_mapping(lattice):
    """Return list with section name of each lattice element."""
    lat = lattice[:]
    section_map = ['' for i in range(len(lat))]

    # find where the nomenclature starts counting and shift the lattice:
    start = _pyaccel.lattice.find_indices(lat, 'fam_name', 'start')[0]
    b1 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B1')
    if b1[0] > start:
        ind_shift = (b1[-1] + 1)  # Next element of last b1
    else:
        for i in b1[::-1]:  # except there is a b1 before start
            if i < start:
                ind_shift = i + 1
                break
    lat = _pyaccel.lattice.shift(lat, ind_shift)

    # find indices important to define the change of the names of
    # the subsections.
    b1 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B1')
    b1_nrsegs = len(b1)//40
    b2 = _pyaccel.lattice.find_indices(lat, 'fam_name', 'B2')
    # b2_nrsegs = len(b2)//40
    bc = _pyaccel.lattice.find_indices(lat, 'fam_name', 'BC')
    bpm = _pyaccel.lattice.find_indices(lat, 'fam_name', 'BPM')

    # divide the ring in 20 sectors defined by the b1 dipoles:
    Sects = []
    ini = 0
    for i in range(len(b1)//(2*b1_nrsegs)):
        fim = b1[(i+1)*2*b1_nrsegs-1] + 1
        Sects.append(list(range(ini, fim)))
        ini = fim

    # Names of the subsections:
    sub_secs = ['M1', 'SX', 'M2', 'C1', 'C2', 'BC', 'C3', 'C4']
    symm = ['SA', 'SB', 'SP', 'SB']

    for i, sec in enumerate(Sects, 1):
        # conditions that define change in subsection name:
        # define changes to C1
        sec_b1 = [x for x in b1 if sec[0] <= x <= sec[-1]]
        relev_inds = [sec_b1[0]-1, sec_b1[-1]]
        # define changes to C2 and C4:
        sec_b2 = [x for x in b2 if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_b2[0]-1, sec_b2[-1]]
        # define changes to BC and C3
        sec_bc = [x for x in bc if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_bc[0]-1, sec_bc[-1]]
        # define changes to SX and M2
        sec_bpm = [x for x in bpm if sec[0] <= x <= sec[-1]]
        relev_inds += [sec_bpm[0], sec_bpm[1]-1]
        relev_inds.sort()
        # fill the section_map variable
        ref = 0
        for j in sec:
            section_map[(ind_shift+j) % len(lat)] = "{0:02d}".format(i)
            section_map[(ind_shift+j) % len(lat)] += \
                symm[(i-1) % len(symm)] if sub_secs[ref] == 'SX' else \
                sub_secs[ref]
            if j >= relev_inds[ref]:
                ref += 1

    return section_map


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for family names.

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice, 'fam_name')
    section_map = get_section_name_mapping(lattice)

    def get_idx(x):
        return x[len(x)//2]
    # get_idx = lambda x: x[0]

    # fill the data dictionary with index info ######
    data = {}
    for key, idx in latt_dict.items():
        nr = _family_segmentation.get(key)
        if nr is None:
            continue
        # Create a list of lists for the indexes
        data[key] = [idx[i*nr:(i+1)*nr] for i in range(len(idx)//nr)]

    # ch - slow horizontal correctors
    idx = []
    fams = ['SDA0', 'SFB0', 'SFP0', 'SDA1', 'SDB1', 'SDP1',
            'SFA2', 'SFB2', 'SFP2']
    for fam in fams:
        idx.extend(data[fam])
    data['CH'] = sorted(idx, key=get_idx)

    # cv - slow vertical correctors
    idx = []
    fams = ['SDA0', 'SFB0', 'SFP0', 'SDA1', 'SDB1', 'SDP1',
            'SDA3', 'SDB3', 'SDP3', 'SFA2', 'SFB2', 'SFP2', 'CV']
    for fam in fams:
        if fam in {'SFA2', 'SFB2', 'SFP2'}:
            # for these families there are skew only in C3 sections
            idx.extend([i for i in data[fam] if 'C3' in section_map[i[0]]])
        else:
            idx.extend(data[fam])
    data['CV'] = sorted(idx, key=get_idx)

    # fch - fast horizontal correctors
    data['FCH'] = sorted(data['FC1']+data['FC2'], key=get_idx)

    # fcv - fast vertical correctors
    data['FCV'] = sorted(data['FC1']+data['FC2'], key=get_idx)

    # qs - skew quad correctors
    idx = []
    fams = ['SFA0', 'SDB0', 'SDP0', 'SDA2', 'SDB2',
            'SDP2', 'SDA3', 'SDB3', 'SDP3', 'FC2']
    for fam in fams:
        if fam in {'SDA2', 'SDB2', 'SDP2'}:
            # for these families there are skew only in C1 sections
            idx.extend([i for i in data[fam] if 'C1' in section_map[i[0]]])
        elif fam in {'SDA3', 'SDB3', 'SDP3'}:
            # for these families there are skew only in C3 sections
            idx.extend([i for i in data[fam] if 'C3' in section_map[i[0]]])
        elif fam == 'FC2':
            idx.extend([i for i in data[fam] if 'C2' in section_map[i[0]]])
        else:
            idx.extend(data[fam])
    data['QS'] = sorted(idx, key=get_idx)

    # quadrupoles knobs for optics correction
    idx = []
    fams = ['QFA', 'QDA', 'QDB2', 'QFB', 'QDB1', 'QDP2', 'QFP', 'QDP1',
            'Q1', 'Q2', 'Q3', 'Q4']
    for fam in fams:
        idx.extend(data[fam])
    data['QN'] = sorted(idx, key=get_idx)

    # sbs - sextupoles knobs for optics correction
    idx = []
    fams = ['SDA0', 'SDB0', 'SDP0', 'SDA1', 'SDB1', 'SDP1', 'SDA2', 'SDB2',
            'SDP2', 'SDA3', 'SDB3', 'SDP3', 'SFA0', 'SFB0', 'SFP0', 'SFA1',
            'SFB1', 'SFP1', 'SFA2', 'SFB2', 'SFP2']
    for fam in fams:
        idx.extend(data[fam])
    data['SN'] = sorted(idx, key=get_idx)

    # Power Supply for B1 and B2 families
    data['B1B2-1'] = sorted(data['B1']+data['B2'], key=get_idx)
    data['B1B2-2'] = sorted(data['B1']+data['B2'], key=get_idx)

    # all dipoles indices
    data['BN'] = sorted(data['B1']+data['B2']+data['BC'], key=get_idx)

    # PingH (in the model the same as InjDpKckr)
    data['PingH'] = sorted(data['InjDpKckr'], key=get_idx)

    # IDs
    idx = []
    fams = ['APU22', 'APU58', ]
    for fam in fams:
        idx.extend(data[fam])
    data['ID'] = sorted(idx, key=get_idx)

    # Girders
    girder = get_girder_data(lattice)
    if girder is not None:
        data['girder'] = girder

    def f(x):
        return '{0:d}'.format(x)

    # now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [section_map[get_idx(i)] for i in idx]

        # find out if there are more than one element per section and
        # attribute a number to it
        num = len(secs)*['']
        if len(secs) > 1:
            j = 1
            num[0] = f(j) if secs[0] == secs[1] else ''
            j = j+1 if secs[0] == secs[1] else 1
            for i in range(1, len(secs)-1):
                num[i] = f(j) if secs[i] == secs[i+1] or secs[i] == secs[i-1] \
                    else ''
                j = j+1 if secs[i] == secs[i+1] else 1
            num[-1] = f(j)if (secs[-1] == secs[-2]) else ''

        new_data[key] = {'index': idx, 'subsection': secs, 'instance': num}

    # girders
    return new_data


def get_girder_data(lattice):
    """Return girder data.

    List of dicts, one for each girder, containing index of elements in that
    girder.
    """
    gir = _pyaccel.lattice.find_indices(lattice, 'fam_name', 'girder')
    if not gir:
        return None
    gir_ini = gir[0::2]
    gir_end = gir[1::2]

    data = []
    for ini, end in zip(gir_ini, gir_end):
        data.append(list(range(ini, end+1)))
    return data
