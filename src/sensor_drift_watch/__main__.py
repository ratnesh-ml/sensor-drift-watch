import json
from .monitor import summarize

if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
