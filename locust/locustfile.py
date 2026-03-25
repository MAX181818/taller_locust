from locust import HttpUser, between, task


class InferenceUser(HttpUser):
    wait_time = between(0.01, 0.2)

    @task
    def predict(self):
        payload = {
            "records": [
                {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                }
            ]
        }
        self.client.post("/predict", json=payload, name="POST /predict")
