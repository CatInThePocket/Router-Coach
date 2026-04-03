
import os
from datetime import datetime
#from dotenv import load_dotenv



#Creating a written report for the file
def save_markdown_report(prompt, accuracy, stats, category_stats, failures, deltas):
    today = datetime.now().strftime("%B %d, %Y at %H:%M")

    #Header and summary
    lines = [
        f"#  Router Evaluation Report - {today}\n",
        f"## System Prompt\n"
        f"{prompt}\n"
        f"## Overall Performance\n",
        f"- **Accuracy**: `{accuracy:.1f}%`",
        f"- **Passed**: {stats['pass']} | **Failed**: {stats['fail']}\n",
        f"## Category Breakdown",
        f""
        "| Category | Accuracy | Score |",
        "| :--- | :--- | :--- |"
    ]
    

    # table rows
    for cat, data in category_stats.items():
        cat_acc = (data["pass"]/data["total"])*100
        lines.append(f"| {cat} | {cat_acc:.1f}%|{data['pass']}/{data['total']} |")
    
    #Implementing changes in the last report compared to the previous one

    if deltas:
        lines.append("\n## Improvements and Regressions")
        lines.append("")
        lines.append("| Status | Query | Was | Now |")
        lines.append("| :--- | :--- | :--- | :--- |")

        for d in deltas:
            icon = "OK" if d['status'] == "FIXED" else "KO"
            lines.append(f"| {icon} **{d['status']}** | {d['query'][:40]}... | `{d['old']}` | `{d['new']}` |")


    #Failures list
    if failures:
        lines.append("\n## Failures to Review")
        for i, f in enumerate(failures, start=1):
            lines.append(f"### {i}. query: {f['query']}")
            lines.append(f"-**Expected**: `{f['expected']}`")
            lines.append(f"-**Actual**: `{f['actual']}`\n")

    #Save to file
    with open("eval_report.md", "w", encoding ="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n Report saved to: {os.path.abspath('outputs/reports/eval_report.md')}")
