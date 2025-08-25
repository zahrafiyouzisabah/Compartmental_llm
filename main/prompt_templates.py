llama_template = (
    "<|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}<|eot_id|>"
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "{user_prompt}<|eot_id|>"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "Epidemiology Assistant: "
)

compartmental_system_prompt = """You are an expert in epidemiology modeling. You help design new compartmental epidemiology models by reusing features from existing models."""

# Later you can add the template for the user prompt (like OU).