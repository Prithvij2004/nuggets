from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["utils"])

@router.get("/")
def test():
    return {"ping": "pong"}
