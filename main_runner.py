# main_runner.py
import os
import re
from llm.reasoning_chain import generate_workflow
from engine.executor import execute_workflow

def parse_yaml_from_response(response_text: str):
    """
    A simple utility to extract a YAML code block from the LLM's response.
    """
    # Regex to find a YAML block, allows for optional 'yaml' language specifier
    match = re.search(r"```(?:yaml)?\n(.*?)\n```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        # Fallback if no code block is found, assume the whole response is YAML
        print("Warning: Could not find a YAML code block. Attempting to parse entire response.")
        return response_text.strip()

if __name__ == '__main__':
    # 1. DEFINE THE PROBLEM
    # This simulates a user query and uploaded data.
    # In the Streamlit app, this data will come from the UI.
    user_query = "I have a shapefile of rivers. Create a 500 meter buffer around them and save the result."
    
    # IMPORTANT: We need a dummy file for this to work.
    # Create a placeholder file. You can replace this with a real shapefile later.
    dummy_river_path = os.path.join('data', 'input', 'rivers.txt')
    with open(dummy_river_path, 'w') as f:
        f.write("This is a placeholder for a river shapefile.")

    data_manifest = {
        'input_rivers': dummy_river_path
    }

    # 2. LLM REASONING (The "Brain")
    # Generate the Chain-of-Thought and the YAML workflow plan.
    llm_response = generate_workflow(user_query, data_manifest)
    
    print("\n\n--- 🧠 LLM Full Response ---")
    print(llm_response)
    print("----------------------------\n")

    # 3. PARSE THE WORKFLOW
    # Extract the clean YAML from the full text response.
    workflow_yaml = parse_yaml_from_response(llm_response)
    
    if not workflow_yaml:
        print("🛑 Could not extract a valid workflow from the LLM response. Exiting.")
        exit()
        
    print("--- ამოღებული YAML Workflow ---")
    print(workflow_yaml)
    print("-----------------------------\n")

    # 4. EXECUTION ENGINE (The "Hands")
    # Run the parsed workflow.
    # Note: This will fail right now because our dummy file is not a real shapefile,
    # but it will correctly call the first step 'geopandas.read_file'.
    # This proves the entire pipeline is connected.
    try:
        final_outputs = execute_workflow(workflow_yaml, data_manifest)
        print("\n✅ System executed successfully!")
        print("Final outputs:", final_outputs)
    except Exception as e:
        print(f"\n🛑 An error occurred during workflow execution: {e}")
        print("This is expected if using a dummy input file. The key is that the system tried to run.")