"""Segmented models of the lattice."""

import math as _math
import numpy as _np
import pyaccel as _pyaccel


def dipole(sign, simplified=False):
    """Segmented TS dipole model."""
    segtypes = {
        'b': ('B', _pyaccel.elements.rbend),
        'b_edge': ('edgeB', _pyaccel.elements.marker),
        'b_pb': ('physB', _pyaccel.elements.marker),
    }

    # dipole model 2019-10-31
    # Interpolated Dipole Model for TS at 3GeV (698.85A) for BD-006 (interpolation of 680A and 720A data)
    # ===============================================
    monomials = [0, 1, 2, 3, 4, 5, 6]
    segmodel = [
        # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
        # type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        ['b',      0.19600, 0.809257, +0.0000e+00, -1.5054e-01, -1.3448e+00, -2.8514e+00, +4.9654e+01, -9.7962e+03, -1.4425e+06],
        ['b',      0.19200, 0.797120, +0.0000e+00, -1.4328e-01, -1.3380e+00, -2.7288e+00, +2.1067e+02, +5.1905e+03, -1.6808e+06],
        ['b',      0.18200, 0.760060, +0.0000e+00, -1.3084e-01, -1.3232e+00, +7.4249e-01, -9.9878e+01, -2.2005e+03, +1.5113e+05],
        ['b',      0.01000, 0.034611, +0.0000e+00, -1.5176e-01, -1.2704e+00, +6.8939e+00, +4.2288e+01, +8.9753e+03, -1.5715e+06],
        ['b',      0.01000, 0.025086, +0.0000e+00, -9.5750e-02, -1.0544e+00, +1.0254e+01, -1.5327e+02, +9.3432e+03, -1.8207e+06],
        ['b_edge', 0,0,0,0,0,0,0,0,0],
        ['b',      0.01300, 0.022508, +0.0000e+00, -3.2273e-02, -1.3281e+00, +1.0407e+01, -3.2405e+02, +9.0864e+03, -9.2305e+05],
        ['b',      0.01700, 0.020260, +0.0000e+00, -1.0375e-03, -1.5937e+00, +5.8647e+00, -2.3126e+02, +5.5698e+03, -3.9056e+04],
        ['b',      0.02000, 0.015855, +0.0000e+00, +9.8129e-03, -1.5127e+00, +1.1375e+00, -4.5477e+01, +2.0338e+03, +2.1443e+05],
        ['b',      0.03000, 0.013028, +0.0000e+00, +9.4251e-03, -1.0114e+00, -7.6112e-01, +7.4214e+01, +9.2988e+02, -1.1137e+05],
        ['b',      0.05000, 0.007986, -8.5102e-07, +3.1611e-03, -3.4872e-01, -9.4469e-01, +4.3492e+01, +1.9965e+03, -1.4370e+05],
        ['b_pb',   0,0,0,0,0,0,0,0,0],
    ]

    d2r = _math.pi/180.0
    for i in range(len(segmodel)):
        segmodel[i][2] = sign * segmodel[i][2]
        # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
        segmodel[i][3] = 0.0

    # # --- manipule polynomialB ---
    # for i in range(len(segmodel)):
    #     # invert sign of bending angle, if the case.
    #     segmodel[i][2] = sign * segmodel[i][2]
    #     # invert sign of odd-order polynomb, if the case.
    #     for j in range(0, len(monomials)):
    #         segmodel[i][3+j] *= sign**monomials[j]
    #     # turns deflection angle error off
    #     segmodel[i][3] = 0.0

    # --- creates half model ---
    model = []
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
    mb = _pyaccel.elements.marker('mB')
    model = model[::-1] + [mb] + model

    if simplified:
        le = sum([s[1] for s in segmodel[:8]])
        ang1 = sum([s[2] for s in segmodel[:8]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[:8]])/le
        s = sum([s[5]*s[1] for s in segmodel[:8]])/le
        el = _pyaccel.elements.rbend(fam_name='B', length=2*le, angle=2*ang1,
                                     angle_in=0, angle_out=0,
                                     gap=0, fint_in=0, fint_out=0,
                                     polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        le = sum([s[1] for s in segmodel[9:14]])
        ang2 = sum([s[2] for s in segmodel[9:]]) * d2r
        k = sum([s[4]*s[1] for s in segmodel[9:]])/le
        s = sum([s[5]*s[1] for s in segmodel[9:]])/le
        el_e = _pyaccel.elements.rbend(
            fam_name='B', length=le, angle=ang2,
            angle_in=0, angle_out=0*ang2,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        el_b = _pyaccel.elements.rbend(
            fam_name='B', length=le, angle=ang2,
            angle_in=0*ang2, angle_out=0,
            gap=0, fint_in=0, fint_out=0,
            polynom_a=[0, 0, 0], polynom_b=[0, k, s])
        l2 = sum([s[1] for s in segmodel[14:]])
        dr = _pyaccel.elements.drift('LBC', l2)
        model = [dr, el_b, el, el_e, dr]
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


def setpum(dip_nam, dip_len, dip_ang, strengths, nseg=6):
    if nseg < 2:
        raise Exception('Number of segments must be >= 2.')
    rbend_sirius = _pyaccel.elements.rbend
    m66 = _pyaccel.elements.matrix
    marker = _pyaccel.elements.marker
    deg_2_rad = _math.pi / 180.0

    polya = [0, 0, 0]
    polyb = [0, 0, 0]

    matrix_name = dip_nam + 'M66'
    dip_ang = dip_ang * deg_2_rad

    dip_kxl = strengths[dip_nam.lower()+'_kxl']
    dip_kyl = strengths[dip_nam.lower()+'_kyl']
    dip_ksxl = strengths[dip_nam.lower()+'_ksxl']
    dip_ksyl = strengths[dip_nam.lower()+'_ksyl']

    seg_len = dip_len / nseg
    seg_ang = dip_ang / nseg

    seg_kxl = dip_kxl / (nseg - 1)
    seg_kyl = dip_kyl / (nseg - 1)
    seg_ksxl = dip_ksxl / (nseg - 1)
    seg_ksyl = dip_ksyl / (nseg - 1)

    septe = rbend_sirius(
        fam_name=dip_nam, length=seg_len, angle=seg_ang,
        angle_in=dip_ang/2, angle_out=0,
        gap=0, fint_in=0, fint_out=0,
        polynom_a=polya, polynom_b=polyb)
    septs = rbend_sirius(
        fam_name=dip_nam, length=seg_len, angle=seg_ang,
        angle_in=0, angle_out=dip_ang/2,
        gap=0, fint_in=0, fint_out=0,
        polynom_a=polya, polynom_b=polyb)

    matrix = m66(matrix_name, 0)
    matrix.KxL = seg_kxl
    matrix.KyL = seg_kyl
    matrix.KsxL = seg_ksxl
    matrix.KsyL = seg_ksyl

    segs = [matrix, ]
    element = rbend_sirius(
        fam_name=dip_nam, length=seg_len, angle=seg_ang,
        angle_in=0, angle_out=0,
        gap=0, fint_in=0, fint_out=0,
        polynom_a=polya, polynom_b=polyb)

    if nseg > 2:
        for _ in range(nseg-2):
            segs.append(_pyaccel.elements.Element(element))
            segs.append(_pyaccel.elements.Element(matrix))

    bgn = marker('b'+dip_nam)  # marker at the beginning of thin septum
    mdl = marker('m'+dip_nam)  # marker at the center of thin septum
    fin = marker('e'+dip_nam)  # marker at the end of thin septum
    segs = segs[:len(segs)//2] + [mdl] + segs[len(segs)//2:]
    model = [bgn, septe] + segs + [septs, fin]
    return model
