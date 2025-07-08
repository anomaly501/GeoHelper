# app/main.py

# --- FIX PYTHON PATH ---
# This block must be at the very top of the file
import sys
import os
# Add the project's root directory (the parent of 'app') to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# -----------------------

import streamlit as st
import glob
import re
import traceback
from llm.reasoning_chain import generate_workflow
from engine.executor import execute_workflow
import leafmap.foliumap as leafmap

# --- 1. UTILITY FUNCTIONS ---
def parse_yaml_from_response(response_text: str):
    """Extracts a YAML code block from the LLM's response."""
    if not response_text:
        return None
    # Regex to find a YAML block, allows for optional 'yaml' language specifier
    match = re.search(r"```(?:yaml)?\n(.*?)\n```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback if no code block is found, check if the response itself is valid YAML
    if response_text.lstrip().startswith("task:") or response_text.lstrip().startswith("steps:"):
        return response_text.strip()

    print("Warning: Could not find a YAML code block in the LLM response.")
    return None

def get_available_files(directory="data/input"):
    """Gets a list of file paths from the specified directory."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        return []
    # Using glob to find common vector/raster file types
    patterns = ["*.shp", "*.geojson", "*.gpkg", "*.tif", "*.tiff"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(directory, pattern)))
    return files

# --- 2. STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LLM Geo-Analyst",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ LLM-Powered Geospatial Analyst")
st.write("Ask a spatial question in plain English, and the AI will generate and execute a GIS workflow to answer it.")

# --- 3. UI LAYOUT (Sidebar and Main Area) ---
with st.sidebar:
    st.header("1. Data Input")
    st.info("Add your data files to the `data/input` folder and they will appear here.")
    
    available_files = get_available_files()
    if not available_files:
        st.warning("No data found! Please add files to the `data/input` directory.")
    else:
        st.success(f"Found {len(available_files)} file(s):")
        for f in available_files:
            st.code(os.path.basename(f), language=None)

    st.header("2. Analysis Query")
    user_query = st.text_area(
        "Enter your spatial analysis request:",
        "Create a 10-degree buffer around the rivers and save the result as GeoJSON.",
        height=150
    )
    
    process_button = st.button("Generate & Run Workflow", type="primary", use_container_width=True)

# Initialize session state to hold results and prevent re-runs on widget interaction
if "llm_response" not in st.session_state:
    st.session_state.llm_response = ""
if "workflow_yaml" not in st.session_state:
    st.session_state.workflow_yaml = ""
if "final_outputs" not in st.session_state:
    st.session_state.final_outputs = None
if "error_message" not in st.session_state:
    st.session_state.error_message = ""

# --- 4. BACKEND LOGIC (Triggered by button press) ---
if process_button:
    if not user_query:
        st.error("Please enter a query.")
    elif not available_files:
        st.error("Please add data files to `data/input` before running.")
    else:
        # Clear previous results
        st.session_state.llm_response = ""
        st.session_state.workflow_yaml = ""
        st.session_state.final_outputs = None
        st.session_state.error_message = ""
        
        # Create a placeholder for real-time log display
        log_placeholder = st.empty()

        try:
            with st.spinner("🧠 Step 1/3: AI is thinking and generating a workflow..."):
                # Create data manifest for the LLM
                data_manifest = {os.path.basename(f).split('.')[0]: f for f in available_files}
                st.session_state.llm_response = generate_workflow(user_query, data_manifest)
                st.session_state.workflow_yaml = parse_yaml_from_response(st.session_state.llm_response)

            if not st.session_state.workflow_yaml:
                st.session_state.error_message = "Failed to generate a valid workflow from the LLM. Check the 'LLM Raw Output' tab for details."
                st.error(st.session_state.error_message)
            else:
                log_placeholder.success("✅ Workflow generated successfully!")
                with st.spinner("⚙️ Step 2/3: Executing GIS workflow... Please wait."):
                    st.session_state.final_outputs = execute_workflow(
                        st.session_state.workflow_yaml, 
                        data_manifest
                    )
                log_placeholder.success("✅ Workflow executed successfully!")
                st.balloons()

        except Exception as e:
            st.session_state.error_message = f"An error occurred: {str(e)}"
            st.error(st.session_state.error_message)
            st.code(traceback.format_exc()) # Show full traceback for debugging

# --- 5. RESULTS DISPLAY ---
st.header("Results")

if st.session_state.error_message:
    st.error(f"Last run failed: {st.session_state.error_message}")

# Create tabs for different outputs
tab1, tab2, tab3 = st.tabs(["🗺️ Map Visualization", "⚙️ Generated Workflow (YAML)", "🧠 LLM Raw Output"])

with tab1:
    st.subheader("Map Output")
    if st.session_state.final_outputs:
        m = leafmap.Map(center=[20, 0], zoom=2)
        
        # Find the final GeoJSON output file to display
        output_files = [v for v in st.session_state.final_outputs.values() if isinstance(v, str) and (v.endswith('.geojson') or v.endswith('.shp'))]
        if output_files:
            final_layer_path = output_files[-1]
            st.write(f"Displaying layer: `{os.path.basename(final_layer_path)}`")
            try:
                # Add a style to make the output layer stand out
                style = {"color": "#ff0000", "weight": 2, "opacity": 1, "fillColor": "#ff0000", "fillOpacity": 0.5}
                m.add_vector(final_layer_path, layer_name="Final Output", style=style)
            except Exception as e:
                st.error(f"Could not display map layer: {e}")
        else:
            st.warning("No vector output file (.geojson, .shp) was found to display on the map.")

        m.to_streamlit(height=600)
    else:
        st.info("Run a workflow to see the map visualization here.")

with tab2:
    st.subheader("Generated Workflow")
    if st.session_state.workflow_yaml:
        st.code(st.session_state.workflow_yaml, language="yaml")
    else:
        st.info("Run a workflow to see the generated YAML here.")

with tab3:
    st.subheader("LLM Chain-of-Thought and Raw Output")
    if st.session_state.llm_response:
        st.text_area("LLM Log", st.session_state.llm_response, height=500)
    else:
        st.info("Run a workflow to see the LLM's full reasoning process here.")