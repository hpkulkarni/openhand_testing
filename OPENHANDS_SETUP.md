# OpenHands + Ollama (Qwen3-Coder)

1. Start Ollama and Docker Desktop.
2. `./start.sh`
3. Open http://localhost:3000. If the LLM isn't preconfigured, go to Settings > LLM > Advanced:
   - Custom Model: `ollama/qwen3-coder-64k`
   - Base URL: `http://host.docker.internal:11434`
   - API Key: `ollama`

Edit `.env` (copied from `.env.example`) to change model/versions. Agent files live in `./workspace`.
