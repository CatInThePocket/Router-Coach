import os
import json
import requests
import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Keeping your library imports
from src.routertest import run_evaluation
from src.history import save_snapshot

# Constants
OLLAMA_URL = "http://localhost:11434/api/chat"

def call_coach_llm(current_prompt, failures, model, temperature, timeout):
    today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    # 1. Professional Pathing (src/ -> prompts/)
    base_path = Path(__file__).parent.parent / 'prompts'
    prompt_path = base_path / "coach_prompt.txt"

    try:
        with open(prompt_path, "r", encoding="UTF-8") as f:
            coach_prompt = f.read()
            
        failure_str = json.dumps(failures, indent=2)
        full_message = coach_prompt.format(
            current_prompt=current_prompt,
            failure_log=failure_str,
            today=today_date,
            cutoff="March 2023"
        )

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": full_message}],
            "options": {"temperature": temperature},
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout = timeout)
        response.raise_for_status()
        
        new_prompt = response.json()['message']['content'].strip()

        # 2. Markdown Cleanup
        if new_prompt.startswith("```"):
            lines = new_prompt.splitlines()
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            new_prompt = "\n".join(lines).strip()
        
        return new_prompt

    except Exception as e:
        print(f"⚠️ Coach Error: {e}")
        return None

def auto_optimize(initial_prompt, eval_dataset, max_iterations, coach_model, temperature, timeout, patience_limit,verbose):
    best_prompt = initial_prompt
    patience = 0

    # 1. Baseline using YOUR variable names
    print("📊 Establishing baseline performance...")
    best_accuracy, stats, category_stats, failures, full_results = run_evaluation(best_prompt, eval_dataset,verbose)
    save_snapshot(best_accuracy, stats, category_stats, failures, full_results, best_prompt)

    # Configuration
    model = coach_model
    temperature = temperature

    for i in range(max_iterations):
        print(f"\n🚀 --- Optimization Round {i+1} ---")

        new_prompt = call_coach_llm(best_prompt, failures, model, temperature, timeout)
        
        if not new_prompt:
            print("❌ Coach failure, skipping round.")
            continue

        # 2. Evaluate with YOUR names
        new_accuracy, new_stats, new_category_stats, new_failures, new_full_report = run_evaluation(new_prompt, eval_dataset,verbose)

        # 3. Comparison
        if new_accuracy > best_accuracy:
            print(f"📈 Improvement! {best_accuracy:.2f}% -> {new_accuracy:.2f}%")
            best_accuracy = new_accuracy
            best_prompt = new_prompt
            failures = new_failures # Update failure log for the next round
            patience = 0 
            save_snapshot(new_accuracy, new_stats, new_category_stats, new_failures, new_full_report, new_prompt)
        else:
            print(f"📉 No improvement ({new_accuracy:.2f}%). Patience: {patience + 1}/3")
            patience += 1
            if patience >= patience_limit:
                print("🏁 Reached local maximum. Stopping.")
                break
                
    return best_prompt
