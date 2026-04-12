
import datetime
from pathlib import Path
from src.config_utils import load_config

import datetime
from pathlib import Path

def generate_pro_report(initial_data, final_data, history, config):
    report_dir = Path(config['paths']['reports_dir'])
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"Optimization_Report_{timestamp}.md"

    content = []
    
    # --- SECTION 1: EXECUTIVE SUMMARY ---
    content.append(f"# 🚀 Prompt Optimization Executive Summary")
    content.append(f"**Date:** {datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')}")
    content.append(f"**Coach Model:** {config['coach']['model']}")
    content.append(f"**Total Rounds:** {len(history) - 1}")
    content.append("\n---\n") # Horizontal rule

    # Accuracy Overview
    content.append("## 📊 Performance Overview\n") # Added newline
    delta = final_data['accuracy'] - initial_data['accuracy']
    content.append("| Metric | Initial | Final | Delta |")
    content.append("| :--- | :--- | :--- | :--- |")
    content.append(f"| Accuracy | {initial_data['accuracy']:.2f}% | {final_data['accuracy']:.2f}% | **+{delta:.2f}%** |")
    content.append("\n")

    # BIAS INDICATOR TABLE
    content.append("## ⚖️ Bias Analysis\n")
    # CRITICAL: Ensure there is a blank line after the blockquote
    content.append("> Bias % represents the deviation from a 50/50 error distribution.\n") 
    
    # Standard Markdown table syntax
    content.append("| Metric | Type 1 (Lazy) | Type 2 (Paranoid) | Bias % | Direction |")
    content.append("| :--- | :--- | :--- | :--- | :--- |")
    
    i_bias = initial_data['bias']
    f_bias = final_data['bias']
    
    # Ensure strings are clean
    content.append(f"| Initial | {i_bias['type_1']} | {i_bias['type_2']} | {i_bias['percentage']}% | {i_bias['direction']} |")
    content.append(f"| Final | {f_bias['type_1']} | {f_bias['type_2']} | {f_bias['percentage']}% | {f_bias['direction']} |")
    content.append("\n") # Mandatory blank line after

    # Category Table
    content.append("## 🗂️ Category Breakdown\n")
    content.append("| Category | Initial Acc | Final Acc | Status |")
    content.append("| :--- | :--- | :--- | :--- |")
    for cat in initial_data['category_stats']:
        i_acc = (initial_data['category_stats'][cat]['pass'] / initial_data['category_stats'][cat]['total']) * 100
        f_acc = (final_data['category_stats'][cat]['pass'] / final_data['category_stats'][cat]['total']) * 100
        status = "📈" if f_acc > i_acc else ("✅" if f_acc == 100 else "➖")
        content.append(f"| {cat} | {i_acc:.1f}% | {f_acc:.1f}% | {status} |")
    content.append("\n")

    # Prompts comparison
    content.append("## 📝 Final Prompt Comparison\n")
    content.append("### Starting Prompt")
    content.append(f"```text\n{initial_data['prompt']}\n```\n") # Newline after code block
    content.append("### Final Optimized Prompt")
    content.append(f"```text\n{final_data['prompt']}\n```\n")

    # Remaining Failures
    content.append("## ❌ Remaining Failures\n")
    if not final_data['failures']:
        content.append("Perfect score! No remaining failures.")
    else:
        for i, f in enumerate(final_data['failures'], 1):
            content.append(f"{i}. **Query:** `{f['query']}`")
            content.append(f"   - Expected: `{f['expected']}` | Actual: `{f['actual']}`")
    
    # --- SECTION 2: DETAILED LOGS ---
    content.append("\n\n---\n\n")
    content.append("# 🔄 Detailed Round-by-Round Logs\n")
    content.append("> Full technical history of prompts and evaluations.\n")

    for record in history:
        content.append(f"## 📍 Round {record['iteration']}")
        content.append(f"**Accuracy:** {record['accuracy']:.2f}% | **Bias:** {record['bias']['percentage']}% ({record['bias']['direction']})\n")
        
        content.append("### Prompt Used")
        content.append(f"```text\n{record['prompt']}\n```\n")
        
        content.append("### Evaluation Detail\n")
        content.append("| # | Result | Query | Expected | Actual |")
        content.append("| :--- | :--- | :--- | :--- | :--- |")
        for i, res in enumerate(record['full_results'], 1):
            icon = "✅" if res['is_correct'] else "❌"
            content.append(f"| {i} | {icon} | {res['query'][:60]}... | {res['expected']} | {res['actual']} |")
        content.append("\n")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
    print(f"📄 Professional Report generated: {report_file.absolute()}")
