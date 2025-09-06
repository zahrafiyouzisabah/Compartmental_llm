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



multi_step_compartmental_prototyping_template = [
"""You are an expert in epidemiological modeling, skilled at comparing and matching elements across different compartmental models.
### Context:
You are performing Step 1: Variant Matching in a workflow for rapid prototyping of epidemiological models. The input is a set of epidemiological compartmental models. These models may vary in format and content.  Your job is to find which elements mean the same thing and which ones are different.

### Previous Steps Responses:
{previous_llm_response}

### Input Corpus:
{input_models}

### Current Step Tasks:
1.Analyze the input models.
2.Match elements that represent the same concept (Two Susceptible compartments that exist in two different models).
3.Point out elements that appear in only one model (unique ones).

### Response format:
** Matched Elements **
[List groups of elements that are the same concept.]
Example: (
(Element: Compartment Susceptible, source: model1), (Element: Compartment Susceptible, source: model2)
(Element: Flow x-y, source: model 2), (Element: Flow x-y, source: model 3)
)

** Unique elements **
[List elements that appear only once across all models.]""",
"""System role:
You are an expert in epidemiological modeling, skilled at finding reusable structures across compartmental models.

### Context:
You are performing Step 2: Feature Identification in a workflow for rapid prototyping of epidemiological models. 

### Summary of Previous Step(s):
In Step 1 (Variant Matching), equivalent elements across different models were identified and grouped together, while elements that appeared only once were marked as unique. You must now use the previous steps results and the input corpus as the basis for this step.

### Previous Steps Responses:
{previous_llm_response}

### Input Corpus:
{input_models}

### Current Step Tasks:
1.Use the equivalence classes and unique elements from Step 1.
2.Find groups of elements that appear together across the models.
3.Organize these clusters by how common they are:
 -Patterns present in all models.
 -Patterns present in most models (n–1, n–2, …).
 -Patterns unique to one model.
4.Treat each cluster as a feature.
5.Give each feature a clear, meaningful name (e.g., “SEIR Core”, “Hospitalization Pathway”).
6.Explain what elements belong to that feature and why they form a group.

### Response format:

** Identified Features **
-Feature Name: [name you assign]
-Elements: [list of matched/unique elements included, with model references]
-Pattern Frequency: [ How many models | unique]
-Reason: [why these elements form a feature]"

""",
"""
You are performing Step 3: Feature Relationship Identification in a workflow for rapid prototyping of epidemiological models. The input is the set of features identified in the previous step. The goal is to find relationships between these features that affect how they can be combined in a valid prototype model. Relationships can include constraints such as mutual exclusivity, dependencies, or overlaps in parameters.

### Summary of Previous Step(s):
In Step 1 (Variant Matching), equivalent elements across models were grouped together, and unique ones were flagged.  
In Step 2 (Feature Identification), those elements were clustered into features representing reusable modeling ideas, each given a clear name and explanation.  
Now, in Step 3, the goal is to discover how these features relate to each other.

### Previous Steps Responses:
{previous_llm_response}

### Input Corpus:
{input_models}

### Current Step Tasks:
1. Look at the identified features and detect relationships between features, such as:
   - Mutual exclusivity: two features cannot be used together.  
   - Dependencies: one feature requires another to be present.  
   - Overlaps/conflicts: features that use the same parameters but assign different values.  

2.List the identified Relationships and provide reasoning for why the relationship exists.

### Response format:
**Feature Relationships**
- Left-Hand Side Feature: [feature name]  
- Right-Hand Side Features: [list of related features]  
- Relationship Type: [mutual exclusivity | dependency | overlap/conflict | other]  
- Reason: [explanation]  
""",
"""
System role:
You are an expert in epidemiological modeling, skilled at assembling prototype compartmental models from reusable features.

### Context:
You are performing Step 4: Prototype Model Construction in a workflow for rapid prototyping of epidemiological models. At this point, features have been identified (Step 2) and their relationships have been analyzed (Step 3). The goal of this step is to select a set of features and construct a valid prototype model that respects the identified relationships and constraints.

### Summary of Previous Step(s):
- Step 1 (Variant Matching): Equivalent elements across models were grouped, and unique elements were flagged.  
- Step 2 (Feature Identification): Features were identified by clustering elements that frequently appear together.  
- Step 3 (Feature Relationship Identification): Constraints between features were identified, such as mutual exclusivity, dependencies, and overlaps/conflicts.  
Now, in Step 4, the goal is to build a valid prototype model by combining features into a coherent structure.

### Previous Steps Responses:
{previous_llm_response}

### Input Corpus:
{input_models}

### Current Step Tasks:
1. Randomly select a subset of identified features.  
2. Check the selected features against the constraints from Step 3.  
   - If conflicts are found (e.g., mutual exclusivity, parameter conflicts), revise the selection until a valid combination is reached.  
3. Assemble the prototype model from the selected features.  
4. Ensure the prototype is coherent, consistent, and valid as an epidemiological compartmental model.  


### Response format:
**Selected Features**  
- [List of feature names chosen]

**Prototype Model**  
[Present the final prototype model]
"""

]
