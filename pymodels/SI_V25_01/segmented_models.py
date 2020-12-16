"""Segmented models of the lattice."""

import math as _math
import numpy as _np
import pyaccel as _pyaccel


def dipole_bc(m_accep_fam_name, simplified=False):
    """Segmented BC dipole model."""
    segtypes = {
        'BC': ('BC', _pyaccel.elements.rbend),
        'BC_EDGE': ('BC_EDGE', _pyaccel.elements.marker),
        'mc': ('mc', _pyaccel.elements.marker),
        'm_accep': (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # Average Dipole Model for BC
    # =============================================
    # date: 2019-06-27
    # Based on multipole expansion around average segmented model trajectory calculated
    # from fieldmap analysis of measurement data
    # folder = si-dipoles-bc/model-13/analysis/hallprobe/production/x0-0p079mm-reftraj
    # init_rx =  79 um
    # ref_rx  = 7.7030 mm (average model trajectory)
    # goal_tunes = [49.096188917357331, 14.151971558423915];
    # goal_chrom = [2.549478494984214, 2.527086095938103];

    monomials = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
    segmodel = [
     #         len[m]  angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)   PolyB(n=7)   PolyB(n=8)   PolyB(n=10)
        ['BC', 0.00100, 0.01877, -1.4741e-05, -3.2459e-03, -2.5934e+01, +2.2655e+02, -4.2041e+05, -1.9362e+06, -8.8515e+08, +1.8066e+10, -4.1927e+13, +1.8535e+17],
        ['BC', 0.00400, 0.07328, -3.5868e-06, -8.0872e-03, -2.3947e+01, +1.9896e+02, -3.8312e+05, -1.5555e+06, -8.7538e+08, +1.5588e+10, -3.4411e+13, +1.5036e+17],
        ['BC', 0.00500, 0.08149, -1.5878e-06, -2.2156e-02, -1.6636e+01, +9.5225e+01, -2.4803e+05, -2.8667e+05, -6.2015e+08, +5.9788e+09, -1.1795e+13, +5.3967e+16],
        ['BC', 0.00500, 0.06914, -2.2515e-06, -2.6794e-02, -9.9744e+00, +4.0910e+01, -1.2934e+05, -1.8459e+04, +6.5912e+06, +1.8432e+09, -3.7282e+12, +1.5831e+16],
        ['BC', 0.00500, 0.05972, +2.4800e-07, -2.6704e-02, -7.1238e+00, +2.8365e+01, -7.1836e+04, -1.7947e+05, +2.5073e+08, +1.9029e+09, -3.3936e+12, +1.2829e+16],
        ['BC', 0.01000, 0.09814, -7.2919e-07, -2.5788e-02, -5.4243e+00, +1.8297e+01, -3.6399e+04, -1.8928e+05, +2.7961e+08, +1.5270e+09, -3.1054e+12, +1.1735e+16],
        ['BC', 0.01000, 0.07568, -1.8658e-06, -2.4549e-02, -3.7961e+00, +7.9939e+00, -1.8270e+04, -9.0518e+04, +2.3235e+08, +8.1040e+08, -2.4656e+12, +9.3410e+15],
        ['BC', 0.01000, 0.05755, -6.9437e-07, -1.9501e-02, -2.2458e+00, +2.9742e+00, -1.0525e+04, -1.8749e+04, +1.6339e+08, +2.9806e+08, -1.6673e+12, +6.2159e+15],
        ['BC', 0.01000, 0.04544, -1.2861e-07, -1.2764e-03, -8.7276e-01, -4.5371e-01, -5.5830e+03, +2.6585e+04, +9.6483e+07, +1.2858e+06, -1.0053e+12, +3.9069e+15],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.03200, 0.11887, -3.6974e-08, +1.2757e-02, +1.1825e+00, +1.8453e+00, -4.6262e+03, +2.4200e+04, +7.3751e+07, -6.3579e+07, -7.8054e+11, +3.0544e+15],
        ['BC', 0.03200, 0.09720, -9.0591e-07, -1.2063e-01, +5.2835e-01, +1.0917e+01, -3.2323e+03, -1.8683e+03, +4.9009e+07, -4.9946e+07, -4.6379e+11, +1.7988e+15],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.16000, 0.62161, -1.1668e-06, -8.9725e-01, +4.4207e-01, +3.2247e+01, +1.9416e+03, -2.8567e+05, -5.0265e+07, +1.4028e+09, +6.1042e+11, -2.5574e+15],
        ['BC', 0.16000, 0.62274, +2.8034e-07, -9.0717e-01, +2.0879e-01, -6.2815e-01, +1.9822e+03, +2.4218e+05, -4.1507e+07, -1.1837e+09, +4.3276e+11, -1.5769e+15],
        ['BC', 0.01200, 0.04249, +5.4796e-07, -8.8611e-01, +4.9910e-01, +2.4958e+01, -9.4206e+03, -1.6025e+05, +1.8960e+08, +8.8432e+08, -1.6666e+12, +5.5453e+15],
        ['BC_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['BC', 0.01400, 0.03339, -4.4895e-07, -4.4684e-01, -1.8750e+00, +2.2077e+01, -5.5912e+03, -1.6748e+05, +1.0327e+08, +9.3221e+08, -8.6332e+11, +2.7550e+15],
        ['BC', 0.01600, 0.01935, +7.1551e-07, -1.1215e-01, -1.9597e+00, +1.3313e+01, -3.5424e+03, -1.6337e+05, +6.3653e+07, +8.9179e+08, -5.4044e+11, +1.7393e+15],
        ['BC', 0.03500, 0.01344, -1.7487e-07, -1.9828e-02, -1.2534e+00, +1.9342e+01, +2.8084e+03, -2.9546e+05, -5.0640e+07, +1.4694e+09, +4.0940e+11, -1.2172e+15]
    ]

    # turns deflection angle error off (convenient for having a nominal model
    # with zero 4d closed orbit)
    for i in range(len(segmodel)):
        segmodel[i][3] = 0.0

    model = []

    # --- creates half model ---
    d2r = _math.pi/180.0
    PolyB = _np.zeros(1+max(monomials))
    for i in range(len(segmodel)):
        fam_name, element_type = segtypes[segmodel[i][0]]
        if element_type == _pyaccel.elements.rbend:
            for j in range(len(monomials)):
                PolyB[monomials[j]] = segmodel[i][j+3]
            PolyA = 0 * PolyB
            element = element_type(fam_name=fam_name, length=segmodel[i][1],
                                   angle=d2r * segmodel[i][2],
                                   angle_in=0, angle_out=0,
                                   gap=0, fint_in=0, fint_out=0,
                                   polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mc = segtypes['mc'][1](segtypes['mc'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mc, maccep] + model

    if simplified:
        m_accep = _pyaccel.elements.marker(m_accep_fam_name)
        le = sum([s[1] for s in segmodel[:8]])
        ang1 = sum([s[2] for s in segmodel[:8]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[:8]])/le
        s = sum([s[5]*s[1] for s in segmodel[:8]])/le
        el = _pyaccel.elements.rbend(fam_name='BC', length=2*le, angle=2*ang1,
                                     angle_in=0, angle_out=0,
                                     gap=0, fint_in=0, fint_out=0,
                                     polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        le = sum([s[1] for s in segmodel[9:14]])
        ang2 = sum([s[2] for s in segmodel[9:]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[9:]])/le
        s = sum([s[5]*s[1] for s in segmodel[9:]])/le
        el_e = _pyaccel.elements.rbend(
            fam_name='BC', length=le, angle=ang2,
            angle_in=0, angle_out=0*ang2,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        el_b = _pyaccel.elements.rbend(
            fam_name='BC', length=le, angle=ang2,
            angle_in=0*ang2, angle_out=0,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[14:]])
        dr = _pyaccel.elements.drift('LBC', l2)
        model = [dr, el_b, m_accep, el, m_accep, el_e, dr]

    return model


def dipole_b1(m_accep_fam_name, simplified=False):
    """Segmented B1 dipole model."""
    segtypes = {
        'B1': ('B1', _pyaccel.elements.rbend),
        'B1_EDGE': ('B1_EDGE', _pyaccel.elements.marker),
        'mb1': ('mb1', _pyaccel.elements.marker),
        'm_accep': (m_accep_fam_name, _pyaccel.elements.marker),
    }

    # Average Dipole Model for B1 at current 403p6A
    # =============================================
    # date: 2019-01-30
    # Based on multipole expansion around average segmented model trajectory
    # calculated from fieldmap analysis of measurement data
    # init_rx =  8.527 mm
    # ref_rx  = 13.693 mm (average model trajectory)
    # goal_tunes = [49.096188917357331, 14.151971558423915];
    # goal_chrom = [2.549478494984214, 2.527086095938103];

    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
        # type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        ['B1', 0.00200, 0.00633, -1.9696e-06, -7.2541e-01, -5.4213e-01, +5.4347e+00, +2.5091e+02, +4.9772e+02, -1.9113e+06],
        ['B1', 0.00300, 0.00951, -3.8061e-06, -7.2968e-01, -4.5292e-01, +4.3822e+00, +3.1863e+02, +1.5282e+03, -2.3387e+06],
        ['B1', 0.00500, 0.01592, -4.7568e-07, -7.4227e-01, -2.1669e-01, +2.9544e+00, +2.9316e+02, +1.4632e+03, -2.0877e+06],
        ['B1', 0.00500, 0.01603, -1.9480e-06, -7.5771e-01, -1.0657e-02, +3.5007e+00, +2.9571e+02, -1.7742e+03, -2.0010e+06],
        ['B1', 0.00500, 0.01611, -2.7633e-06, -7.6662e-01, +3.3285e-02, +4.7919e+00, +3.3381e+02, -3.3109e+03, -2.0402e+06],
        ['B1', 0.01000, 0.03236, -1.9098e-06, -7.7081e-01, +1.6451e-02, +5.3028e+00, +3.7119e+02, -4.8877e+03, -2.0590e+06],
        ['B1', 0.04000, 0.12963, -1.6309e-06, -7.7247e-01, +4.8673e-02, +4.6505e+00, +3.3306e+02, -2.1646e+03, -1.5868e+06],
        ['B1', 0.15000, 0.48382, -1.9888e-06, -7.7332e-01, +9.7601e-02, +5.3336e+00, +2.5126e+02, +8.0649e+02, -9.2335e+05],
        ['B1', 0.10000, 0.32247, -2.1025e-06, -7.7271e-01, +1.1969e-01, +5.6811e+00, +2.1496e+02, +5.2023e+03, -6.0518e+05],
        ['B1', 0.05000, 0.16165, -2.1257e-06, -7.7203e-01, +5.6224e-02, +4.5293e+00, +6.3908e+01, +6.1651e+03, +3.4951e+05],
        ['B1', 0.03400, 0.10509, -1.8623e-06, -7.7144e-01, -1.2160e-01, +9.1976e+00, -5.3231e+01, +9.0360e+03, +7.2783e+05],
        ['B1_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['B1', 0.01600, 0.03414, -9.6169e-07, -4.5231e-01, -1.8149e+00, +1.9400e+01, -2.2843e+02, +1.6525e+04, -4.0477e+04],
        ['B1', 0.04000, 0.03296, -5.2504e-07, -8.6643e-02, -1.7536e+00, +8.5147e+00, -5.8350e+01, +4.2954e+03, -3.7834e+04],
        ['B1', 0.04000, 0.00774, -1.6259e-07, -8.3065e-03, -3.8990e-01, +1.3183e+00, +2.5814e+01, +3.1642e+02, -5.0464e+04],
        ['B1', 0.05000, 0.00389, -7.9445e-08, -1.0742e-03, -9.8271e-02, +5.0359e-02, -1.0312e+01, +9.0013e+02, +8.2477e+04],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    # turns deflection angle error off (convenient for having a nominal model
    # with zero 4d closed orbit)
    for i in range(len(segmodel)):
        segmodel[i][3] = 0.0

    model = []

    # --- creates half model ---
    d2r = _math.pi/180.0
    PolyB = _np.zeros(1+max(monomials))
    for i in range(len(segmodel)):
        fam_name, element_type = segtypes[segmodel[i][0]]
        if element_type == _pyaccel.elements.rbend:
            for j in range(len(monomials)):
                PolyB[monomials[j]] = segmodel[i][j+3]
            PolyA = 0 * PolyB
            element = element_type(fam_name=fam_name, length=segmodel[i][1],
                                   angle=d2r * segmodel[i][2],
                                   angle_in=0, angle_out=0,
                                   gap=0, fint_in=0, fint_out=0,
                                   polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mb1 = segtypes['mb1'][1](segtypes['mb1'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mb1, maccep] + model

    if simplified:
        le = sum([s[1] for s in segmodel[:12]])
        ang = sum([s[2] for s in segmodel]) * d2r
        k = sum([s[4]*s[1] for s in segmodel])/le
        s = sum([s[5]*s[1] for s in segmodel])/le
        el = _pyaccel.elements.rbend(
            fam_name='B1', length=2*le, angle=2*ang,
            angle_in=0*ang, angle_out=0*ang,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[12:]])
        dr = _pyaccel.elements.drift('LB1', l2)
        model = [dr, el, dr]

    return model


def dipole_b2(m_accep_fam_name, simplified=False):
    """Segmented B2 dipole model."""
    segtypes = {
        'B2': ('B2', _pyaccel.elements.rbend),
        'B2_EDGE': ('B2_EDGE', _pyaccel.elements.marker),
        'mb2': ('mb2', _pyaccel.elements.marker),
        'm_accep': (m_accep_fam_name, _pyaccel.elements.marker),
    }

    #  Average Dipole Model for B2 at current 401p8A
    #  =============================================
    #  date: 2019-01-30
    #  Based on multipole expansion around average segmented model trajectory calculated
    #  from fieldmap analysis of measurement data
    #  init_rx =  8.153 mm
    #  ref_rx  = 19.428 mm (average model trajectory)
    #  goal_tunes = [49.096188917357331, 14.151971558423915];
    #  goal_chrom = [2.549478494984214, 2.527086095938103];

    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
        #type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        ['B2', 0.12500, 0.40623, +2.8141e-07, -7.7535e-01, +3.8504e-02, +1.7048e+00, -2.6809e+02, +8.8090e+03, +1.8541e+06],
        ['B2', 0.05500, 0.17963, +2.4869e-07, -7.7400e-01, +1.8903e-02, +1.3538e+00, -2.7871e+02, +8.4667e+03, +1.7913e+06],
        ['B2', 0.01000, 0.03260, -1.4532e-07, -7.6990e-01, -7.3993e-03, +1.4325e+00, -3.7053e+02, +9.0098e+03, +1.8818e+06],
        ['B2', 0.00500, 0.01624, -9.6976e-07, -7.6272e-01, -4.4905e-02, +3.7505e-01, -4.0759e+02, +1.0527e+04, +1.8729e+06],
        ['B2', 0.00500, 0.01619, -8.5112e-08, -7.5413e-01, -1.7000e-01, +1.3254e-01, -4.2095e+02, +1.2650e+04, +1.8762e+06],
        ['B2', 0.00500, 0.01616, +5.0825e-07, -7.4866e-01, -2.8166e-01, +7.1392e-01, -3.5386e+02, +1.3287e+04, +1.5160e+06],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['B2', 0.00500, 0.01618, +1.7001e-06, -7.5218e-01, -2.1312e-01, +3.8486e-01, -3.9031e+02, +1.2889e+04, +1.7072e+06],
        ['B2', 0.01000, 0.03254, +1.3585e-06, -7.6428e-01, -4.1565e-02, +6.7680e-01, -4.0577e+02, +1.0602e+04, +1.8735e+06],
        ['B2', 0.01000, 0.03269, +2.9027e-07, -7.7165e-01, -8.0002e-03, +1.7812e+00, -3.2568e+02, +8.2067e+03, +1.7365e+06],
        ['B2', 0.17500, 0.57073, -1.1637e-07, -7.7428e-01, +6.8988e-02, +4.1024e+00, -5.1871e+01, +7.5752e+02, +5.9943e+05],
        ['B2', 0.17500, 0.57034, -3.3225e-07, -7.7352e-01, +7.8447e-02, +5.4514e+00, +1.9975e+02, +3.3621e+03, -3.1314e+05],
        ['B2', 0.02000, 0.06315, +2.2577e-08, -7.8534e-01, -1.4538e-01, +9.2976e+00, -1.5715e+02, +1.2311e+04, +1.1408e+06],
        ['B2', 0.01000, 0.02719, +8.7645e-08, -6.7626e-01, -3.1354e-01, +1.6050e+01, -3.9938e+02, +1.6288e+04, +8.1085e+05],
        ['B2_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['B2', 0.01500, 0.02866, +6.3204e-08, -3.6034e-01, -2.3415e+00, +2.0402e+01, -3.9166e+02, +1.9055e+04, +3.1586e+05],
        ['B2', 0.02000, 0.01994, +5.4460e-07, -1.0711e-01, -2.1654e+00, +1.1296e+01, -1.7816e+02, +7.2357e+03, +1.6786e+05],
        ['B2', 0.03000, 0.01188, +1.3393e-07, -2.3886e-02, -8.9207e-01, +3.8284e+00, -1.5146e+01, +5.3693e+02, +7.8230e+04],
        ['B2', 0.03200, 0.00444, -2.8999e-07, -4.5556e-03, -2.6166e-01, +7.8754e-01, +1.5573e+00, +8.3579e+01, +3.8831e+04],
        ['B2', 0.03250, 0.00341, -1.3468e-07, -1.2481e-03, -1.3069e-01, +3.6679e-01, +1.3671e+01, -7.7370e+02, -2.9544e+04],
        ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    # turns deflection angle error off (convenient for having a nominal model
    # with zero 4d closed orbit)
    for i in range(len(segmodel)):
        segmodel[i][3] = 0.0

    model = []

    # --- creates half model ---
    d2r = _math.pi/180.0
    PolyB = _np.zeros(1+max(monomials))
    for i in range(len(segmodel)):
        fam_name, element_type = segtypes[segmodel[i][0]]
        if element_type == _pyaccel.elements.rbend:
            for j in range(len(monomials)):
                PolyB[monomials[j]] = segmodel[i][j+3]
            PolyA = 0 * PolyB
            element = element_type(
                fam_name=fam_name, length=segmodel[i][1],
                angle=d2r * segmodel[i][2],
                angle_in=0, angle_out=0,
                gap=0, fint_in=0, fint_out=0,
                polynom_a=PolyA, polynom_b=PolyB)
        else:
            element = element_type(fam_name)
        model.append(element)

    # --- adds additional markers ---
    mb2 = segtypes['mb2'][1](segtypes['mb2'][0])
    maccep = segtypes['m_accep'][1](segtypes['m_accep'][0])
    model = model[::-1] + [mb2, maccep] + model

    if simplified:
        le = sum([s[1] for s in segmodel[:15]])
        ang = sum([s[2] for s in segmodel]) * d2r
        k = sum([s[4]*s[1] for s in segmodel])/le
        s = sum([s[5]*s[1] for s in segmodel])/le
        el = _pyaccel.elements.rbend(
                fam_name='B2', length=2*le, angle=2*ang,
                angle_in=0*ang, angle_out=0*ang,
                gap=0, fint_in=0, fint_out=0,
                polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[15:]])
        dr = _pyaccel.elements.drift('LB2', l2)
        model = [dr, el, dr]

    return model


def quadrupole_q14(fam_name, strength, simplified=False):
    """Segmented Q14 quadrupole model."""
    segtypes = {
        fam_name: (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q14 model
    # =========
    # this (half) model is based on fieldmap
    # '2017-02-24_Q14_Model04_Sim_X=-14_14mm_Z=-500_500mm_Imc=146.6A_Itc=10A.txt'
    monomials = [1, 5, 9, 13]
    segmodel = [
        # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)
        #                            PolyB(n=13)
        [fam_name, 0.0700, +0.00000, -4.06e+00, +6.38e+04, -1.45e+13,
         +2.90e+20],
    ]

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in
                     range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name,
                           length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model


def quadrupole_q20(fam_name, strength, simplified=False):
    """Segmented Q20 quadrupole model."""
    segtypes = {
        fam_name: (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q20 model
    # =========
    # this (half) model is based on fieldmap
    # '2017-02-24_Q20_Model05_Sim_X=-14_14mm_Z=-500_500mm_Imc=
    #  154.66A_Itc=10A.txt'
    monomials = [1, 5, 9, 13]
    segmodel = [
        # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)
        #                                                      PolyB(n=13)
        [fam_name, 0.1000, +0.00000, -4.74e+00, +8.41e+04, -1.83e+13,
         +3.47e+20],
    ]

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in
                     range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name,
                           length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model


def quadrupole_q30(fam_name, strength, simplified=False):
    """Segmented Q30 quadrupole model."""
    segtypes = {
        fam_name: (fam_name, _pyaccel.elements.quadrupole),
    }

    # Q30 model
    # =========
    # this (half) model is based on fieldmap
    # '2017-02-24_Q30_Model06_Sim_X=-14_14mm_Z=-500_500mm_Imc=
    #  153.8A_Itc=10A.txt'
    monomials = [1, 5, 9, 13]
    segmodel = [
        # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)
        #                                                      PolyB(n=13)
        [fam_name, 0.1500, +0.00000, -4.75e+00, +1.06e+05, -1.95e+13,
         +3.56e+20],
    ]

    # rescale fieldmap data to strength argument
    quadidx = monomials.index(1)
    seg_lens = [segmodel[i][1] for i in range(len(segmodel))]
    model_length = 2 * sum(seg_lens)
    fmap_strength = [2*segmodel[i][3+quadidx]*seg_lens[i]/model_length for i in
                     range(len(segmodel))]
    rescale = [strength / fmap_strength[i] for i in range(len(segmodel))]

    # --- hard-edge 1-segment model ---
    model = []
    i = 0
    fam_name, element_type = segtypes[segmodel[i][0]]
    PolyB = _np.zeros(1+max(monomials))
    for j in range(len(monomials)):
        PolyB[monomials[j]] = segmodel[i][j+3] * rescale[i]
    PolyA = 0 * PolyB
    element = element_type(fam_name=fam_name,
                           length=2*segmodel[i][1], K=PolyB[1])
    element.polynom_a = PolyA
    element.polynom_b = PolyB
    model.append(element)

    if simplified:
        model[0].polynom_a = model[0].polynom_a[:3]
        model[0].polynom_b = model[0].polynom_b[:3]

    return model
