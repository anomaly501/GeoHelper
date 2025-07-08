from llama_cpp import Llama
import os

# Define the path to the model
model_path = os.path.join("models", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# Check if the model file exists
if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}")
    print("Please download the model and place it in the 'models' directory.")
    exit()

print("Loading LLM model... This may take a moment.")

# Initialize the Llama model
# n_gpu_layers=-1 means to offload all possible layers to the GPU.
# Set to 0 if you want to run on CPU only.
llm = Llama(
    model_path=model_path,
    n_ctx=4096,         # Context window size
    n_threads=8,        # Number of CPU threads to use
    n_gpu_layers=-1     # Offload all layers to GPU if available
)

print("Model loaded successfully.")

# Define a simple prompt
prompt = "Question: what is capital of india Answer:"

# Generate a response
output = llm(
    prompt,
    max_tokens=256,  # Maximum number of tokens to generate
    stop=["Question:", "\n"],  # Stop generating when these strings are encountered
    echo=True       # Echo the prompt in the output
)

print("\n--- LLM Response ---")
print(output['choices'][0]['text'])
print("--------------------")