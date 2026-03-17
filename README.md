# TinyLLaMA Chat

A lightweight, self-contained chatbot app that runs a small language model locally—no APIs, no agents, no external dependencies. Just you, your computer, and an AI model.

Perfect for:
- 🎓 Learning how LLMs work
- 🏢 Private, offline AI conversations
- 💻 Prototyping and experimentation
- 🚀 Running AI on modest hardware (the entire model + server is ~2GB)

Built with [TinyLLaMA](https://huggingface.co/cognitivecomputations/TinyLlama-1.1B) (1.1B parameters), [`llama.cpp`](https://github.com/ggerganov/llama.cpp) for fast C++ inference, and a clean web interface. Everything runs in Docker.

---

## ⚡ Quick Start

```bash
# Clone and enter the directory
git clone https://github.com/zachdwight/chatbot-app-tinyllama.git
cd chatbot-app-tinyllama

# Build and run
docker build -t tinyllama .
docker run -p 8081:8081 tinyllama
```

Then open **[http://localhost:8081](http://localhost:8081)** in your browser and start chatting.

---

## 💡 Use Cases

### Personal Assistant
Use it as a private notepad companion—ask questions, brainstorm, or get writing help without sending data anywhere.

### Learning Tool
Experiment with different prompts, model parameters (temperature, response length), and see how the model behaves. Perfect for AI/ML students.

### Offline Development
Need AI assistance while offline or without API keys? Run it locally and integrate it into your own apps via the REST API.

### Privacy-First Workflows
Handle sensitive documents or conversations locally. Everything stays on your machine.

---

## 🎮 Features

- **Adjustable creativity**: Temperature slider (0–2) for more predictable or creative responses
- **Control response length**: Set max tokens from 10 to 4096
- **Clear chat history**: Button to reset and start fresh
- **Error handling**: User-friendly messages if something goes wrong
- **Responsive design**: Works on desktop and mobile
- **No external APIs**: Everything runs locally

---

## 🚀 Running It

### Option 1: Docker (Recommended)
```bash
docker build -t tinyllama .
docker run -p 8081:8081 tinyllama
```

Visit [http://localhost:8081](http://localhost:8081)

### Option 2: Manual Setup
If you prefer not to use Docker:

```bash
# Install dependencies (macOS)
brew install cmake openblas

# Clone and build llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && mkdir build && cd build
cmake .. -DLLAMA_BUILD_SERVER=ON
cmake --build . --config Release

# Download TinyLLaMA model
mkdir -p ../models
cd ../models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# Start the backend (in one terminal)
cd ../build/bin
./llama-server -m ../models/tinyllama.gguf -p 8080

# Start the frontend (in another terminal)
cd /path/to/chatbot-app-tinyllama
python3 server.py
```

Visit [http://localhost:8081](http://localhost:8081)

---

## 🔌 REST API

The backend exposes a completion endpoint. Use it to integrate the model into your own apps:

```bash
curl -X POST http://localhost:8080/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of Spain?",
    "n_predict": 128,
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "content": "The capital of Spain is Madrid..."
}
```

---

## ⚙️ Configuration

### Change the Model
Edit the `Dockerfile` and replace the model URL:
```dockerfile
wget -O /app/models/tinyllama.gguf \
  https://huggingface.co/[your-model-url]
```

Find more GGUF models at [ggml.org/models](https://ggml.org/models).

### Adjust Context Size
Edit `supervisord.conf` and change the `-c` flag:
```ini
command=/app/llama.cpp/build/bin/llama-server -m /app/models/tinyllama.gguf -c 4096
```

Higher values use more memory but allow longer conversations.

---

## 📁 Project Structure

```
chatbot-app-tinyllama/
├── Dockerfile              # Container setup
├── supervisord.conf        # Process manager config
├── server.py               # Python reverse proxy + static server
├── frontend/
│   └── index.html          # Web UI
└── README.md
```

---

## 🛠️ Tech Stack

- **Backend**: [llama.cpp](https://github.com/ggerganov/llama.cpp) (C++) for fast inference
- **Proxy**: Python `http.server` (handles CORS, static files, API proxying)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Process Management**: `supervisord` in Docker
- **Containerization**: Docker

---

## 🐛 Troubleshooting

**Model download times out**
The initial `docker build` downloads ~2GB. If it's slow, you may need to add the model manually.

**"Cannot reach server" error**
Make sure both services are running:
- Backend should be on `localhost:8080`
- Frontend should be on `localhost:8081`

**Out of memory**
Reduce context size (`-c 1024` instead of default) or upgrade your hardware.

---

## 📝 License

MIT — but credit to:
- [llama.cpp](https://github.com/ggerganov/llama.cpp) for the incredible inference engine
- [TinyLLaMA](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF) for the compact model
- [TheBloke](https://huggingface.co/TheBloke) for the GGUF quantizations
