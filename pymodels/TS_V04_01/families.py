"""Element family definitions"""

import pyaccel as _pyaccel


_family_segmentation = {
    'B': 20, 'CH': 1, 'CV':  1,
    'QF1A': 1, 'QF1B': 1, 'QD2': 1, 'QF2': 1, 'QF3': 1,
    'QD4A': 1, 'QF4': 1, 'QD4B': 1,
    'InjSeptF': 6, 'InjSeptG': 6, 'EjeSeptF': 6, 'EjeSeptG': 6,
    'ICT': 1, 'FCT': 1, 'Scrn': 1, 'BPM': 1
    }

family_mapping = {
    'B': 'dipole',

    'CH': 'horizontal_corrector',
    'CV': 'vertical_corrector',

    'QF1A': 'quadrupole',
    'QF1B': 'quadrupole',
    'QD2': 'quadrupole',
    'QF2': 'quadrupole',
    'QF3': 'quadrupole',
    'QD4A': 'quadrupole',
    'QF4': 'quadrupole',
    'QD4B': 'quadrupole',

    'InjSeptF': 'pulsed_magnet',
    'InjSeptG': 'pulsed_magnet',
    'EjeSeptF': 'pulsed_magnet',
    'EjeSeptG': 'pulsed_magnet',

    'ICT': 'beam_current_monitor',
    'FCT': 'beam_current_monitor',
    'Scrn': 'beam_profile_monitor',
    'BPM': 'bpm'
    }


def families_dipoles():
    return ['B']


def families_pulsed_magnets():
    return ['InjSeptF', 'InjSeptG', 'EjeSeptF', 'EjeSeptG']


def families_quadrupoles():
    return ['QF1A', 'QF1B', 'QD2', 'QF2', 'QF3', 'QD4A', 'QF4', 'QD4B']


def families_horizontal_correctors():
    return ['CH']


def families_vertical_correctors():
    return ['CV']


def families_sextupoles():
    return []


def families_skew_correctors():
    return []


def families_rf():
    return []


def families_di():
    return ['ICT', 'FCT', 'BPM', 'Scrn']


def get_section_name_mapping(lattice):
    section_map = len(lattice)*['']

    # Find indices important to define the change of the names of the sections
    b = _pyaccel.lattice.find_indices(lattice, 'fam_name', 'B')
    b_nrsegs = len(b)//3

    # Names of the sections:
    secs = ['01', '02', '03', '04']

    # conditions that define change in section name:
    relev_inds = [b[b_nrsegs-1], b[2*b_nrsegs-1], b[-1]]
    relev_inds += [len(lattice)-1]
    relev_inds.sort()
    # fill the section_map variable
    ref = 0
    for j in range(len(lattice)):
        section_map[j] += secs[ref]
        if j >= relev_inds[ref]:
            ref += 1

    return section_map


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name.

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice, 'fam_name')
    section_map = get_section_name_mapping(lattice)

    # Fill the data dictionary with index info ######
    data = {}
    for key, idx in latt_dict.items():
        nr = _family_segmentation.get(key)
        if nr is None:
            continue
        # Create a list of lists for the indexes
        data[key] = [idx[i*nr:(i+1)*nr] for i in range(len(idx)//nr)]

    # ch - slow horizontal correctors
    idx = []
    fams = ['QF1B', 'QF2', 'QF3', 'QF4']
    for fam in fams:
        idx.extend(data[fam])
    data['CH'] = sorted(idx, key=lambda x: x[0])

    # cv - slow horizontal correctors (inside quadrupoles)
    idx = []
    fams = ['QF1A', 'QD2', 'QD4A', 'QD4B', 'CV']
    for fam in fams:
        idx.extend(data[fam])
    data['CV'] = sorted(idx, key=lambda x: x[0])

    # now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [section_map[i[0]] for i in idx]

        # find out if there are more than one element per section and
        # attribute a number to it
        num = len(secs)*['']
        if len(secs) > 1:
            j = 1
            if secs[0] == secs[1]:
                num[0] = '{0:d}'.format(j)
                j += 1
            for i in range(1, len(secs)-1):
                if secs[i] == secs[i+1] or secs[i] == secs[i-1]:
                    num[i] = '{0:d}'.format(j)

                if secs[i] == secs[i+1]:
                    j += 1
                else:
                    j = 1

            if secs[-1] == secs[-2]:
                num[-1] = '{0:d}'.format(j)

        new_data[key] = {'index': idx, 'subsection': secs, 'instance': num}

    return new_data
