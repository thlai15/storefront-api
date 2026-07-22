# API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/healthz` | Health check, used by k8s readiness/liveness probes |
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get a single product by ID |
| POST | `/orders` | Create an order (body: `customer_email`, `items[]`) |
| GET | `/metrics` | Prometheus metrics endpoint |

Full interactive docs available at `/docs` (Swagger UI) when the service is running.