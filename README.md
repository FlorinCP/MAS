# Zaragoza Emergency Response MAS

A Multi-Agent System for coordinating emergency responses in Zaragoza, Spain. This system utilizes CrewAI to orchestrate various emergency service crews for effective incident management.

## Features

- Coordinate multiple emergency response crews (Fire, Medical, Police)
- Real-time distance calculations using OSMnx
- Efficient resource allocation
- Customizable emergency scenarios
- Comprehensive reporting system

## Prerequisites

- Python 3.9+
- Ollama (for local LLM support)
- OSMnx
- CrewAI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zaragoza-emergency-mas.git
cd zaragoza-emergency-mas
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and download the required model:
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3.1
```

## Usage

1. Generate an emergency report:
```bash
python src/emergency_generator.py
```

2. Run the emergency response system:
```bash
python src/main.py
```

## Project Structure

```
src/
├── emergency_solver/  # Main package
│   ├── crews/         # Agent crews and their specification
│   │   ├── config/    # Agent configuration files (tasks and agents)
│   ├── resources/     # JSON resource files
│   ├── schemas/       # Pydantic models
│   └── tools/         # Custom tools
├── emergency_generator.py  # Emergency report generator
└── main.py                 # Main file from which the MAS is kicked off
```
## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Florin Cosmin Peana
- Ignacio Miguel Rodríguez
- Mar Vidal Cid
- Hugo Prieto Tarrega

## Acknowledgments

- CrewAI team for the framework
- OSMnx developers for the mapping capabilities
- Zaragoza city data providers
