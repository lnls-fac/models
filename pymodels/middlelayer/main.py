
from collections import OrderedDict

import numpy as np

from siriuspy.epics import PV as _PV
from siriuspy.magnet.factory import NormalizerFactory as _NormFact


class ModelElement():
    def __init__(self, name, model, index, magnet_type):
        self._model = model
        self._indcs = index
        self._name = name
        self._type = magnet_type

    @property
    def magnet_type(self):
        return self._type

    @property
    def model_indices(self):
        return self._indcs

    @property
    def model_nrsegs(self):
        return len(self._indcs)

    @property
    def model_length(self):
        return sum([self._model[idx].length for idx in self._indcs])

    @property
    def model_angle(self):
        return sum([self._model[idx].angle for idx in self._indcs])

    @property
    def model_KL(self):
        return sum([self._model[idx].KL for idx in self._indcs])

    @property
    def model_KsL(self):
        return sum([self._model[idx].KsL for idx in self._indcs])

    @property
    def model_hkick(self):
        return sum([self._model[idx].hkick_polynom for idx in self._indcs])

    @property
    def model_vkick(self):
        return sum([self._model[idx].vkick_polynom for idx in self._indcs])

    @property
    def model_SL(self):
        return sum([self._model[idx].SL for idx in self._indcs])

    @property
    def model_strength(self):
        if self._type.endswith('quadrupole'):
            return self.model_KL * 1
        elif self._type.endswith('sextupole'):
            return self.model_SL * 1
        elif self._type.endswith('horizontal_corrector'):
            return self.model_hkick * 1e6
        elif self._type.endswith('vertical_corrector'):
            return self.model_vkick * 1e6
        elif self._type.endswith('pulsed_magnet'):
            return (self.model_hkick + self.model_angle) * 1e3

    @model_strength.setter
    def model_strength(self, value):
        if self._type.endswith('horizontal_corrector'):
            for idx in self._indcs:
                self._model[idx].hkick_polynom = value * 1e-6
        elif self._type.endswith('vertical_corrector'):
            for idx in self._indcs:
                self._model[idx].vkick_polynom = value * 1e-6
        elif self._type.endswith(('quadrupole', 'sextupole')):
            inival = self.model_strength
            alpha = value/inival * 1
            for idx in self._indcs:
                self._model[idx].polynom_b *= alpha
                self._model[idx].polynom_a *= alpha
        elif self._type.endswith('pulsed_magnet'):
            inival = self.model_strength
            alpha = value/inival * 1e-3
            for idx in self._indcs:
                ang = self._model[idx].angle
                self._model[idx].polynom_b *= alpha
                self._model[idx].polynom_a *= alpha
                self._model[idx].hkick_polynom += ang*(alpha-1)


class Element(ModelElement):

    def __init__(self, name, model, index, magnet_type):
        super().__init__(name, model, index, magnet_type)
        self._norm = _NormFact.create(name)
        prop_sp = 'Current-SP'
        prop_rb = 'Current-RB'
        dis = 'PS'
        if self._type == 'linac_quadrupole':
            prop_sp = 'seti'
            prop_rb = 'rdi'
        elif self._type == 'pulsed_magnet':
            dis = 'PU'
            prop_sp = 'Voltage-SP'
            prop_rb = 'Voltage-RB'
        self._sp = _PV(self._name.substitute(dis=dis, propty=prop_sp))
        self._rb = _PV(self._name.substitute(dis=dis, propty=prop_rb))

    @property
    def connected(self):
        return self._sp.connected & self._rb.connected

    @property
    def strength(self):
        return self._norm.conv_current_2_strength(
            self._rb.value, strengths_dipole=self._model.energy*1e-9)

    @strength.setter
    def strength(self, value):
        self._sp.value = self._norm.conv_strength_2_current(
            value, strengths_dipole=self._model.energy*1e-9)

    @property
    def current(self):
        return self._rb.value

    @current.setter
    def current(self, value):
        self._sp.value = value

    @property
    def model_current(self):
        return self._norm.conv_strength_2_current(
            self.model_strength, strengths_dipole=self._model.energy*1e-9)

    @model_current.setter
    def model_current(self, value):
        self.model_strength = self._norm.conv_current_2_strength(
            value, strengths_dipole=self._model.energy*1e-9)


class Family():

    def __init__(self, name, model, magnets, index, magnet_type):
        self._model = model
        self._elements = OrderedDict()
        for n, idx in zip(magnets, index):
            self._elements[n] = ModelElement(n, model, idx, magnet_type)
        self._indcs = index
        self._name = name
        self._type = magnet_type
        self._norm = _NormFact.create(name)
        prop_sp = 'Current-SP'
        prop_rb = 'Current-RB'
        dis = 'PS'
        if self._type == 'linac_quadrupole':
            prop_sp = 'seti'
            prop_rb = 'rdi'
        elif self._type == 'pulsed_magnet':
            dis = 'PM'
            prop_sp = 'Voltage-SP'
            prop_rb = 'Voltage-RB'
        self._sp = _PV(self._name.substitute(dis=dis, propty=prop_sp))
        self._rb = _PV(self._name.substitute(dis=dis, propty=prop_rb))

    @property
    def model_nrsegs(self):
        return len(self._indcs[0])

    @property
    def nrmagnets(self):
        return len(self._elements)

    @property
    def model_length(self):
        return self._get_from_model('model_length')

    @property
    def model_angle(self):
        return self._get_from_model('model_angle')

    @property
    def model_KL(self):
        return self._get_from_model('model_KL')

    @property
    def model_hkick(self):
        return self._get_from_model('model_hkick')

    @property
    def model_vkick(self):
        return self._get_from_model('model_vkick')

    @property
    def model_SL(self):
        return self._get_from_model('model_SL')

    def _get_from_model(self, attr):
        vals = [getattr(ele, attr) for ele in self._elements.values()]
        return vals[np.argmin(np.abs(vals))]

    @property
    def model_strength(self):
        if self._type.endswith('quadrupole'):
            return self.model_KL * 1
        elif self._type.endswith('sextupole'):
            return self.model_SL * 1
        elif self._type.endswith('horizontal_corrector'):
            return self.model_hkick * 1e6
        elif self._type.endswith('vertical_corrector'):
            return self.model_vkick * 1e6
        elif self._type.endswith('pulsed_magnet'):
            return (self.model_hkick + self.model_angle) * 1e3

    @model_strength.setter
    def model_strength(self, value):
        value -= self.model_strength
        value /= self.model_length
        for ele in self._elements.values():
            ele.model_strength += value*ele.model_length

    @property
    def connected(self):
        return self._sp.connected & self._rb.connected

    @property
    def strength(self):
        return self._norm.conv_current_2_strength(
            self._rb.value, strengths_dipole=self._model.energy*1e-9)

    @strength.setter
    def strength(self, value):
        self._sp.value = self._norm.conv_strength_2_current(
            value, strengths_dipole=self._model.energy*1e-9)

    @property
    def current(self):
        return self._rb.value

    @current.setter
    def current(self, value):
        self._sp.value = value

    @property
    def model_current(self):
        return self._norm.conv_strength_2_current(
            self.model_strength, strengths_dipole=self._model.energy*1e-9)

    @model_current.setter
    def model_current(self, value):
        self.model_strength = self._norm.conv_current_2_strength(
            value, strengths_dipole=self._model.energy*1e-9)


def get_element(name, model, index, magnet_type, magnets=None):
    if name.sub == 'Fam':
        return Family(name, model, magnets, index, magnet_type)
    else:
        return Element(name, model, index, magnet_type)
