# GPU Inference Platform Blueprint

A FastAPI inference service template with a CUDA container and an example
Kubernetes deployment. The bundled model is an echo fixture that runs on a CPU.

## Run the local demo

```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d '{"inputs":[1,2]}'
```

The health endpoint returns `{"status":"ok"}`. The prediction endpoint returns
`{"outputs":[1,2]}`. An empty input array returns HTTP 400.

## Deployment template

`Dockerfile` packages the API in a CUDA runtime image. `k8s.yaml` requests
one NVIDIA GPU, selects GPU nodes, and uses `/health` for readiness and
liveness. Configure the image reference and node selector for your cluster.
The probes check the fixture API's HTTP availability. A trained model adapter
would need its own readiness checks and resource sizing.
