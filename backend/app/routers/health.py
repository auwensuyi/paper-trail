from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Load balancers (like AWS ALB) call this to check the app is alive."""
    return {"status": "ok"}
