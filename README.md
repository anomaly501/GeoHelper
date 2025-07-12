# 🗺️ LLM-Powered Geospatial Analyst

![Languages Count](https://img.shields.io/github/languages/count/anomaly501/GeoHelper?style=for-the-badge)
![Top Language](https://img.shields.io/github/languages/top/anomaly501/GeoHelper?style=for-the-badge&color=blue)
![License](https://img.shields.io/github/license/anomaly501/GeoHelper?style=for-the-badge&color=green)
![Issues](https://img.shields.io/github/issues/anomaly501/GeoHelper?style=for-the-badge)

An AI agent that functions as a GIS co-pilot, interpreting natural language, generating multi-step geospatial workflows using Chain-of-Thought (CoT) reasoning, and executing them with open-source tools. Built with a local LLM for privacy and offline capability.

---


---

## ✨ Core Features

- **Natural Language to GIS Workflow**  
  Translates queries like “Find flood-prone areas using DEM and river data” into executable GIS operations.

- **Explainable AI (XAI)**  
  Uses Chain-of-Thought (CoT) prompting to generate transparent, step-by-step reasoning.

- **Grounded Generation via RAG**  
  A Retrieval-Augmented Generation pipeline anchors tool usage to real documentation, reducing hallucinations.

- **Intelligent Tool Orchestration**  
  Dynamically builds and executes YAML workflows using GeoPandas, GDAL, Rasterio, etc.

- **Interactive Web Interface**  
  Built with Streamlit featuring chat, Leafmap viewer, CoT logs, and output download.

- **100% Local & Private**  
  All processing—including Mistral-7B LLM—inferred locally via `llama-cpp-python`.

---

## 🏛️ System Architecture

A modular, multi-stage architecture mimicking a GIS expert’s reasoning:

### UI (Streamlit)
- Natural language query input
- File uploader and result display

### LLM Reasoning Engine (`/llm`)
- **RAG Retriever**: ChromaDB-based document retriever
- **CoT Prompting**: Combines query, docs, and file metadata
- **LLM Inference**: Generates Chain-of-Thought and YAML workflow

### Geoprocessing Execution Engine (`/engine`)
- **Workflow Parser**: Parses YAML instructions
- **Tool Dispatcher**: Matches steps to tool wrappers
- **Execution**: Sequential operation execution and data flow

### Visualization & Output (`/app`)
- Leafmap viewer for final result
- CoT log and YAML displayed
- Outputs available for download


---

## 🚀 Getting Started

### 🛠 Prerequisites

- Python 3.10 or 3.11  
- Anaconda or Miniconda (Recommended)  
- `git` installed  
- *(Optional)* NVIDIA GPU + CUDA for better performance

---

### 📦 Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/anomaly501/GeoHelper.git
cd GeoHelper
```

#### 2. Set Up the Environment

```bash
# Using Conda (Recommended)
conda create -n geo_llm python=3.11 -y
conda activate geo_llm

# Install core geospatial dependencies
conda install -c conda-forge gdal geopandas rasterio -y
```

#### 3. Install Python Dependencies

**For GPU Users (CUDA):**

```bash
# Windows
set CMAKE_ARGS="-DLLAMA_CUBLAS=on"
set FORCE_CMAKE=1

# macOS/Linux
export CMAKE_ARGS="-DLLAMA_CUBLAS=on"
export FORCE_CMAKE=1

pip install -r requirements.txt
```

**For CPU-Only Users:**

```bash
pip install -r requirements.txt
```

#### 4. Download the LLM Model

```bash
mkdir models
# Download: Mistral-7B-Instruct-v0.2.Q4_K_M.gguf (~4.37GB)
# Place it inside the models/ directory.
```

#### 5. Build the RAG Knowledge Base

```bash
python llm/knowledge_base/build_kb.py
```

---

## ▶️ Running the App

```bash
conda activate geo_llm
streamlit run app/main.py
```

Your browser will open with the application ready to use!

---

## 🧪 Example Prompts

- "Find low-lying areas (elevation < 100m) within 2km of rivers."
- "Identify new park sites not within 500m of highways."
- "Buffer all roads by 50m and export to GeoJSON."

---

## 🤝 Contributing

We welcome contributions of all kinds:

```bash
# Example workflow
git checkout -b feature/YourFeature
git commit -m "Add new feature"
git push origin feature/YourFeature
```

Then submit a Pull Request with a clear description.

---



