"""Example GPU inference service.

This script defines a FastAPI application exposing a single `/predict`
endpoint.  It loads a stub model on startup and performs fake inference
for demonstration purposes.  Replace the `StubModel` class with your
actual machine learning model to serve real predictions.
"""

from __future__ import annotations

from typing import Any, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """Schema for prediction requests.  The `inputs` field holds a list
    of input values (e.g. feature vectors) to be passed to the model.
    """

    inputs: List[Any]


class PredictionResponse(BaseModel):
    """Schema for prediction responses.  The `outputs` field holds
    predictions corresponding to each input value.
    """

    outputs: List[Any]


class StubModel:
    """A stand‑in for a real machine learning model.

    The `predict` method simply echoes back the input values.  In a
    production system you would load your trained model (e.g., a PyTorch
    `torch.nn.Module` or a TensorFlow graph) here and perform
    inference on the GPU.
    """

    def predict(self, inputs: List[Any]) -> List[Any]:
        return inputs


app = FastAPI(title="GPU Inference Service", version="0.1.0")

# Instantiate the model once at startup.  Loading large models can be
# expensive so do it only once.  In a real implementation you might
# perform additional configuration here (e.g. setting device IDs).
model = StubModel()


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """Run inference on the provided inputs.

    Parameters
    ----------
    request: PredictionRequest
        The incoming prediction request containing a list of inputs.

    Returns
    -------
    PredictionResponse
        The model outputs corresponding to the inputs.
    """
    if not request.inputs:
        raise HTTPException(status_code=400, detail="No inputs provided")
    outputs = model.predict(request.inputs)
    return PredictionResponse(outputs=outputs)


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)