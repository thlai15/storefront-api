# Architecture

## Data storage

Currently SQLite, written to `/data/storefront.db` inside the pod. This is a demo simplification — data does not survive pod restarts. Production would use a managed Postgres instance instead.

## Deployment

Deployed to Kubernetes via the Helm chart in `chart/`, exposed through ingress-nginx at `storefront.local/api`, with the `/api` prefix stripped via a rewrite rule before reaching the FastAPI app.

## Observability

- `/metrics` scraped by Prometheus via pod annotations
- Dashboard and alert rule (`storefront-api-high-cpu`) configured in Grafana, linked from this service's Backstage catalog entry