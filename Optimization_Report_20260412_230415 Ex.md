# 🚀 Prompt Optimization Executive Summary
**Date:** Sunday, April 12, 2026 23:04:15
**Coach Model:** gemma4:e2b
**Total Rounds:** 4

---

## 📊 Performance Overview

| Metric | Initial | Final | Delta |
| :--- | :--- | :--- | :--- |
| Accuracy | 83.33% | 91.67% | **+8.33%** |


## ⚖️ Bias Analysis

> Bias % represents the deviation from a 50/50 error distribution.

| Metric | Type 1 (Lazy) | Type 2 (Paranoid) | Bias % | Direction |
| :--- | :--- | :--- | :--- | :--- |
| Initial | 2 | 0 | 100.0% | Type 1 (Should Search but didn't) |
| Final | 1 | 0 | 100.0% | Type 1 (Should Search but didn't) |


## 🗂️ Category Breakdown

| Category | Initial Acc | Final Acc | Status |
| :--- | :--- | :--- | :--- |
| Product & Price Comparison | 100.0% | 100.0% | ✅ |
| Static World Knowledge | 100.0% | 100.0% | ✅ |
| Real-Time Data Streams | 100.0% | 100.0% | ✅ |
| Local & Geo-Specific | 0.0% | 0.0% | ➖ |
| Mathematics & Logic | 100.0% | 100.0% | ✅ |
| Breaking News & Current Events | 0.0% | 100.0% | 📈 |
| Language & Translation | 100.0% | 100.0% | ✅ |
| Roleplay & Persona | 100.0% | 100.0% | ✅ |
| Technical & Coding | 100.0% | 100.0% | ✅ |
| Summarization & Extraction | 100.0% | 100.0% | ✅ |
| Post-Cutoff Knowledge | 100.0% | 100.0% | ✅ |
| Creative Writing & Brainstorming | 100.0% | 100.0% | ✅ |


## 📝 Final Prompt Comparison

### Starting Prompt
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"If the query requires information post-dating March 2023, or involves a live TRIGGER, you must trigger a search."
"For search-required queries, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

### Final Optimized Prompt
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"Additionally, evaluate the query for requests requiring specific, dynamic, or localized factual information (e.g., current business listings, recent political outcomes, specific addresses, or up-to-date rankings)."
"If the query requires information post-dating March 2023, involves a live TRIGGER, or asks for specific, dynamic, or localized factual knowledge, you must trigger a search."
"For search-required queries, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

## ❌ Remaining Failures

1. **Query:** `Are there any halal-certified restaurants in Seoul, Myeongdong?`
   - Expected: `SEARCH` | Actual: `INTERNAL`


---


# 🔄 Detailed Round-by-Round Logs

> Full technical history of prompts and evaluations.

## 📍 Round 0
**Accuracy:** 83.33% | **Bias:** 100.0% (Type 1 (Should Search but didn't))

### Prompt Used
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"If the query requires information post-dating March 2023, or involves a live TRIGGER, you must trigger a search."
"For search-required queries, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

### Evaluation Detail

| # | Result | Query | Expected | Actual |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ✅ | Compare the monthly cost of YouTube TV vs Hulu + Live TV for... | SEARCH | SEARCH |
| 2 | ✅ | Who is the author of 'The Great Gatsby'?... | INTERNAL | INTERNAL |
| 3 | ✅ | What is the current yield on the US 10-year Treasury note?... | SEARCH | SEARCH |
| 4 | ❌ | Are there any halal-certified restaurants in Seoul, Myeongdo... | SEARCH | INTERNAL |
| 5 | ✅ | If a car travels at 60 mph, how far will it go in 2.5 hours?... | INTERNAL | INTERNAL |
| 6 | ❌ | Who is the new favorite to succeed Ali Khamenei as Supreme L... | SEARCH | INTERNAL |
| 7 | ✅ | How do you write 'Happy Birthday' in Traditional Chinese?... | INTERNAL | INTERNAL |
| 8 | ✅ | Roleplay as a weary traveler who just arrived at a fantasy t... | INTERNAL | INTERNAL |
| 9 | ✅ | How do I center a div using Flexbox?... | INTERNAL | INTERNAL |
| 10 | ✅ | Extract all email addresses from this text block: [Text]... | INTERNAL | INTERNAL |
| 11 | ✅ | What was the final inflation rate in the US for the year 202... | SEARCH | SEARCH |
| 12 | ✅ | Create a tagline for a luxury brand of fountain pens.... | INTERNAL | INTERNAL |


## 📍 Round 1
**Accuracy:** 91.67% | **Bias:** 100.0% (Type 1 (Should Search but didn't))

### Prompt Used
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"Additionally, evaluate the query for requests requiring specific, dynamic, or localized factual information (e.g., current business listings, recent political outcomes, specific addresses, or up-to-date rankings)."
"If the query requires information post-dating March 2023, involves a live TRIGGER, or asks for specific, dynamic, or localized factual knowledge, you must trigger a search."
"For search-required queries, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

### Evaluation Detail

| # | Result | Query | Expected | Actual |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ✅ | Compare the monthly cost of YouTube TV vs Hulu + Live TV for... | SEARCH | SEARCH |
| 2 | ✅ | Who is the author of 'The Great Gatsby'?... | INTERNAL | INTERNAL |
| 3 | ✅ | What is the current yield on the US 10-year Treasury note?... | SEARCH | SEARCH |
| 4 | ❌ | Are there any halal-certified restaurants in Seoul, Myeongdo... | SEARCH | INTERNAL |
| 5 | ✅ | If a car travels at 60 mph, how far will it go in 2.5 hours?... | INTERNAL | INTERNAL |
| 6 | ✅ | Who is the new favorite to succeed Ali Khamenei as Supreme L... | SEARCH | SEARCH |
| 7 | ✅ | How do you write 'Happy Birthday' in Traditional Chinese?... | INTERNAL | INTERNAL |
| 8 | ✅ | Roleplay as a weary traveler who just arrived at a fantasy t... | INTERNAL | INTERNAL |
| 9 | ✅ | How do I center a div using Flexbox?... | INTERNAL | INTERNAL |
| 10 | ✅ | Extract all email addresses from this text block: [Text]... | INTERNAL | INTERNAL |
| 11 | ✅ | What was the final inflation rate in the US for the year 202... | SEARCH | SEARCH |
| 12 | ✅ | Create a tagline for a luxury brand of fountain pens.... | INTERNAL | INTERNAL |


## 📍 Round 2
**Accuracy:** 91.67% | **Bias:** 100.0% (Type 1 (Should Search but didn't))

### Prompt Used
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"Additionally, evaluate the query for requests requiring specific, dynamic, or localized factual information (e.g., current business listings, recent political outcomes, specific addresses, up-to-date rankings, or current geo-specific details)."
"If the query requires information post-dating March 2023, involves a live TRIGGER, or asks for specific, dynamic, or localized factual knowledge, you must trigger a search."
"For search-required queries, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

### Evaluation Detail

| # | Result | Query | Expected | Actual |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ✅ | Compare the monthly cost of YouTube TV vs Hulu + Live TV for... | SEARCH | SEARCH |
| 2 | ✅ | Who is the author of 'The Great Gatsby'?... | INTERNAL | INTERNAL |
| 3 | ✅ | What is the current yield on the US 10-year Treasury note?... | SEARCH | SEARCH |
| 4 | ❌ | Are there any halal-certified restaurants in Seoul, Myeongdo... | SEARCH | INTERNAL |
| 5 | ✅ | If a car travels at 60 mph, how far will it go in 2.5 hours?... | INTERNAL | INTERNAL |
| 6 | ✅ | Who is the new favorite to succeed Ali Khamenei as Supreme L... | SEARCH | SEARCH |
| 7 | ✅ | How do you write 'Happy Birthday' in Traditional Chinese?... | INTERNAL | INTERNAL |
| 8 | ✅ | Roleplay as a weary traveler who just arrived at a fantasy t... | INTERNAL | INTERNAL |
| 9 | ✅ | How do I center a div using Flexbox?... | INTERNAL | INTERNAL |
| 10 | ✅ | Extract all email addresses from this text block: [Text]... | INTERNAL | INTERNAL |
| 11 | ✅ | What was the final inflation rate in the US for the year 202... | SEARCH | SEARCH |
| 12 | ✅ | Create a tagline for a luxury brand of fountain pens.... | INTERNAL | INTERNAL |


## 📍 Round 3
**Accuracy:** 75.00% | **Bias:** 100.0% (Type 2 (Shouldn't Search but did))

### Prompt Used
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"Additionally, evaluate the query for requests requiring specific, dynamic, or localized factual information (e.g., current business listings, specific addresses, up-to-date rankings, or localized data)."
"Decision Rule: You must trigger a search if the query meets ANY of the following conditions:
1. It requires information post-dating March 2023.
2. It involves a live TRIGGER (weather, financial markets, live news, etc.).
3. It asks for specific, dynamic, or localized factual knowledge (e.g., current business listings, specific addresses, or up-to-date rankings).
"For search-required queries, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

### Evaluation Detail

| # | Result | Query | Expected | Actual |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ✅ | Compare the monthly cost of YouTube TV vs Hulu + Live TV for... | SEARCH | SEARCH |
| 2 | ✅ | Who is the author of 'The Great Gatsby'?... | INTERNAL | INTERNAL |
| 3 | ✅ | What is the current yield on the US 10-year Treasury note?... | SEARCH | SEARCH |
| 4 | ✅ | Are there any halal-certified restaurants in Seoul, Myeongdo... | SEARCH | SEARCH |
| 5 | ✅ | If a car travels at 60 mph, how far will it go in 2.5 hours?... | INTERNAL | INTERNAL |
| 6 | ✅ | Who is the new favorite to succeed Ali Khamenei as Supreme L... | SEARCH | SEARCH |
| 7 | ❌ | How do you write 'Happy Birthday' in Traditional Chinese?... | INTERNAL | SEARCH |
| 8 | ✅ | Roleplay as a weary traveler who just arrived at a fantasy t... | INTERNAL | INTERNAL |
| 9 | ❌ | How do I center a div using Flexbox?... | INTERNAL | SEARCH |
| 10 | ✅ | Extract all email addresses from this text block: [Text]... | INTERNAL | INTERNAL |
| 11 | ✅ | What was the final inflation rate in the US for the year 202... | SEARCH | SEARCH |
| 12 | ❌ | Create a tagline for a luxury brand of fountain pens.... | INTERNAL | SEARCH |


## 📍 Round 4
**Accuracy:** 83.33% | **Bias:** 100.0% (Type 2 (Shouldn't Search but did))

### Prompt Used
```text
"You are a specialized router tasked with determining if a query requires real-time internet data."
"Your internal knowledge cutoff is March 2023 and today's date is Sunday, April 12, 2026."
"Evaluate the query for time-sensitive TRIGGERS: weather, financial markets, live news, 2026 events, sports results, or scheduled concerts."
"Additionally, evaluate the query for requests requiring specific, dynamic, or localized factual information (e.g., current business listings, specific addresses, up-to-date rankings, or localized business details)."
"Decision Logic: If the query requires information post-dating March 2023, involves a live TRIGGER, OR asks for specific, dynamic, or localized factual knowledge, you MUST trigger a search."
"If the query requires a search, output ONLY the string 'SEARCH: ' followed by a concise, keyword-optimized search query."
"Example: If asked about the current Pope, output: SEARCH: current Pope 2026."
"If the query is a general fact, creative task, or logic puzzle that can be solved with static knowledge, answer the user directly from memory."
"Do not provide any preamble, explanations, or conversational filler."
"Strictly adhere to the cutoff date to decide between memory and search."
```

### Evaluation Detail

| # | Result | Query | Expected | Actual |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ✅ | Compare the monthly cost of YouTube TV vs Hulu + Live TV for... | SEARCH | SEARCH |
| 2 | ✅ | Who is the author of 'The Great Gatsby'?... | INTERNAL | INTERNAL |
| 3 | ✅ | What is the current yield on the US 10-year Treasury note?... | SEARCH | SEARCH |
| 4 | ✅ | Are there any halal-certified restaurants in Seoul, Myeongdo... | SEARCH | SEARCH |
| 5 | ✅ | If a car travels at 60 mph, how far will it go in 2.5 hours?... | INTERNAL | INTERNAL |
| 6 | ✅ | Who is the new favorite to succeed Ali Khamenei as Supreme L... | SEARCH | SEARCH |
| 7 | ❌ | How do you write 'Happy Birthday' in Traditional Chinese?... | INTERNAL | SEARCH |
| 8 | ✅ | Roleplay as a weary traveler who just arrived at a fantasy t... | INTERNAL | INTERNAL |
| 9 | ❌ | How do I center a div using Flexbox?... | INTERNAL | SEARCH |
| 10 | ✅ | Extract all email addresses from this text block: [Text]... | INTERNAL | INTERNAL |
| 11 | ✅ | What was the final inflation rate in the US for the year 202... | SEARCH | SEARCH |
| 12 | ✅ | Create a tagline for a luxury brand of fountain pens.... | INTERNAL | INTERNAL |

