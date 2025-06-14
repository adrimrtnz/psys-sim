from enum import Enum

"""
Constants module for membrane computing system.

This module defines enumerations and constants used throughout the membrane
computing simulation system, including movement codes, scene objects, and
inference types.
"""


class MoveCode(Enum):
    """Enumeration of movement codes for membrane operations.
    
    This enum defines the different types of movements and operations that can
    be performed on membranes and objects within the membrane computing system.
    
    Attributes:
        HERE (int): Destination is the same region.
        OUT (int): Destination is the parent region.
        IN (int): Destination is a region within the current one.
        MEM (int): Destination of elements is other region at same level.
        DISS (int): Dissolve region and remove its elements.
        DISS2 (int): Dissolve region and its elements go to the parent.
        MEMWC (int): Marks a movement of one membrane between regions but in
            the transmitting region take a copy of the membrane.
        MEMTRANS (int): MEM operation for plasmid transmission.
        GROUP_TRANS (int): One region passes a percentage of some membranes
            to another region at the same level.
        MEMwOB (int): Move membranes with some specific object inside.
        DMEM (int): MEM operation but does the transmission at the moment.
    
    Note:
        TODO: Review all names to make them more meaningful.
    """
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
    

class SceneObject():
    """Constants for scene object identifiers.
    
    This class provides string constants for different types of objects
    in the membrane computing scene. It allows name changes with minor
    code impact throughout the system.
    
    Attributes:
        MEMBRANE (str): Identifier for membrane objects.
        MEMBRANE_RULE (str): Identifier for membrane rules.
        OBJECT (str): Identifier for basic objects.
        OBJECT_RULE (str): Identifier for object rules.
        RULE_LH (str): Identifier for left-hand side of rules.
        RULE_RH (str): Identifier for right-hand side of rules.
    """
    MEMBRANE = 'membrane'
    MEMBRANE_RULE = 'rMM'
    OBJECT = 'BO'
    OBJECT_RULE = 'rBO'
    RULE_LH = 'lh'
    RULE_RH = 'rh'


class InferenceType():
    """Constants for inference execution types.
    
    This class defines the different types of inference modes available
    in the membrane computing system.
    
    Attributes:
        MIN_PARALLEL (str): Minimal parallel inference mode.
        SEQUENTIAL (str): Sequential inference mode.
    """
    MIN_PARALLEL = 'minpar'
    SEQUENTIAL = 'sequential'