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
    import datetime
    from pathlib import Path
    
    cfg = load_config()
    best_prompt = initial_prompt
    patience = 0
    history_log = []
    # --- NEW: Master Log Buffer ---
    master_log_buffer = []

    # 1. Baseline
    print("📊 Establishing baseline performance...")
    # Catching 7 variables now (including eval_logs)
    best_accuracy, stats, category_stats, failures, full_results, bias_metrics, eval_logs = run_evaluation(best_prompt, eval_dataset, verbose)
    
    # Store baseline logs
    master_log_buffer.append(f"--- BASELINE EVALUATION ---")
    master_log_buffer.extend(eval_logs)
    
    save_snapshot(best_accuracy, stats, category_stats, failures, full_results, best_prompt)

    initial_data = {
        "prompt": initial_prompt,
        "accuracy": best_accuracy,
        "category_stats": category_stats.copy(),
        "failures": failures.copy(),
        "bias": bias_metrics
    }
    
    history_log.append({
        "iteration": 0,
        "prompt": initial_prompt,
        "accuracy": best_accuracy,
        "bias": bias_metrics,
        "full_results": full_results
    })

    current_bias = bias_metrics 

    for i in range(max_iterations):
        print(f"\n🚀 --- Optimization Round {i+1} ---")

        new_prompt = call_coach_llm(best_prompt, failures, coach_model, temperature, timeout, current_bias)
        
        if not new_prompt:
            print("❌ Coach failure, skipping round.")
            master_log_buffer.append(f"Round {i+1}: Coach Failure")
            continue

        # 2. Evaluate (Catching 7 variables)
        new_accuracy, new_stats, new_category_stats, new_failures, new_full_report, new_bias, eval_logs = run_evaluation(new_prompt, eval_dataset, verbose)

        # Store logs for this round
        master_log_buffer.append(f"\n--- OPTIMIZATION ROUND {i+1} ---")
        master_log_buffer.append(f"Prompt used: {new_prompt[:100]}...") # Log a snippet of the prompt
        master_log_buffer.extend(eval_logs)

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
            best_accuracy, best_prompt, failures, current_bias, category_stats = new_accuracy, new_prompt, new_failures, new_bias, new_category_stats
            patience = 0 
            save_snapshot(new_accuracy, new_stats, new_category_stats, new_failures, new_full_report, new_prompt)
        else:
            patience += 1
            print(f"📉 No improvement ({new_accuracy:.2f}%). Patience: {patience}/{patience_limit}")
            if patience >= patience_limit:
                print("🏁 Reached local maximum. Stopping.")
                master_log_buffer.append("Patience limit reached. Stopping.")
                break
    
    # 4. FINAL ATOMIC LOG DUMP
    log_dir = Path(cfg['paths']['snapshot_dir']).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "session.log"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(master_log_buffer))
    
    print(f"📝 Atomic Log Dump completed: {log_file.absolute()}")

    # 5. Final Reporting
    final_data = {
        "prompt": best_prompt,
        "accuracy": best_accuracy,
        "category_stats": category_stats,
        "failures": failures,
        "bias": current_bias
    }
    
    generate_pro_report(initial_data, final_data, history_log, cfg)
                
    return best_prompt
