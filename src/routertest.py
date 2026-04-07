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
    category_stats = {}
    failures = []
    full_results = []

    if verbose:
        print(f"\n🚀 STARTING EVALUATION | Dataset: {len(eval_dataset)} items", flush=True)

    for item in eval_dataset:
        prediction = routertest(item['query'], prompt)
        
        is_correct = ((prediction == "SEARCH") == item['needs_search'])
        cat = item.get('Category', 'General')
        
        # --- THE "PAINTING" LOGIC ---
        if verbose:
            icon = "✅" if is_correct else "❌"
            print(f" Query: {item['query'][:50]}...")
            print(f" Expected: {'SEARCH' if item['needs_search'] else 'INTERNAL'} | Actual: {prediction} {icon}\n", flush=True)

        if cat not in category_stats:
            category_stats[cat] = {"pass": 0, "total": 0}
        category_stats[cat]["total"] += 1

        if is_correct:
            stats["pass"] += 1
            category_stats[cat]["pass"] += 1
        else:
            stats["fail"] += 1
            failures.append({
                "query": item['query'],
                "category": cat,
                "expected": "SEARCH" if item['needs_search'] else "INTERNAL",
                "actual": prediction
            })
        
        full_results.append({"query": item['query'], "category": cat, "is_correct": is_correct})

    accuracy = (stats["pass"] / len(eval_dataset)) * 100

    if verbose:
        print(f"📊 Accuracy: {accuracy:.2f}% ({stats['pass']}/{len(eval_dataset)})", flush=True)
        print("\n🗂️  CATEGORY BREAKDOWN:", flush=True)
        for c, d in category_stats.items():
            print(f" - {c}: {(d['pass']/d['total'])*100:.1f}%", flush=True)

    return accuracy, stats, category_stats, failures, full_results

# --- END OF FILE ---
