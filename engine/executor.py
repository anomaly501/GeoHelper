# engine/executor.py
import yaml
import os
from engine.tools import geopandas_tools

# This dictionary maps the function names from the YAML to our actual Python functions.
# engine/executor.py

# ... (imports remain the same) ...

# --- THIS IS THE PART TO CHANGE ---
# This dictionary maps the function names from the YAML to our actual Python functions.
# We will map the names the LLM is likely to use.
TOOL_MAPPING = {
    'geopandas.read_file': geopandas_tools.read_file,
    'geopandas.buffer': geopandas_tools.buffer,
    'geopandas.to_file': geopandas_tools.to_file,
    # Add other potential aliases if needed
    'read_vector_file': geopandas_tools.read_file,
    'buffer_vector': geopandas_tools.buffer,
    'save_vector_file': geopandas_tools.to_file
}
# --- END OF CHANGE ---



def execute_workflow(workflow_yaml: str, data_manifest: dict):
    """
    Parses and executes a YAML-defined geoprocessing workflow.
    This version is robust to different YAML formats from the LLM.
    """
    print("\n--- STARTING WORKFLOW EXECUTION ---")
    try:
        workflow_obj = yaml.safe_load(workflow_yaml)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

    # --- ROBUSTNESS FIX ---
    # Check if the loaded YAML is a dictionary with a 'steps' key,
    # or if it's just a list of steps directly.
    steps_list = []
    if isinstance(workflow_obj, dict) and 'steps' in workflow_obj:
        # Case A: LLM provided a full dictionary {'task': ..., 'steps': [...]}
        steps_list = workflow_obj['steps']
    elif isinstance(workflow_obj, list):
        # Case B: LLM provided just the list of steps [...]
        steps_list = workflow_obj
    else:
        raise ValueError("Invalid workflow format. Expected a dictionary with a 'steps' key or a list of steps.")
    # --- END OF FIX ---

    step_outputs = {} # Stores the output of each step, e.g., {'step_1': <GeoDataFrame>}

    for i, step in enumerate(steps_list):
        step_id = step['id']
        function_name = step['function']
        params = step.get('parameters', {})
        
        print(f"\nExecuting Step {i+1}: '{step_id}' ({function_name})")

        # --- Resolve Parameters ---
        resolved_params = {}
        for key, value in params.items():
            # Resolve placeholders like '{{input_rivers}}' or '{{step_1_output}}'
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                placeholder = value.strip('{}').strip() # .strip() for safety
                if placeholder in data_manifest:
                    resolved_params[key] = data_manifest[placeholder]
                    print(f"  > Resolved data input '{placeholder}' to '{data_manifest[placeholder]}'")
                elif placeholder in step_outputs:
                    resolved_params[key] = step_outputs[placeholder]
                    print(f"  > Resolved step input '{placeholder}' from a previous step.")
                else:
                    raise ValueError(f"Could not resolve placeholder: {placeholder}")
            else:
                resolved_params[key] = value

        # --- Define Output Path ---
        # Automatically create an output path for any step that doesn't have one specified
        # and whose function name implies file creation.
        if 'output_path' not in resolved_params and 'save' in function_name or 'buffer' in function_name:
            output_filename = f"{step_id}.geojson"
            output_path = os.path.join('data', 'output', output_filename)
            resolved_params['output_path'] = output_path
        
        # --- Execute Function ---
        if function_name not in TOOL_MAPPING:
            # Provide a helpful error message if the LLM hallucinates a function
            raise NotImplementedError(
                f"Function '{function_name}' is not implemented in the tool mapping. "
                f"Available tools are: {list(TOOL_MAPPING.keys())}"
            )
        
        func_to_call = TOOL_MAPPING[function_name]
        
        result = func_to_call(**resolved_params)
        step_outputs[step_id] = result
        
        if isinstance(result, str):
             print(f"  > Step '{step_id}' completed. Output file at: {result}")

    print("\n--- WORKFLOW EXECUTION FINISHED ---")
    return step_outputs