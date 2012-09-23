import os
import os.path

_tp = os.path.split(os.path.abspath(__file__))[0]

ONLINE = os.getenv('minestatus', 'offline') == 'offline'

ENTROPY = os.path.join(_tp, 'entropy.dat')