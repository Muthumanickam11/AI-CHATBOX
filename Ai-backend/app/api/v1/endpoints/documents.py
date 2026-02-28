from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.rag import process_document
# from app.api.deps import get_current_user # Day 4 dependency

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = "user-001", # Placeholder until fully auth constrained
    db: AsyncSession = Depends(get_db)
):
    """
    Day 6: Document Ingestion.
    Uploads file, processes chunks, and returns metadata.
    """
    content = await file.read()
    
    # Resolve user_id to int if necessary
    try:
        uid = int(user_id.replace("user-", "") if "user-" in str(user_id) else user_id)
    except:
        uid = 1
        
    result = await process_document(content, file.filename, uid, db)
    
    return {
        "doc_id": result["doc_id"],
        "file_name": file.filename,
        "user_id": user_id,
        "embedding_status": result["embedding_status"],
        "chunks_indexed": result["chunks_indexed"]
    }
