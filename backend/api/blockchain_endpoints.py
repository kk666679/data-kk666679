from fastapi import APIRouter

router = APIRouter(prefix="/api/blockchain", tags=["blockchain"])

@router.get("/status")
async def blockchain_status():
    return {
        "blockchain": "ethereum",
        "network": "testnet",
        "status": "connected"
    }