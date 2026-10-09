#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -f .env ] || cp .env.example .env
set -a; source .env; set +a

curl -sf http://localhost:11434/api/version >/dev/null || { echo "Ollama not running: start it with 'ollama serve'"; exit 1; }
models=$(ollama list)
grep -q "^${OLLAMA_MODEL}" <<<"$models" || { echo "Model ${OLLAMA_MODEL} not found in ollama"; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker daemon not running: open Docker Desktop first"; exit 1; }

mkdir -p workspace

tty_flags=(-i)
[ -t 0 ] && tty_flags+=(-t)

docker run "${tty_flags[@]}" --rm --pull=always \
  --name openhands-app \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.openhands.dev/openhands/runtime:${RUNTIME_VERSION} \
  -e SANDBOX_VOLUMES="$PWD/workspace:/workspace:rw" \
  -e LLM_MODEL="ollama/${OLLAMA_MODEL}" \
  -e LLM_BASE_URL="${LLM_BASE_URL}" \
  -e LLM_API_KEY="${LLM_API_KEY}" \
  -e LOG_ALL_EVENTS=true \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$HOME/.openhands:/.openhands" \
  -p "${OPENHANDS_PORT}:3000" \
  --add-host host.docker.internal:host-gateway \
  docker.openhands.dev/openhands/openhands:${OPENHANDS_VERSION}
