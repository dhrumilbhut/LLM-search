import json
import mlflow
from mlflow.tracking import MlflowClient


MODEL_NAME = "rag-search-model"


def load_production_config() -> dict:
    """
    Loads the RAG configuration of the model currently
    marked as Production in MLflow Model Registry.

    Returns:
        dict: RAG configuration

    Raises:
        Exception: If no Production model exists
    """
    client = MlflowClient()

    # Fetch latest Production model
    versions = client.get_latest_versions(
        name=MODEL_NAME,
        stages=["Production"]
    )

    if not versions:
        raise Exception("No Production model found in MLflow registry")

    prod_version = versions[0]
    run_id = prod_version.run_id

    # Download the config artifact
    artifact_path = client.download_artifacts(
        run_id=run_id,
        path="rag_config.json"
    )

    with open(artifact_path, "r") as f:
        config = json.load(f)

    return config
