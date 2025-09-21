import time
from prompt_templates import (
    compartmental_system_prompt,
    compartmental_prototyping_template,
    llama_template
)
from config import ExLlamaArguments
import exllamav2
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer, Timer
from exllamav2.generator import ExLlamaV2DynamicGenerator, ExLlamaV2DynamicJob, ExLlamaV2Sampler
from transformers import HfArgumentParser


# parse arguments
parser = HfArgumentParser(ExLlamaArguments)
model_args = parser.parse_args_into_dataclasses()[0]

dataset_path = model_args.dataset_path
model_dir = model_args.model_dir
output_path = model_args.output_path
checkpoint_path = model_args.checkpoint_path
save_steps = model_args.save_steps
config = ExLlamaV2Config(model_dir)
config.arch_compat_overrides()
model = ExLlamaV2(config)
cache = ExLlamaV2Cache(model, max_seq_len = model_args.max_seq_len, lazy = True)
model.load_autosplit(cache, progress = True)

print("Loading tokenizer...")
tokenizer = ExLlamaV2Tokenizer(config)

generator = ExLlamaV2DynamicGenerator(
    model=model,
    cache=cache,
    tokenizer=tokenizer,
    max_batch_size=model_args.max_batch_size,
    max_q_size=model_args.max_q_size
)

gen_settings = ExLlamaV2Sampler.Settings(
    token_repetition_penalty = model_args.gen_settings[0],
    temperature = model_args.gen_settings[1],
)


# -------------------
# Load epidemiology models
# -------------------

epi_file_paths = [
    "../epi_models/carol/m2.cmp",
    "../epi_models/carol/m1.cmp",
    "../epi_models/carol/m3.cmp"
]

all_epi_models = []
for path in epi_file_paths:
    with open(path, "r") as f:
        text = f.read().strip()
        all_epi_models.append(text)


# -------------------
# Conversation setup
# -------------------

# --- Conversation history ---
conversation_history = compartmental_prototyping_template.format(input_models=all_epi_models)



# --- Interactive loop ---
while True:
    with exllamav2.util.get_basic_progress() as progress:  # >>> NEW
        task = progress.add_task("Creating jobs", total=1)   # >>> NEW
        # Format prompt
        input_prompt = llama_template.format(
            system_prompt=compartmental_system_prompt,
            user_prompt=conversation_history
        )
        # Encode
        input_ids = tokenizer.encode(input_prompt, encode_special_tokens=True, add_bos=False)

        # Job
        job = ExLlamaV2DynamicJob(
            input_ids=input_ids,
            gen_settings=gen_settings,
            max_new_tokens=model_args.max_new_tokens,
            stop_conditions=[tokenizer.single_id("<|eot_id|>")],
            token_healing=True,
            identifier=0,
        )

        # Run generation
        generator.enqueue(job)
        progress.update(task, advance=1)

    print("\nAssistant is thinking...\n")
    response_text = ""
    samples = []
    num_completions = 0
    num_tokens = 0
    time_begin = time.time()

    with exllamav2.util.get_basic_progress() as progress: 
        task = progress.add_task("Generating response", total=generator.num_remaining_jobs()) 


        while generator.num_remaining_jobs():
            results = generator.iterate()
            bsz = len(set([r["identifier"] for r in results]))
            num_tokens += bsz

            for result in results:
                if result["eos"]:
                    response_text = result["full_completion"]
                    print(response_text)
                    # Measure performance
                    num_completions += 1
                    elapsed_time = time.time() - time_begin
                    rpm = num_completions / (elapsed_time / 60)
                    tps = num_tokens / elapsed_time
                    print()
                    print("---------------------------------------------------------------------------")
                    print(f"Current batch size: {bsz}")
                    print(f"Avg. completions/minute: {rpm:.2f}")
                    print(f"Avg. output tokens/second: {tps:.2f}")
                    print("---------------------------------------------------------------------------")
                    break
            progress.update(task, advance=len(results))

    # --- Ask user for next step ---
    user_input = input("\nYour reply (or type 'exit'): ").strip()
    if user_input.lower() == "exit":
        break

    # Add user input to conversation history
    conversation_history += f"\n\nUser: {user_input}"

