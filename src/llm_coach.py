import os
import json
from routertest import get_system_prompt
from routertest import load_tests
from routertest import run_evaluation
from history import save_snapshot
from datetime import datetime
import requests

#eval_dataset = load_tests(1)
#initial_prompt = get_system_prompt()




def auto_optimize(intital_prompt, eval_dataset, max_iterations = 10):
    best_prompt = intital_prompt
    #1. Get the baseline score
    best_accuracy, stats, category_stats, failures, full_results = run_evaluation(best_prompt, eval_dataset)
    save_snapshot(best_accuracy, stats, category_stats, failures, full_results, best_prompt)

    #Coach model variables
    model ="deepseek-r1:8b"
    temperature = 0.7
    coach_prompt_path = "coach_prompt.txt"

    patience = 0

    for i in range(max_iterations):
        print(f"\n---Optimization Round {i+1} ---")

        #2. Ask the coach to refine the prompt based on the failures
        #Use temperature ~0.7 to encourage creative solutions
        new_prompt = call_coach_llm(best_prompt, failures,model, temperature, coach_prompt_path)

        #3. Evaluate new prompt
        new_accuracy, new_stats, new_category_stats, new_failures, new_full_report = run_evaluation(new_prompt, eval_dataset)

        #4. Compare Results
        if new_accuracy > best_accuracy:
            print(f" Improvement! {best_accuracy}% -> {new_accuracy}%")
            best_accuracy = new_accuracy
            best_prompt = new_prompt
            failures = new_failures #Update failure log for the next round
            save_snapshot(new_accuracy, new_stats, new_category_stats, new_failures, new_full_report, new_prompt)
            patience = 0 #reset patience because we improved
        else:
            print(f" No improvement ({new_accuracy}%). reverting to best prompt.")
            patience += 1
            if patience >= 3:
                print("Reached local maximum. Stopping.")
                break
    return best_prompt

def call_coach_llm(current_prompt, failures, model, temperature, coach_prompt_path="coach_prompt.txt"):
    url = "http://localhost:11434/api/chat"
    
    cutoff_date = "March 2023"
    today_date = datetime.now().strftime("%A, %B %d, %Y")
    
    #2. Load template from the test file

      #Load raw text file with the prompt
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts') #os.path twice, up to root and back down to 'prompts'
    coach_prompt_path = os.path.join(base_path, "coach_prompt.txt")

    with open(coach_prompt_path, "r", encoding = "UTF-8") as f:
        coach_prompt = f.read()
    #3. Fil in the blanks
    #We convert failures to a string so it fits in the text
    failure_str = json.dumps(failures, indent=2)

    full_message = coach_prompt.format(
        current_prompt = current_prompt,
        failure_log = failure_str,
        today=today_date,
        cutoff = cutoff_date
    )

    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": full_message},
            
        ],
        "options": {
            "temperature": temperature
        },
        "stream": False
    }
    try:

        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        #Extract the refined prompt from the response
        new_prompt =data['message']['content'].strip()

        #Clean up if the AI wrapped the result in markdown code blocks
        if new_prompt.startswith("```"):
            #Removes opening ```text or similar and closing
            new_prompt = new_prompt.split("\n",1)[-1].rsplit("\n", 1)[0].strip()
        
        return new_prompt
    
    except:
        
        print(f"Calling the model failed")
        return None
    
#auto_optimize(initial_prompt)

