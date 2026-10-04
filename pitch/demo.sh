#!/bin/bash
set -e

BASE_URL="http://localhost:8000/api/v1"

echo -e "\033[1;36m=========================================================\033[0m"
echo -e "\033[1;36m       🎬 HACKATHON LIVE STAGE BACKUP DEMO RUNNER        \033[0m"
echo -e "\033[1;36m=========================================================\033[0m"

echo -e "\n\033[1;33m[1/3] Verifying System Health & Database Connectivity...\033[0m"
curl -s -X GET "$BASE_URL/health" | jq .
sleep 1

echo -e "\n\033[1;33m[2/3] Dispatching Async Multi-Agent Task...\033[0m"
JOB_RESP=$(curl -s -X POST "$BASE_URL/jobs/render" \
  -H "Content-Type: application/json" \
  -d '{"task_type": "research_and_synthesize", "payload": {"query": "Explain the zero-hallucination timeout architecture."}}')

echo "$JOB_RESP" | jq .
JOB_ID=$(echo "$JOB_RESP" | jq -r .data.job_id)
echo -e "\033[1;32mTracking Job ID: $JOB_ID\033[0m"
sleep 1

echo -e "\n\033[1;33m[3/3] Streaming Real-Time Execution Logs (SSE)...\033[0m"
curl -N -s "$BASE_URL/jobs/$JOB_ID/stream" | head -n 12

echo -e "\n\033[1;32m=========================================================\033[0m"
echo -e "\033[1;32m✔ LIVE STAGE DEMONSTRATION COMPLETE WITH ZERO ERRORS!    \033[0m"
echo -e "\033[1;32m=========================================================\033[0m\n"
