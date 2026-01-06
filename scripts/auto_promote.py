import mlflow
from mlflow.tracking import MlflowClient

from app.ml.promotion_logic import should_promote
from app.ml.registry_utils import get_production_metrics
from app.ml.load_model import load_production_config
from app.ml.model_config import RAG_CONFIG


MODEL_NAME = "rag-search-model"
EXPERIMENT_NAME = "rag-evaluation"


def auto_promote():
    client = MlflowClient()

    # 1️⃣ Get the latest evaluation run
    runs = mlflow.search_runs(
        experiment_names=[EXPERIMENT_NAME],
        order_by=["attributes.start_time DESC"],
        max_results=1
    )

    if runs.empty:
        print("❌ No evaluation runs found")
        return

    latest_run = runs.iloc[0]

    new_metrics = {
        "avg_latency": latest_run["metrics.avg_latency"],
        "avg_generation_score": latest_run["metrics.avg_generation_score"]
    }

    # 2️⃣ Load production metrics (if any)
    prod_metrics = get_production_metrics(MODEL_NAME)

    # 3️⃣ Load configs
    new_config = RAG_CONFIG

    try:
        prod_config = load_production_config()
    except Exception:
        prod_config = None  # First deployment case

    # 4️⃣ Decide whether to promote
    promote = should_promote(
        new_metrics=new_metrics,
        prod_metrics=prod_metrics,
        new_config=new_config,
        prod_config=prod_config
    )

    if not promote:
        print("❌ Promotion blocked (no meaningful improvement)")
        return

    # 5️⃣ Find latest un-staged model version
    versions = client.get_latest_versions(
        name=MODEL_NAME,
        stages=["None"]
    )

    if not versions:
        print("⚠️ No candidate model version found for promotion")
        return

    candidate = versions[0]

    # 6️⃣ Promote to Production
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=candidate.version,
        stage="Production",
        archive_existing_versions=False
    )

    print(
        f"✅ Promoted model version {candidate.version} "
        f"to Production (run_id={candidate.run_id})"
    )


if __name__ == "__main__":
    auto_promote()
