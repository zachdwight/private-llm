FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git build-essential cmake curl wget libopenblas-dev \
    libcurl4-openssl-dev \
    supervisor python3 && \
    apt-get clean

# Set up working directory
WORKDIR /app

# Clone and build llama.cpp using CMake
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    mkdir build && cd build && \
    cmake .. -DLLAMA_BUILD_SERVER=ON -DLLAMA_CURL=OFF && \
    cmake --build . --config Release && \
    ls -l

# Download TinyLlama GGUF model
RUN mkdir -p /app/models && \
    wget -O /app/models/tinyllama.gguf \
    https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf



# Copy frontend, server, and supervisor config into image
COPY frontend /app/frontend
COPY server.py /app/server.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Expose both ports
EXPOSE 8080 8081

# Start both servers via supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
