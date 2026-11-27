import json
from pathlib import Path
from core.mind import IntelligentMind

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "config" / "parameters.json"

def load_parameters():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def main():
    mind = IntelligentMind(load_parameters())
    print("=" * 40)
    print("INTELLIGENT MIND IM-01")
    print("=" * 40)
    while True:
        user_input = input("\nEnter evidence strength (0-1) or type exit: ").strip()
        if user_input.lower() == "exit":
            print("System shutting down.")
            break
        try:
            x = float(user_input)
            result = mind.evaluate(x)
            print("\n--- RESULT ---")
            print("Input:", result["input"])
            print("Raw score:", round(result["raw_score"], 4))
            print("Score:", round(result["score"], 4))
            print("Decision:", result["decision"])
        except (ValueError, TypeError) as error:
            print("Invalid input:", error)

if __name__ == "__main__":
    main()
