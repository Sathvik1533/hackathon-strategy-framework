#!/bin/bash
set -e

# AWS ECS/Fargate Deployment Automation
AWS_REGION=${AWS_REGION:-"us-east-1"}
ECR_REPO_NAME="hackathon-agent-api"
CLUSTER_NAME="hackathon-production-cluster"
SERVICE_NAME="hackathon-agent-service"

echo "🚀 Building and pushing Docker container to AWS ECR..."

# 1. AWS Login
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# 2. Build & Tag
docker build -t $ECR_REPO_NAME:latest -f infra/Dockerfile .
docker tag $ECR_REPO_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest

# 3. Push
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest

# 4. Trigger ECS Service Redeployment
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --force-new-deployment --region $AWS_REGION

echo "✅ Deployment initiated on AWS ECS Fargate!"
