from enum import Enum

"""
MoveCodes explanation:
    HERE: destination is the same region
    OUT: destination is the parent region
    IN: destination is a region whithin the current one
    MEM: destination of elements is other region at same level
    DISS: dissolve region and remove its elements
    DISS2: dissolve region and its elements go to the parent
    MEMWC: marks a movement of one membrane between regions but in the transmitting región take a copy of the membrane
    MEMTRANS: MEM for plasmid transmision
    GROUP_TRANS: one region pass a % of some membranes to another region at the same level
    MEMwOB: move membranes with some specific object inside
    DMEM: MEM but does de transmition at the moment
"""

# TODO revisar todos los nombres para que sean más significativos

class MoveCodes(Enum):
    HERE = 1
    OUT = 2
    IN = 3
    MEM = 4
    DISS = 5
    DISS2 = 6   # DISS_KEEP
    MEMWC = 7   
    MEMTRANS = 8
    GROUP_TRANS = 9
    MEMwOB = 10
    DMEM = 11
    

class SceneObjects():
    """Allow name changes with minor code impact"""
    MEMBRANE = 'membrane'
    OBJECT = 'BO'
    OBJECT_RULE = 'rBO'
    RULE_LH = 'lh'
    RULE_RH = 'rh'