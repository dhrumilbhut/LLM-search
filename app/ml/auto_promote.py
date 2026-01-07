import mlflow
from mlflow.tracking import MlflowClient
from mlflow.exceptions import RestException


MODEL_NAME = "rag_pipeline"
EXPERIMENT_NAME = "rag-evaluation"


def should_promote(new_metrics, prod_metrics):
    """
    Promotion policy.
    Returns True if new model should replace Production.
    """
    if prod_metrics is None:
        return True  # bootstrap case

    return (
        new_metrics["avg_retrieval_score"] >= prod_metrics["avg_retrieval_score"]
        and new_metrics["avg_generation_score"] >= prod_metrics["avg_generation_score"]
        and new_metrics["avg_latency"] <= prod_metrics["avg_latency"]
    )


def ensure_registered_model(client: MlflowClient):
    """
    Create the registered model if it does not exist.
    Idempotent.
    """
    try:
        client.create_registered_model(MODEL_NAME)
        print(f"📦 Created registered model: {MODEL_NAME}")
    except RestException:
        # Already exists
        pass


def get_production_metrics(client: MlflowClient):
    """
    Fetch metrics of the Production model, if it exists.
    Returns None if this is the first run.
    """
    try:
        prod_versions = client.get_latest_versions(
            MODEL_NAME, stages=["Production"]
        )
    except RestException:
        return None

    if not prod_versions:
        return None

    prod_run = client.get_run(prod_versions[0].run_id)
    return prod_run.data.metrics


def promote_latest_run():
    client = MlflowClient()
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Get latest evaluation run
    runs = mlflow.search_runs(
        experiment_names=[EXPERIMENT_NAME],
        order_by=["start_time DESC"],
        max_results=1,
    )

    if runs.empty:
        raise RuntimeError("No evaluation runs found")

    latest = runs.iloc[0]
    run_id = latest["run_id"]

    new_metrics = {
        "avg_retrieval_score": latest["metrics.avg_retrieval_score"],
        "avg_generation_score": latest["metrics.avg_generation_score"],
        "avg_latency": latest["metrics.avg_latency"],
    }

    # Ensure model exists
    ensure_registered_model(client)

    # Fetch production metrics (if any)
    prod_metrics = get_production_metrics(client)

    if should_promote(new_metrics, prod_metrics):
        mv = client.create_model_version(
            name=MODEL_NAME,
            source=f"runs:/{run_id}/model",
            run_id=run_id,
        )

        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=mv.version,
            stage="Production",
            archive_existing_versions=True,
        )

        print("✅ Promoted new model to Production")
    else:
        print("❌ Model not better than current Production")
