llama_template = (
    "<|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}<|eot_id|>"
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "{user_prompt}<|eot_id|>"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "Epidemiology Assistant: "
)

compartmental_system_prompt = """You are an expert in epidemiological modeling, specialized in analyzing and reusing components from existing compartmental models to support rapid prototyping. Your role is to create a prototype epidemiological compartmental model by systematically reusing and combining components from a given corpus of existing models."""

compartmental_prototyping_template = """ ### Context:
The input is a set of epidemiological compartmental models. These models may vary in format and content. The goal is to accelerate model construction by extracting reusable features (such as compartments, flows, and parameters) and combining them into a valid new prototype model.

### Task:
1.Analyze the input models.
2.Identify features (reusable modeling ideas) in input models. Make sure that all the model elements should be covered by your features.
3.Detect possible relationships or constraints between features (e.g., mutual exclusivity, dependencies).
4.Randomly select a set of features and construct a prototype model by assembling appropriate features, ensuring the result is valid and consistent.

### Input Corpus:
{input_models}

### Response format:
**Identified Features **
    [List features, each with a meaningful name and explanation]
** Feature Relationships **
    [Describe any constraints, dependencies, or conflicts detected between features.]
** Prototype Model **
    [List the selected features]
    [Present the assembled prototype model composed of selected features. Ensure the structure is valid considering the feature relationships.] """
# Later you can add the template for the user prompt (like OU).
