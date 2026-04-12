# 🚀 LLM Router Optimizer
**Autonomous Prompt Engineering through Iterative QA Testing**

## 📖 Project Vision
This system was designed to optimize a **Router Model** that serves as the "brain" of a larger AI ecosystem. The router decides whether a query requires internet search or can be answered using internal knowledge. If search is required, it generates an optimized search phrase for a search API, the results of which are synthesized by a larger model.

## 🛠️ The Optimization System
To achieve the perfect router prompt, I developed an autonomous training loop that treats **Prompt Engineering as a Software QA process**.

### The Training Loop:
- **Baseline Evaluation**: Runs a balanced dataset through the current Router prompt.
- **The Coach (Gemma 4 e2B)**: A smarter model analyzes failure logs and suggests surgical improvements.
- **Iterative Refinement**: The system only keeps changes that measurably increase accuracy.
- **Patience Logic**: The process only stops after failing to improve the "all-time best" score for 3 consecutive rounds.

## 🧪 QA-First Methodology
Drawing from my **Software Quality Assurance (QA) background**, this project prioritizes **validation and traceability**:

### 1. The Bias Metric
Rather than just a "pass/fail" percentage, I developed a custom **Directional Bias Metric** to understand the "personality" of the model's errors:
- **Type 1 (Lazy)**: The model fails to search when it should (False Internal).
- **Type 2 (Paranoid)**: The model searches for general knowledge it already has (False Search).

**Formula:** 

$$Bias \% = \left( \frac{\max(\text{Type 1}, \text{Type 2})}{\text{Total Failures}} - 0.5 \right) \times 2 \times 100$$

> *A 0% bias indicates a perfectly balanced model, while 100% indicates a model that only makes one type of error.*

### 2. Comprehensive Reporting
Every session generates a detailed **Markdown Report** featuring:
- **Executive Summary**: High-level delta in accuracy and bias.
- **Category Breakdown**: Performance across different query types (Weather, News, etc.).
- **Evolution Logs**: A round-by-round history of every prompt version used.

## 📂 Project Structure
- `src/`: Core logic (Router evaluation, Coaching, and History).
- `data/`: Evaluation datasets and sampled test sets.
- `prompts/`: Version-controlled system prompts for the Router and Coach.
- `outputs/`: JSON snapshots, session logs, and final Markdown reports.

## 🔍 Traceability & Reproducibility
- **Snapshots**: Every evaluation generates a unique JSON snapshot.
- **Session Logs**: Detailed runtime logs are captured in `outputs/logs/session.log`.
- **Version Control**: Prompts are stored as discrete text files for easy A/B testing.
