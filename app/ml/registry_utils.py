import mlflow

def get_production_metrics(model_name: str):
    client = mlflow.tracking.MlflowClient()

    versions = client.get_latest_versions(
        name=model_name,
        stages=["Production"]
    )

    if not versions:
        return None

    run_id = versions[0].run_id
    run = client.get_run(run_id)

    return run.data.metrics
