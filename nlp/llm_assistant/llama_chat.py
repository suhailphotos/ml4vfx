import os
import subprocess
import sys
from pathlib import Path

def setup_llama(base_dir):
    base_dir = Path(base_dir).resolve()
    base_dir.mkdir(exist_ok=True, parents=True)
    os.chdir(base_dir)

    print(f"Setting up Llama in: {base_dir}")

    #install the pkgs
    subprocess.check_call([sys.executable, "-m", "pip", "install", "llama-cpp-python"])

    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    model_path = base_dir / "llama-2-7b-chat.gguf"

    if not model_path.exists():
        print(f"Downloading model file to {model_path}")
        subprocess.check_call(["curl", "-L", model_url, "-o", str(model_path)])

    return model_path

def chat_with_llama(model_path):
    from llama_cpp import Llama

    llm = Llama(
        model_path=str(model_path),
        n_ctx=2048,
        n_threads=8,
        chat_format="llama-2"
    )

    print("\nLlama Chat Interface")
    print("Type 'exit' to quit.\n")
    print("-" * 50)

    messages = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        response = llm.create_chat_completion(messages)
        assistant_message = response["choices"][0]["message"]["content"]

        messages.append({"role": "assistant", "content": assistant_message})

        print("\nAssistant:")
        print(assistant_message.strip())
        print("-" * 50)

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            custom_dir = sys.argv[1]
        else:
            custom_dir = "."

        model_path = setup_llama(custom_dir)
        chat_with_llama(model_path)
    except Exception as e:
        print(f"An error occurred: {e}")