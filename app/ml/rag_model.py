import json
import mlflow.pyfunc

class RagConfigModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        with open(context.artifacts["config"]) as f:
            self.config = json.load(f)

    def predict(self, context, model_input):
        return self.config
