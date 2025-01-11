# Zaragoza Emergency Response MAS

A Multi-Agent System for coordinating emergency responses in Zaragoza, Spain. This system utilizes CrewAI to orchestrate various emergency service crews for effective incident management.

## Features

- Coordinate multiple emergency response crews (Fire, Medical, Police)
- Real-time distance calculations using OSMnx
- Intelligent resource allocation
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

## Configuration

1. Create necessary configuration files:
```bash
cp .env.example .env
```

2. Update the configuration files in the `config/` directory as needed:
- `emergency_agents.yaml`
- `fire_agents.yaml`
- `medical_agents.yaml`
- `police_agents.yaml`
- `combiner_agents.yaml`

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
├── emergency_solver/   # Main package
│   ├── crews/         # Agent crews
│   ├── schemas/       # Pydantic models
│   └── tools/         # Custom tools
├── config/            # Configuration files
└── data/              # Resource data
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- [Your Name]
- [Team Member 1]
- [Team Member 2]
- [Team Member 3]

## Acknowledgments

- CrewAI team for the framework
- OSMnx developers for the mapping capabilities
- Zaragoza city data providers
