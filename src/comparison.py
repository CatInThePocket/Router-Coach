import os
import json

def get_latest_snapshot():
    if not os.path.exists("history"):
        return None
    
    #Get all .json files in the history folder
    files = [f for f in os.listdir("history") if f.endswith(".json")]
    if not files:
        return None
    
    #Sort them (they are named by timestamp, so the last one is the newest)
    files.sort()

    latest_file = os.path.join("history", files[-1])

    with open(latest_file, "r") as f:
        return json.load(f)
    
def compare_runs(new_results, old_results):
    deltas = []

    #We turn the old rsults into a dictionary for fast Lookup by "query"
    old_map = {item['query']: item for item in old_results['full_results']}

    for new_item in new_results:
        query = new_item['query']
        old_item = old_map.get(query)       
        if old_item:
            # Dis the status change?
            if old_item['is_correct'] == False and new_item['is_correct'] == True:
                deltas.append({"query": query, "status": "FIXED", "old": old_item['actual'], "new": new_item['actual']})
            elif old_item['is_correct'] == True and new_item['is_correct'] == False:
                deltas.append({"query": query, "status": "REGRESSED", "old": old_item['actual'], "new": new_item['actual']})

    return deltas