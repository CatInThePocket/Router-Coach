import os
from llm_coach import auto_optimize
from routertest import load_tests
from routertest import get_system_prompt




eval_dataset = load_tests(2)
initial_prompt = get_system_prompt()
print(f"{initial_prompt}")

auto_optimize(initial_prompt, eval_dataset)


