import os
from functools import lru_cache
from typing import Any

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="MLflow Inference API", version="1.0.0")


class PredictionRequest(BaseModel):
    records: list[dict[str, Any]] = Field(
        ..., description="Lista de registros tabulares para inferencia"
    )


class PredictionResponse(BaseModel):
    predictions: list[Any]


@lru_cache(maxsize=1)
def get_model():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "")
    model_uri = os.getenv("MODEL_URI")

    if not model_uri:
        raise RuntimeError("MODEL_URI no está definido")

    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)

    return mlflow.pyfunc.load_model(model_uri)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    if not request.records:
        raise HTTPException(status_code=400, detail="records no puede estar vacío")

    try:
        model = get_model()
        df = pd.DataFrame(request.records)
        preds = model.predict(df)
        return PredictionResponse(predictions=list(preds))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error en inferencia: {exc}") from exc
