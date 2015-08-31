import os as _os
from . import LI_V00
from . import TB_V01
from . import BO_V901
from . import TS_V01
#from . import TS_V500
from . import SI_V10

from . import coordinate_system

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['LI_V00', 'TB_V01', 'BO_V901', 'TS_V01', 'SI_V10']

li = LI_V00
tb = TB_V01
bo = BO_V901
ts = TS_V01
si = SI_V10
