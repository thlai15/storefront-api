from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/healthz")
def liveness() -> dict:
    """Liveness probe: process is up. No dependency checks."""
    return {"status": "ok"}


@router.get("/readyz")
def readiness(db: Session = Depends(get_db)) -> dict:
    """Readiness probe: dependencies (DB) are reachable."""
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - surface any DB failure as not-ready
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"database not reachable: {exc}",
        ) from exc
    return {"status": "ready"}
