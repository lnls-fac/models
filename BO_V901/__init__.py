from . import _lattice
from . import _accelerator
from . import _record_names

create_accelerator = _accelerator.create_accelerator

# -- default accelerator values for BO_V901 --

energy = _lattice._energy
harmonic_number = _lattice._harmonic_number
default_cavity_on = _accelerator._default_cavity_on
default_radiation_on = _accelerator._default_cavity_on
default_vchamber_on = _accelerator._default_vchamber_on
default_optics_mode = _lattice._default_optics_mode.label
lattice_symmetry = _lattice._lattice_symmetry
