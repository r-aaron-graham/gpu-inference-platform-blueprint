# GPU Inference Platform Blueprint

A FastAPI inference service template with a CPU reviewer container and an example
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

`Dockerfile.cuda` is an optional CUDA runtime template. Its build and GPU execution need separate verification. The default `Dockerfile` uses Python 3.12 and packages the CPU fixture. `k8s.yaml` requests
one NVIDIA GPU, selects GPU nodes, and uses `/health` for readiness and
liveness. Configure the image reference and node selector for your cluster.
The probes check the fixture API's HTTP availability. A trained model adapter
would need its own readiness checks and resource sizing.

## Deployment verification

```sh
docker build -t reviewer-smoke .
docker run --rm -p 127.0.0.1:8000:8000 reviewer-smoke
```

From another terminal, run `curl --fail http://127.0.0.1:8000/health`. Expect HTTP 200. The smoke test exercises the echo fixture on a CPU. Kubernetes scheduling, model performance, and GPU execution remain unverified.
