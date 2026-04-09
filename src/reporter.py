
import datetime
from pathlib import Path
from src.config_utils import load_config

def generate_pro_report(initial_data, final_data, history, config):
    """
    Generates a two-section report:
    1. Executive Summary (Metrics, Categories, Prompts, Final Failures)
    2. Detailed Technical Logs (Round-by-round terminal style output)
    """
    report_dir = Path(config['paths']['reports_dir'])
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"Optimization_Report_{timestamp}.md"

    content = []
    
    # --- SECTION 1: EXECUTIVE SUMMARY ---
    content.append(f"# 🚀 Prompt Optimization Executive Summary")
    content.append(f"**Date:** {datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')}")
    content.append(f"**Coach Model:** {config['coach']['model']}")
    content.append(f"**Total Rounds:** {len(history) - 1}\n")

    # Accuracy Overview
    content.append("## 📊 Performance Overview")
    delta = final_data['accuracy'] - initial_data['accuracy']
    content.append(f"| Metric | Initial | Final | Delta |")
    content.append(f"| :--- | :--- | :--- | :--- |")
    content.append(f"| **Accuracy** | {initial_data['accuracy']:.2f}% | {final_data['accuracy']:.2f}% | **+{delta:.2f}%** |")
    content.append("\n")

    # Category Table
    content.append("## 🗂️ Category Breakdown")
    content.append("| Category | Initial Acc | Final Acc | Improvement |")
    content.append("| :--- | :--- | :--- | :--- |")
    for cat in initial_data['category_stats']:
        i_acc = (initial_data['category_stats'][cat]['pass'] / initial_data['category_stats'][cat]['total']) * 100
        f_acc = (final_data['category_stats'][cat]['pass'] / final_data['category_stats'][cat]['total']) * 100
        status = "📈" if f_acc > i_acc else ("✅" if f_acc == 100 else "➖")
        content.append(f"| {cat} | {i_acc:.1f}% | {f_acc:.1f}% | {status} |")
    content.append("\n")

    # Prompts
    content.append("## 📝 Prompt Evolution")
    content.append("### Starting Prompt")
    content.append(f"```text\n{initial_data['prompt']}\n```")
    content.append("### Final Optimized Prompt")
    content.append(f"```text\n{final_data['prompt']}\n```\n")

    # Remaining Failures
    content.append("## ❌ Remaining Failures")
    if not final_data['failures']:
        content.append("Perfect score! No remaining failures.")
    for i, f in enumerate(final_data['failures'], 1):
        content.append(f"{i}. **Query:** `{f['query']}`")
        content.append(f"   - Expected: `{f['expected']}` | Actual: `{f['actual']}`")
    
    # --- PAGE BREAK FOR DETAILED LOGS ---
    content.append("\n---\n")
    content.append("# 🔄 Detailed Round-by-Round Logs")
    content.append("> This section contains the full terminal-style logs for every optimization attempt.\n")

    for record in history:
        content.append(f"## 📍 Round {record['iteration']}")
        content.append(f"**Accuracy:** {record['accuracy']:.2f}%")
        
        content.append("### Full Evaluation Log")
        content.append("| # | Result | Query | Expected | Actual |")
        content.append("| :--- | :--- | :--- | :--- | :--- |")
        for i, res in enumerate(record['full_results'], 1):
            icon = "✅" if res['is_correct'] else "❌"
            content.append(f"| {i} | {icon} | {res['query'][:60]}... | {res['expected']} | {res['actual']} |")
        content.append("\n")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    
    print(f"📄 Professional Report generated: {report_file.absolute()}")
