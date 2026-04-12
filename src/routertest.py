import os
import json
import random
import requests
import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional
import sys
import json
import logging


# Constants
CUTOFF_DATE = "March 2023"
OLLAMA_URL = "http://localhost:11434/api/chat"

def get_system_prompt() -> str:
    """Loads the router prompt template and injects dynamic dates."""
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    base_path = Path(__file__).parent.parent / 'prompts'
    prompt_path = base_path / "router_prompt.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(today=today, cutoff=CUTOFF_DATE)

def routertest(user_question: str, prompt: str, model: str = "llama3") -> str:
    """Determines if a query needs SEARCH or INTERNAL knowledge."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_question}
        ],
        "options": {"temperature": 0.0},
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=30)
    content = response.json().get('message', {}).get('content', '').upper()
    return "SEARCH" if "SEARCH:" in content else "INTERNAL"

def load_tests(sample_per_category: Optional[int] = None) -> List[Dict]:
    """Balanced loader for the evaluation dataset."""
    data_path = Path(__file__).parent.parent / 'data'
    file_path = data_path / "dataset.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if sample_per_category is None or sample_per_category == "full":
        return data
    by_cat = defaultdict(list)
    for item in data:
        by_cat[item.get('Category', 'General')].append(item)
    sampled = []
    n = int(sample_per_category)
    for items in by_cat.values():
        count = min(len(items), n)
        sampled.extend(random.sample(items, count))
    return sampled

def run_evaluation(prompt, eval_dataset, verbose):
    stats = {"pass": 0, "fail": 0}
    type_1 = 0 
    type_2 = 0 
    category_stats = {}
    failures = []
    full_results = []
    # --- NEW: Log Buffer ---
    eval_logs = [] 

    header = f"\n🚀 STARTING EVALUATION | Dataset: {len(eval_dataset)} items"
    eval_logs.append(header)
    if verbose:
        print(header, flush=True)

    for item in eval_dataset:
        expected_search = item['needs_search'] 
        prediction = routertest(item['query'], prompt)
        
        actual_search = (str(prediction).strip().upper() == "SEARCH")
        is_correct = (actual_search == expected_search)
        cat = item.get('Category', 'General')
        
        # Construct the log line
        icon = "✅" if is_correct else "❌"
        expected_str = 'SEARCH' if expected_search else 'INTERNAL'
        log_line = f" Query: {item['query'][:50]}... | Expected: {expected_str} | Actual: {prediction} {icon}"
        
        eval_logs.append(log_line) # Buffer it
        if verbose:
            print(f" Query: {item['query'][:50]}...")
            print(f" Expected: {expected_str} | Actual: {prediction} {icon}\n", flush=True)

        if cat not in category_stats:
            category_stats[cat] = {"pass": 0, "total": 0}
        category_stats[cat]["total"] += 1

        if is_correct:
            stats["pass"] += 1
            category_stats[cat]["pass"] += 1
        else:
            stats["fail"] += 1
            if expected_search and not actual_search:
                type_1 += 1
            elif not expected_search and actual_search:
                type_2 += 1

            failures.append({
                "query": item['query'],
                "category": cat,
                "expected": expected_str,
                "actual": prediction
            })
        
        full_results.append({
            "query": item['query'],
            "category": cat,
            "expected": expected_str,
            "actual": prediction,
            "is_correct": is_correct
        })  

    accuracy = (stats["pass"] / len(eval_dataset)) * 100

    total_failures = type_1 + type_2
    bias_percentage = 0.0
    bias_direction = "Neutral"

    if total_failures > 0:
        larger_error = max(type_1, type_2)
        bias_percentage = ((larger_error / total_failures) - 0.5) * 2 * 100
        bias_direction = "Type 1 (Should Search but didn't)" if type_1 > type_2 else "Type 2 (Shouldn't Search but did)"

    bias_metrics = {
        "type_1": type_1, "type_2": type_2,
        "percentage": round(bias_percentage, 1),
        "direction": bias_direction
    }

    summary_line = f"📊 Accuracy: {accuracy:.2f}% | Bias: {bias_percentage}% towards {bias_direction}"
    eval_logs.append(summary_line)
    if verbose:
        print(summary_line, flush=True)

    # RETURN 7 VALUES (Added eval_logs)
    return accuracy, stats, category_stats, failures, full_results, bias_metrics, eval_logs
