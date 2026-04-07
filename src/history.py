import json
import os
import datetime
from pathlib import Path
from typing import Dict, List, Any
from src.config_utils import load_config
    

def save_snapshot(
    accuracy: float, 
    stats: Dict[str, int], 
    category_stats: Dict[str, Any], 
    failures: List[Dict[str, Any]], 
    full_results: List[Dict[str, Any]], 
    prompt: str
) -> str:
    """
    Saves a comprehensive JSON snapshot of a router evaluation run.
    
    Returns:
        str: The absolute path to the saved snapshot file.
    """
   
    cfg = load_config()
    #  # 1. Get path from YAML and force it to be relative to the project root
    root_dir = Path(__file__).parent.parent
    history_dir = root_dir / cfg['paths']['snapshot_dir']
    
    history_dir.mkdir(parents=True, exist_ok=True)

    # 2. Generate unique filename with high-resolution timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = history_dir / f"run_{timestamp}.json"

    # 3. Structure the snapshot payload
    snapshot_data = {
        "metadata": {
            "timestamp": timestamp,
            "version": "1.0"
        },
        "prompt": prompt,
        "metrics": {
            "accuracy_percent": round(accuracy, 2),
            "total_pass": stats.get("pass", 0),
            "total_fail": stats.get("fail", 0)
        },
        "category_breakdown": category_stats,
        "failures": failures,
        "full_results": full_results
    }

    # 4. Atomic Write to disk
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(snapshot_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Success: Snapshot persisted to {filename.name}")
    except IOError as e:
        print(f"❌ Critical Error: Could not write snapshot to disk: {e}")
        raise

    return str(filename)
