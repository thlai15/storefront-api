# Storefront API

Product catalog and order management service for the storefront demo.

## Overview

FastAPI backend serving product listings and order creation for `storefront-web`. Backed by SQLite (demo only — see [Architecture](architecture.md) for production considerations).

## Local development

\`\`\`bash
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

## Endpoints

See [API Reference](api-reference.md) for the full list.

## Related

- Frontend: [storefront-web](../storefront-web)
- Deployed via Helm chart in this repo's `chart/` directory