import os
import json
import requests
import datetime
from pathlib import Path
from typing import List, Dict, Optional
import traceback

# Keeping your library imports
from src.routertest import run_evaluation
from src.history import save_snapshot

# Constants
OLLAMA_URL = "http://localhost:11434/api/chat"

def call_coach_llm(current_prompt, failures, model, temperature, timeout, bias_metrics):
    today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    # Create the bias summary string to be injected into the prompt
    # This explains the 40% bias logic to the LLM
    bias_summary = (
        f"Bias Analysis: {bias_metrics['percentage']}% towards {bias_metrics['direction']}\n"
        f"Breakdown: {bias_metrics['type_1']} Type 1 errors (False Internals) | "
        f"{bias_metrics['type_2']} Type 2 errors (False Searches)"
    )

    # 1. Professional Pathing
    base_path = Path(__file__).parent.parent / 'prompts'
    prompt_path = base_path / "coach_prompt.txt"

    try:
        with open(prompt_path, "r", encoding="UTF-8") as f:
            coach_prompt = f.read()
            
        failure_str = json.dumps(failures, indent=2)
        
        # Added 'bias_info' to the format call
        full_message = coach_prompt.format(
            current_prompt=current_prompt,
            failure_log=failure_str,
            bias_info=bias_summary,  # Ensure your coach_prompt.txt has a {bias_info} placeholder
            today=today_date,
            cutoff="March 2023"
        )

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": full_message}],
            "options": {"temperature": temperature,
                        "num_ctx": 4096  # Limits the memory window to keep it fast
                        },
            "keep_alive": 0,  # Added to ensure memory clears between coaching rounds
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
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
        print("\n❌ CRITICAL COACH ERROR:")
        traceback.print_exc() # This will show the exact line and file
        return None


def auto_optimize(initial_prompt, eval_dataset, max_iterations, coach_model, temperature, timeout, patience_limit, verbose):
    from src.config_utils import load_config
    from src.reporter import generate_pro_report
    
    cfg = load_config()
    best_prompt = initial_prompt
    patience = 0
    history_log = []

    # 1. Baseline
    print("📊 Establishing baseline performance...")
    # Catching 6 variables now
    best_accuracy, stats, category_stats, failures, full_results, bias_metrics = run_evaluation(best_prompt, eval_dataset, verbose)
    save_snapshot(best_accuracy, stats, category_stats, failures, full_results, best_prompt)

    # Capture initial state for report summary (including bias)
    initial_data = {
        "prompt": initial_prompt,
        "accuracy": best_accuracy,
        "category_stats": category_stats.copy(),
        "failures": failures.copy(),
        "bias": bias_metrics
    }
    
    # Log baseline to history (including prompt and bias)
    history_log.append({
        "iteration": 0,
        "prompt": initial_prompt,
        "accuracy": best_accuracy,
        "bias": bias_metrics,
        "full_results": full_results
    })

    current_bias = bias_metrics # Keep track for the coach call

    for i in range(max_iterations):
        print(f"\n🚀 --- Optimization Round {i+1} ---")

        # Added current_bias to the coach call
        new_prompt = call_coach_llm(best_prompt, failures, coach_model, temperature, timeout, current_bias)
        
        if not new_prompt:
            print("❌ Coach failure, skipping round.")
            continue

        # 2. Evaluate (Catching 6 variables)
        new_accuracy, new_stats, new_category_stats, new_failures, new_full_report, new_bias = run_evaluation(new_prompt, eval_dataset, verbose)

        # Log every round to history for the detailed section
        history_log.append({
            "iteration": i + 1,
            "prompt": new_prompt,
            "accuracy": new_accuracy,
            "bias": new_bias,
            "full_results": new_full_report
        })

        # 3. Comparison
        if new_accuracy > best_accuracy:
            print(f"📈 Improvement! {best_accuracy:.2f}% -> {new_accuracy:.2f}%")
            best_accuracy = new_accuracy
            best_prompt = new_prompt
            failures = new_failures 
            current_bias = new_bias # Update bias for the next coach round
            category_stats = new_category_stats 
            patience = 0 # Reset patience because we improved
            save_snapshot(new_accuracy, new_stats, new_category_stats, new_failures, new_full_report, new_prompt)
        else:
            patience += 1
            print(f"📉 No improvement ({new_accuracy:.2f}%). Patience: {patience}/{patience_limit}")
            # If no improvement, we keep the previous best_prompt and failures for the next try
            if patience >= patience_limit:
                print("🏁 Reached local maximum. Stopping.")
                break
    
    # 4. Final Reporting
    final_data = {
        "prompt": best_prompt,
        "accuracy": best_accuracy,
        "category_stats": category_stats,
        "failures": failures,
        "bias": current_bias
    }
    
    generate_pro_report(initial_data, final_data, history_log, cfg)
                
    return best_prompt
