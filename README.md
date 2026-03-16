# GPU Inference Platform Blueprint

This repository provides a reference architecture for deploying GPU-accelerated
machine learning models in a production environment.  It includes a simple
FastAPI service for serving models, a Dockerfile for containerization, and
instructions for deploying to Kubernetes or Docker Compose with NVIDIA GPU
support.

## Features

- Minimal Python server (`app.py`) exposing a `/predict` endpoint.
- Container image definition using an official CUDA base image.
- Guidelines for configuring autoscaling, resource requests/limits, and
  health checks.
- Example deployment manifests for Kubernetes using GPU node selectors and
  affinity rules.

## Getting Started

Install dependencies and run the server locally (requires a GPU with CUDA):

```bash
pip install -r requirements.txt
python app.py
```

The server will load a stub model on startup.  POST JSON data to
`http://localhost:8000/predict` to receive a dummy response.

## Deployment

To build and run the Docker container:

```bash
docker build -t gpu-inference:latest .
docker run --gpus all -p 8000:8000 gpu-inference:latest
```

See `k8s.yaml` for an example Kubernetes deployment.  You may need to
customize the node selector labels to match your GPU nodes.

## Extending

Replace the `StubModel` class in `app.py` with your actual model loading
and inference code.  Configure resource limits in `k8s.yaml` based on your
model's memory and GPU usage.