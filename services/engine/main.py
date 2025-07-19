from src.utils.config_parser import ConfigParser
from src.utils.parser_factory import SceneParserFactory


"""
Main entry point for the P-System membrane computing simulator.

This module provides the main execution flow for running P-System simulations.
It handles configuration loading, scene parsing, system initialization, and
execution of the membrane computing simulation with output display.
"""

if __name__ == '__main__':
    """Execute the P-System simulation.
    
    Main function that orchestrates the complete simulation workflow:
    1. Loads configuration from config.ini
    2. Creates appropriate parser based on configuration
    3. Parses the scene and rules to build the P-System
    4. Displays initial membrane structure
    5. Runs the simulation for the specified number of steps
    6. Displays final membrane structure
    
    The simulation progress and rule applications are logged to trace files
    and plots are generated during execution.
    """
    config = ConfigParser()
    parser = SceneParserFactory(config)
    system = parser.parse()
    
    print('================ STARTING MEMBRANE STRUCTURE ================')
    system.print_membranes()

    print('\n========================== RULES ===========================')
    system.print_rules()
    system.run(config.max_steps)

    print('\n================== FINAL MEMBRANE STRUCTURE ==================')
    system.print_membranes()
