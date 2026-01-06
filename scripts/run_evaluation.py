import sys
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import mlflow
from app.ml.eval_data import EVAL_QUERIES
from app.ml.evaluate_retrieval import evaluate_retrieval
from app.ml.evaluate_generation import evaluate_generation

import json
import mlflow
import mlflow.pyfunc
from app.ml.rag_model import RagConfigModel
from app.ml.model_config import RAG_CONFIG

EXPERIMENT_NAME = "rag-evaluation"

def run():
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run():
        

        total_latency = 0
        retrieval_scores = []
        generation_scores = []

        for item in EVAL_QUERIES:
            start = time.time()
            retrieval = evaluate_retrieval(
                item["query"],
                item["expected_keywords"]
            )
            generation = evaluate_generation(
                item["query"],
                item["expected_keywords"]
            )
            latency = time.time() - start

            retrieval_scores.append(retrieval)
            generation_scores.append(generation)
            total_latency += latency

        mlflow.log_metric("avg_retrieval_score", sum(retrieval_scores)/len(retrieval_scores))
        mlflow.log_metric("avg_generation_score", sum(generation_scores)/len(generation_scores))
        mlflow.log_metric("avg_latency", total_latency / len(EVAL_QUERIES))

        mlflow.log_params(RAG_CONFIG)
        with open("rag_config.json", "w") as f:
            json.dump(RAG_CONFIG, f)

        mlflow.log_artifact("rag_config.json")

        mlflow.pyfunc.log_model(
            artifact_path="rag_model",
            python_model=RagConfigModel(),
            artifacts={"config": "rag_config.json"}
        )

        mlflow.register_model(
            model_uri=f"runs:/{mlflow.active_run().info.run_id}/rag_model",
            name="rag-search-model"
        )

if __name__ == "__main__":
    run()
