# 🗺️ LLM-Powered Geospatial Analyst

![Languages Count](https://img.shields.io/github/languages/count/anomaly501/GeoHelper?style=for-the-badge)
![Top Language](https://img.shields.io/github/languages/top/anomaly501/GeoHelper?style=for-the-badge&color=blue)
![License](https://img.shields.io/github/license/anomaly501/GeoHelper?style=for-the-badge&color=green)
![Issues](https://img.shields.io/github/issues/anomaly501/GeoHelper?style=for-the-badge)

An AI agent that functions as a GIS co-pilot, interpreting natural language, generating multi-step geospatial workflows using Chain-of-Thought (CoT) reasoning, and executing them with open-source tools. Built with a local LLM for privacy and offline capability.

---

## 🎥 Demo

*A short GIF demonstrating the workflow: user enters a query, the AI generates a plan, executes it, and displays the result on a map.*

> 🔧 *Placeholder: Add a GIF showcasing your app in action.*

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

> 🔧 *Placeholder: Add an architecture diagram here.*

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
# GeoHelper
