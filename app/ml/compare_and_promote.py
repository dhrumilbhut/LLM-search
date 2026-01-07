import mlflow
from mlflow.tracking import MlflowClient


EXPERIMENT_NAME = "rag-evaluation"
MODEL_NAME = "rag_pipeline"


def should_promote(new_metrics, prod_metrics):
    if prod_metrics is None:
        return True  # first ever model

    return (
        new_metrics["avg_retrieval_score"] >= prod_metrics["avg_retrieval_score"]
        and new_metrics["avg_generation_score"] >= prod_metrics["avg_generation_score"]
        and new_metrics["avg_latency"] <= prod_metrics["avg_latency"]
    )


def promote_if_better():
    client = MlflowClient()
    mlflow.set_experiment(EXPERIMENT_NAME)

    runs = mlflow.search_runs(
        experiment_names=[EXPERIMENT_NAME],
        order_by=["start_time DESC"],
        max_results=1,
    )

    if runs.empty:
        raise RuntimeError("No evaluation runs found")

    latest = runs.iloc[0]
    new_metrics = {
        "avg_retrieval_score": latest["metrics.avg_retrieval_score"],
        "avg_generation_score": latest["metrics.avg_generation_score"],
        "avg_latency": latest["metrics.avg_latency"],
    }

    # Fetch production model (if exists)
    prod_versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    prod_metrics = None

    if prod_versions:
        prod_run_id = prod_versions[0].run_id
        prod_run = client.get_run(prod_run_id)
        prod_metrics = prod_run.data.metrics

    if should_promote(new_metrics, prod_metrics):
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=latest["tags.mlflow.runName"],
            stage="Production",
            archive_existing_versions=True,
        )
        print("✅ Promoted new model to Production")
    else:
        print("❌ Model not better than Production")
