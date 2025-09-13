# P-System Membrane Computing Simulator

A Python implementation of P-Systems (Membrane Computing) simulator that models biological membranes and their interactions through rule-based transformations.

## 🧬 Overview

This simulator implements P-Systems, a computational model inspired by the structure and functioning of biological cells. The system consists of membranes containing objects that evolve according to transformation rules, simulating complex biological processes through mathematical abstractions.

### Key Features

- **Membrane Hierarchies**: Support for nested membrane structures
- **Rule-Based Evolution**: Object transformations through probabilistic rules
- **Multiple Inference Modes**: Minimal parallel and sequential execution
- **Movement Operations**: Objects can move between membranes (HERE, OUT, IN, MEM, etc.)
- **Priority Systems**: Rule prioritization for conflict resolution
- **Probabilistic Execution**: Stochastic rule application based on probabilities
- **Visualization**: Membrane structure plotting and evolution tracking
- **Flexible Input**: XML scene definition support

## 📋 Requirements

- Python 3.10+
- NumPy
- Additional dependencies listed in requirements.txt

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/adrimrtnz/psys-sim.git
cd p-system-simulator
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage

1. **Configure the simulation** in `config.ini`:
```ini
[Input]
Format=xml
Scene=scene_00
Rules=rules_00

[Runtime]
Inference=minpar
Seed=42
MaxSteps=4
```

2. **Run the simulation**:
```bash
python main.py
```

### Using the GUI

There is a tinny GUI made with [Streamlit](https://streamlit.io/). To use it just follow these commands:

```bash
# 1. Navigate to the frontend directory
cd services/front

# 2. Install the required dependencies
pip install -r requirements.txt

# 3. Start the application
streamlit run app.py
```

This should automatically open the url `http://localhost:8501` in your default browser.

#### Additional Options

#### Additional Options

| Option | Example | Description |
|--------|---------|-------------|
| `--server.port` | `--server.port 8502` | Runs the app on a specific port (default: 8501). |
| `--server.address` | `--server.address 0.0.0.0` | Binds the server to a specific address. Useful for Docker/remote servers. |
| `--server.headless` | `--server.headless true` | Runs without trying to open a browser. Useful on servers without GUI. |
| `--server.baseUrlPath` | `--server.baseUrlPath myapp` | Serves the app under a subpath, e.g. `http://localhost:8501/myapp`. |
| `--server.fileWatcherType` | `--server.fileWatcherType none` | Controls how Streamlit watches for file changes. `none` can reduce CPU usage. |
| `--browser.serverAddress` | `--browser.serverAddress localhost` | Override the address shown in the browser. |
| `--browser.gatherUsageStats` | `--browser.gatherUsageStats false` | Disable anonymous usage statistics reporting. |

## 🏗️ Architecture

### Core Components

```
src/
├── classes/
│   ├── membrane.py              # Membrane structure and operations
│   ├── objects_multiset.py      # Multiset implementation for objects
│   ├── rule.py                  # Rule definitions and properties
│   └── p_system.py              # Main P-System orchestrator
├── enums/
│   └── constants.py             # System constants and enums
├── interfaces/
│   └── multiset_interface.py    # Abstract multiset interface  
└── utils/
    ├── config_parser.py         # Configuration file parser
    ├── xml_parser.py            # XML filetype parser
    └── parser_factory.py        # Scene parser factory
```

### Key Classes

- **`PSystem`**: Main orchestrator managing membranes, rules, and execution
- **`Membrane`**: Represents individual membranes with objects and children
- **`Rule`**: Defines transformation rules with probabilities and movement codes
- **`ObjectsMultiset`**: Manages collections of objects with multiplicities
- **`MultiSetInterface`**: Abstract interface for multiset operations

## 📖 Configuration

### config.ini Structure

```ini
[Input]
# Input format: xml | json (default: xml)
Format=xml
# Scene file to load from scenes/ directory
Scene=scene_00  
# Rules file to load from rules/ directory
Rules=rules_00

[Runtime]
# Inference mode: minpar | maxpar (default: minpar)
Inference=minpar
# Maximum simulation steps (default: unlimited)
MaxSteps=4
```

### Movement Codes

The system supports various movement operations:

- **HERE**: Objects remain in the same membrane
- **OUT**: Objects move to parent membrane  
- **IN**: Objects move to child membrane
- **MEM**: Objects move to sibling membrane
- **DISS**: Dissolve membrane and remove objects
- **DISS_KEEP**: Dissolve membrane, objects go to parent
- **MEMWC**: Copy membrane during movement
- **MEMTRANS**: Membrane movement for plasmid transmission
- **GROUP_TRANS**: Percentage-based membrane group transfer
- **MEMwOB**: Move membranes containing specific objects
- **DMEM**: Immediate membrane transmission

## 🔧 Usage Examples


### Rule Definition

Rules define how objects transform and move:

```python
# Example: a + b → c (with probability 0.8, priority 2)
left_multiset = ObjectsMultiset({'a': 1, 'b': 1})
right_multiset = ObjectsMultiset({'c': 1})
rule = Rule(
    left=left_multiset,
    right=right_multiset, 
    prob=0.8,
    prior=None,
    move=MoveCode.HERE
)
```

## 🧪 Inference Modes

### Minimally Parallel (`minpar`)
- At most one rule per membrane per step
- Probabilistic rule selection
- Handles rule conflicts through priorities
- Default execution mode


### Maximally Parallel (`maxpar`)
- Apply, at each step, a non-extendable number of rules.


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the Google docstring style for documentation
4. Add tests for new functionality
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Documentation Standards

This project follows Google-style docstrings:

```python
def example_function(param1: int, param2: str) -> bool:
    """Brief description of the function.
    
    Longer description if needed.
    
    Args:
        param1 (int): Description of first parameter.
        param2 (str): Description of second parameter.
        
    Returns:
        bool: Description of return value.
        
    Raises:
        ValueError: When param1 is negative.
    """
    pass
```

## 📝 Build the HTML Documentation

To generate the project's documentation locally, follow these steps. The documentation is built using Sphinx.

1. Navigate to the documentation directory
```bash
cd docs
```

2. Install the required dependencies:

```bash
pip install sphinx==8.2.3 sphinx-rtd-theme==3.0.2
```

3. Build the html file

```bash
make html
```

4. View the documentation: After the build process is complete, you can find the generated site in the `docs/build/html` directory. Open the `index.html` file in your browser to view the documentation.

## 📚 References

- Păun, Gheorghe. "Membrane Computing: An Introduction." Springer, 2002.
- [P-Systems Website](http://ppage.psystems.eu/)
- [P-lingua](http://www.p-lingua.org/wiki/index.php/Main_Page)
- [A Formal Framework for P Systems, paper by R. Freund and S. Verlan](https://www.researchgate.net/publication/249783920_A_Formal_Framework_for_P_Systems)

