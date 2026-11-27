import json
from pathlib import Path
from math_engine.linear import calculate_score

ROOT = Path(__file__).resolve().parent.parent

class IntelligentMind:
    def __init__(self, parameters):
        self.parameters = parameters
        self.memory_file = ROOT / "memory" / "memory.json"

    def evaluate(self, x):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("Input must be numeric.")
        if not 0 <= x <= 1:
            raise ValueError("Input must be between 0 and 1.")

        model = self.parameters["model"]
        result = calculate_score(x, model["weight"], model["bias"])
        score = result["output"]
        decision = "ACCEPT" if score >= model["threshold"] else "REJECT"

        record = {
            "input": x,
            "raw_score": result["raw_score"],
            "score": score,
            "decision": decision
        }
        self.save_memory(record)
        return record

    def save_memory(self, record):
        memory_config = self.parameters["memory"]
        if not memory_config.get("enabled", True):
            return

        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        if self.memory_file.exists():
            try:
                records = json.loads(self.memory_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                records = []
        else:
            records = []

        records.append(record)
        limit = max(0, int(memory_config.get("max_records", 1000)))
        records = records[-limit:] if limit else []
        self.memory_file.write_text(
            json.dumps(records, indent=2), encoding="utf-8"
        )
