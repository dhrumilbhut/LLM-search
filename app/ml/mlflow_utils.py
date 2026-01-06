import mlflow

def start_experiment(name: str):
    mlflow.set_experiment(name)
    return mlflow.start_run()
