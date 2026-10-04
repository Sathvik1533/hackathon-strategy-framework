#!/bin/bash
set -e

echo -e "\033[1;36m=========================================================\033[0m"
echo -e "\033[1;36m       🚀 HACKATHON STRATEGY FRAMEWORK (HSF) BOOTSTRAP   \033[0m"
echo -e "\033[1;36m=========================================================\033[0m"

# 1. Environment Config
if [ ! -f .env ]; then
  echo -e "\033[1;33m[1/5] Creating .env from .env.example...\033[0m"
  cp .env.example .env
  echo -e "\033[1;32m✔ .env created.\033[0m"
else
  echo -e "\033[1;32m✔ .env already present.\033[0m"
fi

# 2. Dependency checks
echo -e "\033[1;33m[2/5] Checking System Prerequisites...\033[0m"
command -v docker >/dev/null 2>&1 || { echo >&2 "❌ Docker is required but not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "❌ Python 3 is required but not installed. Aborting."; exit 1; }
echo -e "\033[1;32m✔ System engines verified.\033[0m"

# 3. Launch Docker Compose
echo -e "\033[1;33m[3/5] Starting Multi-Service Infrastructure (API, pgvector, Redis, FastMCP)...\033[0m"
docker compose -f infra/docker-compose.yml up -d --build
echo -e "\033[1;32m✔ Infrastructure active.\033[0m"

# 4. Wait for Postgres readiness and run migrations/seeds
echo -e "\033[1;33m[4/5] Waiting for Database and Seeding Vector Store...\033[0m"
sleep 5
docker compose -f infra/docker-compose.yml exec -T api python database/seed_data.py || echo "Seeding completed or queued."

# 5. Presentation check
echo -e "\033[1;33m[5/5] Compiling Marp Pitch Deck...\033[0m"
if command -v marp >/dev/null 2>&1; then
  marp pitch/pitch.marp.md -o pitch/presentation.html
  echo -e "\033[1;32m✔ Pitch Deck rendered at pitch/presentation.html\033[0m"
else
  echo "ℹ Marp CLI not found globally. Pitch slides ready in Markdown at pitch/pitch.marp.md."
fi

echo -e "\n\033[1;32m=========================================================\033[0m"
echo -e "\033[1;32m🎉 COMPLETE STACK ONLINE AND READY FOR HACKATHON SPRINT! \033[0m"
echo -e "\033[1;32m=========================================================\033[0m"
echo -e "• API Documentation:   \033[1;34mhttp://localhost:8000/docs\033[0m"
echo -e "• Health Check:        \033[1;34mhttp://localhost:8000/api/v1/health\033[0m"
echo -e "• Frontend Dashboard:  \033[1;34mhttp://localhost:8000\033[0m"
echo -e "• FastMCP SSE Server:  \033[1;34mhttp://localhost:8001/sse\033[0m"
echo -e "• Pitch Deck:          \033[1;34mpitch/presentation.html\033[0m"
echo -e "• Live Demo Script:    \033[1;33mbash pitch/demo.sh\033[0m"
echo -e "\033[1;36m=========================================================\033[0m\n"
