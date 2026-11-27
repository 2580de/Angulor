# Intelligent Mind (IM-01)

A modular mathematical intelligence prototype built from first principles.

## Components
- Linear model: z = wx + b
- Sigmoid transformation
- Threshold decision
- Persistent JSON memory
- Parameter configuration
- Unit tests

## Requirements
Python 3.9+

## Run
From this folder:
```bash
python main.py
```

## Test
```bash
python -m tests.test_math
```

Input is a numerical evidence-strength value from 0 to 1. The sigmoid output is a score, not a calibrated real-world probability.
