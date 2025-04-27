from enum import Enum

"""
MoveCodes explanation:
    HERE: destination is the same region
    OUT: destination is the parent region
    IN: destination is a region whithin the current one
    MEM: destination of elements is other region at same level
    DISS: dissolve region and remove its elements
    DISS_KEEP: dissolve region and its elements go to the parent
    MEM_WC: marks a movement of one membrane between regions but in the transmitting región take a copy of the membrane
    MEM_TRANS: MEM for plasmid transmision
    GROUP_TRANS: one region pass a % of some membranes to another region at the same level
    MEM_W_OB: move membranes with some specific object inside
    DMEM: MEM but does de transmition at the moment
"""

# TODO revisar todos los nombres para que sean más significativos

class MoveCodes(Enum):
    HERE = 1
    OUT = 2
    IN = 3
    MEM = 4
    DISS = 5
    DISS_KEEP = 6   # Cambia nombre respecto a DISS2 (revisar dependencia)
    MEM_WC = 7      # Cambia nombre respecto a MEMWC (revisar dependencia)
    MEM_TRANS = 8   # Cambia nombre respecto a MEMTRANS (revisar dependencia)
    GROUP_TRANS = 9
    MEM_W_OB = 10   # Cambia nombre respecto a MEMwOB (revisar dependencia)
    DMEM = 11
    

class SceneObjects():
    """Allow name changes with minor code impact"""
    MEMBRANE = 'membrane'
    OBJECT = 'BO'