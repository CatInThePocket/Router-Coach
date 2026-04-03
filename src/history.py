import json
import os
import datetime

def save_snapshot(accuracy, stats, category_stats, failures, full_results, prompt):
    #1. Create the history folder if it doesn't exist
    os.makedirs("outputs/history",exist_ok=True)

    #2. Create a unique filename using the current data and time
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/history/run_{timestamp}.json"

    #3. Bundle everything into one "Envelope"
    snapshot_data = {
        "timestamp": timestamp,
        "prompt": prompt,
        "metrics": {
            "accuracy": accuracy,
            "pass": stats["pass"],
            "fail": stats["fail"]
            },
        "categories": category_stats,
        "failures": failures,
        "full_results": full_results #This is the momery for comparisons
    }

    #4.Write to a disk
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(snapshot_data, f, indent=4)

    print(f" Snapshot saved to history: {filename}")
    