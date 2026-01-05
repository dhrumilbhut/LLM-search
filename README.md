# LLM Search Platform

Production-grade semantic search and recommendation system using LLMs.

## Goals
- Build a scalable LLM-powered search system
- Track experiments with MLflow
- Automate pipelines with Airflow
- Optimize for latency and cost
- Deploy using cloud-native infrastructure

## High-Level Architecture
Data Ingestion → Embeddings → Vector Search → LLM Generation → API

## Tech Stack
- FastAPI
- PostgreSQL + pgvector
- MLflow
- Airflow
- Docker
- AWS (ECS, SageMaker)
