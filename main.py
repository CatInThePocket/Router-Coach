import os
import logging
import sys
import yaml
import traceback
from pathlib import Path
from src.llm_coach import auto_optimize
from src.routertest import load_tests, get_system_prompt
from src.config_utils import load_config


# 1. Setup basic logging (Cleaner than multiple print statements)
#logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')



def setup_file_logging():
    # 1. Get the path from the YAML we just fixed
    config = load_config()
    # Use the root-relative path from your YAML
    log_dir = Path(config['paths']['snapshot_dir']).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "session.log"

    # 2. THE FIX: Force the configuration
    # 'force=True' resets any logging set by previous imports
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler(sys.stdout) # This keeps your terminal "Painting"
        ],
        force=True 
    )
    
    # 3. Print this to confirm the path in the terminal
    print(f"📝 Logging session to: {log_file.absolute()}")



def main():
    """
    Main entry point for the LLM Prompt Optimization loop.

   
    """
     # MUST BE THE FIRST CALL
    setup_file_logging()
    
    logging.info("Initializing Prompt Optimizer with Config...")

    # 1. Load Settings from YAML
    cfg_data = load_config()

    #2. Extract values for readability
    router_cfg = cfg_data['router']
    coach_config = cfg_data['coach']
    process_cfg = cfg_data['process']

    #3. Load balanced dataset using config value
    #Pass the samles per category value
    eval_dataset = load_tests(router_cfg['samples_per_category'])
  

    # 4. Fetch the starting system prompt
    initial_prompt = get_system_prompt()
    
    logging.info(f"Starting optimization with initial prompt (length: {len(initial_prompt)})")

    import src.routertest as rt
    print(f"DEBUG: I am loading routertest from: {rt.__file__}")

    # 5. Start the optimization loop with the config paramenters
    try:
        auto_optimize(
            initial_prompt = initial_prompt,
            eval_dataset = eval_dataset,
            max_iterations = coach_config['max_iterations'],
            coach_model = coach_config['model'],
            temperature = coach_config['temperature'],
            timeout = coach_config['timeout'],
            patience_limit = coach_config['patience'],
            verbose = process_cfg['verbose']
        )
        logging.info("Optimization process completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during optimization: {e}")
        traceback.print_exc() 


if __name__ == "__main__":
    main()
