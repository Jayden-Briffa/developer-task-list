# Usage
Before any further commands, cd into the src directory
```bash
cd src
```

## Setup
```bash
python -m venv .venv
.venv/Scripts/activate
python -m pip install -r requirements.txt
```

## Start
> Note: taskData.json will be created in your current directory
```bash
python main.py
```

## Test
```bash
python -m pytest tests
```

## Dependencies
- **pytest** (>=8.0.0) - Unit testing framework for writing and running automated tests
- **prompt-toolkit** (>=3.0.0) - Interactive command-line interface library for building terminal UIs with prompts and completions
- **black** (>=23.0.0) - Code formatter for ensuring consistent code style across the project
