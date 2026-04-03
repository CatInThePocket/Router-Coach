import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from reporter import save_markdown_report


#Loading key

load_dotenv()

#Serper key for the search
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

#We get the system prompt

def get_system_prompt():
    #Calculate injected variables
    #We get the date from the system, in order to inject it into the system prompt
    cutoff = "March 2023"
    today = datetime.now().strftime("%A, %B %d, %Y")

    #Load raw text file with the prompt
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts') #os.path twice, up to root and back down to 'prompts'
    prompt_path = os.path.join(base_path, "router_prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    #Inject the variables into the placeholders
    full_prompt = template.format(today = today, cutoff = cutoff)

    return full_prompt
#We create the router function for the model

def routertest(user_question, prompt,model):
    url = "http://localhost:11434/api/chat"
    
    cutoff = "March 2023"
    today = datetime.now().strftime("%A, %B %d, %Y")
    

    system_instructions = (prompt
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_question}
        ],
        "options": {
            "temperature": 0.0 #Forced Consistency
        },
        "stream": False
    }

    response = requests.post(url, json=payload)
    #print(response.json()['message']['content'])
    return "SEARCH" if "SEARCH:" in response.json()['message']['content'] else "INTERNAL"
    
#print(routertest("What is the weather today?", get_system_prompt(), "llama3"))

def load_tests(sample_per_category=None):
    print(f"I am running from: {os.path.abspath(__file__)}")
    print(f"I received the value: {sample_per_category}")
    #Get the file path
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data') #os.path twice, up to root and back down to 'data'
    file_path = os.path.join(base_path, "dataset.json")

    with open(file_path, "r") as f:
        data = json.load(f)

    # --- OLD BEHAVIOR (If no parameter is passed) ---
    if sample_per_category is None or sample_per_category == "full":
        return data
    
    # --- NEW EXTEND LOGIC (If a number is passed) ---
    from collections import defaultdict
    import random
    
    
    
    #Group by category
    by_cat = defaultdict(list)
    for item in data:
        by_cat[item['Category']].append(item)

    

    # Sample N for each
    sampled = []
    for cat, items in by_cat.items():
        count = min(len(items), int(sample_per_category)) #we use min in case one category has less than requested sample
        sampled.extend(random.sample(items, count))

    # Save the sampled version and overwite if aready there
    sampled_path = os.path.join(base_path, "samples/dataset_sampled.json")
    with open(sampled_path, "w", encoding ='utf-8') as f:
        json.dump(sampled, f, indent = 2, ensure_ascii=False)

    return sampled




    
#eval_dataset = load_tests(1)
#prompt = get_system_prompt()

def run_evaluation(prompt, eval_dataset):
    stats = {"pass": 0, "fail": 0}
    category_stats = {} #Storing the categories of the queries
    failures = []
    full_results = []

    print(f"Starting Eval with Prompt:    {prompt[:50]}...")

    for item in eval_dataset:
        #1. Get the router answer
        prediction = routertest(item['query'], prompt, model= "llama3")
        #Standarize
        actual_search = (prediction.upper() == "SEARCH")
        expected_search = item['needs_search']
        is_correct = (actual_search == expected_search)
        status_icon = "\u2705" if is_correct else "\u274C"
        print(f" Query: {item['query'][:50]}...")
        print(f" Expected {'SEARCH' if expected_search else 'INTERNAL'}")
        print(f" Actual: {prediction} {status_icon}\n")
        print(f" Category: {item['Category'][:50]}...")

        cat = item.get('Category', 'General')

        #If we haven't found this category yet, start it at 0.
        if cat not in category_stats:
            category_stats[cat] = {"pass": 0, "total": 0}

        category_stats[cat]["total"] += 1              

        #We compare the results and we increment 1 if pass
        if actual_search == expected_search:
            stats["pass"] += 1
            category_stats[cat]["pass"] += 1

            
        else:
            stats["fail"] += 1
            
            failures.append({
                "query": item['query'],
                "expected": "SEARCH" if expected_search else "INTERNAL",
                "actual": prediction
                })
        #4. Record the full snapshot 
        #Storing this into the full_results
        full_results.append({
            "query": item['query'],
            "category": cat,
            "expected": "SEARCH" if expected_search else "INTERNAL",
            "actual": prediction,
            "is_correct": is_correct
        })
    #Final reporting 
    total = len(eval_dataset)
    accuracy = (stats["pass"]/ total)* 100
    print(f"\n--- EVALUATION COMPLETE ---")
    print(f"Accuracy: {accuracy:2f}% ({stats['pass']}/{total})")
    print(f"\n--- CAEGOR BREAKDOWN ---")
    for cat, data in category_stats.items():
        acc = (data["pass"]/data["total"])*100
        print(f"{cat}: {acc:.1f}% ({data['pass']}/{data['total']})")

    if failures:
        print("\n FAILURES LIST:")
        for i,f in enumerate(failures, 1):
            print(f"{i}, Query: {f['query']}")
            print(f"Should be: {f['expected']} | But AI said: {f['actual']}\n")
    else:
        print("\n Perfect Score! No failures.")
    #save_markdown_report(accuracy, stats, category_stats, failures)
    return accuracy, stats, category_stats, failures, full_results
